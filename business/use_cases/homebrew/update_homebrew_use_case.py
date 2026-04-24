# business/use_cases/update_homebrew_uc.py

from dataclasses import dataclass
from typing import Optional
from business.entities.homebrew import Homebrew, HomebrewType, HomebrewStatus
from business.interfaces.repositories import IHomebrewRepository


@dataclass
class UpdateHomebrewResult:
    """Результат обновления контента"""
    success: bool
    homebrew: Optional[Homebrew]
    error_message: Optional[str] = None
    status_changed: bool = False


class UpdateHomebrewUseCase:
    """
    Use Case: Обновление homebrew контента.
    
    Бизнес-правила:
    - Обновлять можно только DRAFT или REJECTED контент
    - При изменении типа или системы создается новая версия
    - Если контент был REJECTED и его изменили, статус становится DRAFT
    """
    
    def __init__(self, homebrew_repository: IHomebrewRepository):
        self.homebrew_repository = homebrew_repository
    
    def execute(
        self,
        entity_id: int,
        new_system_id: Optional[int] = None,
        new_entity_type: Optional[str] = None
    ) -> UpdateHomebrewResult:
        """
        Обновить контент.
        
        Args:
            entity_id: ID контента
            new_system_id: Новая система (опционально)
            new_entity_type: Новый тип (опционально)
            
        Returns:
            UpdateHomebrewResult с обновленным контентом
        """
        # Получаем контент
        homebrew = self.homebrew_repository.get_by_id(entity_id)
        
        if not homebrew:
            return UpdateHomebrewResult(
                success=False,
                homebrew=None,
                error_message=f"Homebrew #{entity_id} not found"
            )
        
        # Проверяем, можно ли редактировать
        if not homebrew.can_be_edited:
            return UpdateHomebrewResult(
                success=False,
                homebrew=homebrew,
                error_message=f"Cannot edit content with status {homebrew.status.value}"
            )
        
        # Отслеживаем изменения
        changed = False
        old_status = homebrew.status
        
        if new_system_id is not None and new_system_id != homebrew.system_id:
            homebrew.system_id = new_system_id
            changed = True
        
        if new_entity_type is not None:
            new_type = HomebrewType.from_string(new_entity_type)
            if new_type != homebrew.entity_type:
                homebrew.entity_type = new_type
                changed = True
        
        # ВАЖНО: Если контент был REJECTED и произошли изменения, меняем статус на DRAFT
        status_changed = False
        if old_status == HomebrewStatus.REJECTED and changed:
            homebrew.status = HomebrewStatus.DRAFT
            status_changed = True
        
        # Сохраняем изменения
        self.homebrew_repository.update(homebrew)
        
        # Если были изменения, создаем новую версию
        if changed:
            last_version = self.homebrew_repository.get_latest_version(entity_id)
            new_version = (last_version.version_number + 1) if last_version else 1
            self.homebrew_repository.add_edit_version(entity_id, new_version)
        
        return UpdateHomebrewResult(
            success=True,
            homebrew=homebrew,
            status_changed=status_changed
        )