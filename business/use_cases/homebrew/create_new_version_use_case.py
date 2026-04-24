from dataclasses import dataclass
from typing import Optional
from business.entities.homebrew import Homebrew
from business.interfaces.repositories import IHomebrewRepository


@dataclass
class NewVersionResult:
    """Результат создания новой версии"""
    success: bool
    entity_id: int
    version_number: Optional[int]
    error_message: Optional[str] = None


class CreateNewVersionUseCase:
    """
    Use Case: Создание новой версии контента.
    
    Бизнес-правила:
    - Новая версия создается при изменении контента
    - Номер версии = предыдущий + 1
    """
    
    def __init__(self, homebrew_repository: IHomebrewRepository):
        self.homebrew_repository = homebrew_repository
    
    def execute(self, entity_id: int) -> NewVersionResult:
        """
        Создать новую версию контента.
        
        Args:
            entity_id: ID контента
            
        Returns:
            NewVersionResult с номером новой версии
        """
        # Проверяем существование
        homebrew = self.homebrew_repository.get_by_id(entity_id)
        
        if not homebrew:
            return NewVersionResult(
                success=False,
                entity_id=entity_id,
                version_number=None,
                error_message=f"Homebrew #{entity_id} not found"
            )
        
        # Получаем последнюю версию
        last_version = self.homebrew_repository.get_latest_version(entity_id)
        new_version = (last_version.version_number + 1) if last_version else 1
        
        # Создаем новую версию
        self.homebrew_repository.add_edit_version(entity_id, new_version)
        
        return NewVersionResult(
            success=True,
            entity_id=entity_id,
            version_number=new_version
        )