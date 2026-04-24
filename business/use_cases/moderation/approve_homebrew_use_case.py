from dataclasses import dataclass
from typing import Optional
from business.entities.homebrew import Homebrew, HomebrewStatus
from business.interfaces.repositories import IModerationRepository, IHomebrewRepository


@dataclass
class ApproveResult:
    """Результат одобрения контента"""
    success: bool
    entity_id: int
    old_status: Optional[HomebrewStatus]
    new_status: Optional[HomebrewStatus]
    error_message: Optional[str] = None


class ApproveHomebrewUseCase:
    """
    Use Case: Одобрение контента модератором.
    
    Бизнес-правила (из homebrew.py):
    - Одобрить можно только контент в статусе MODERATION
    - После одобрения статус становится APPROVED
    - Добавляется запись в историю модерации
    """
    
    def __init__(
        self, 
        moderation_repository: IModerationRepository,
        homebrew_repository: IHomebrewRepository
    ):
        self.moderation_repository = moderation_repository
        self.homebrew_repository = homebrew_repository
    
    def execute(self, entity_id: int, moderator_id: int) -> ApproveResult:
        """
        Одобрить контент.
        
        Args:
            entity_id: ID контента
            moderator_id: ID модератора
            
        Returns:
            ApproveResult с результатом операции
        """
        # Получаем контент
        homebrew = self.homebrew_repository.get_by_id(entity_id)
        
        if not homebrew:
            return ApproveResult(
                success=False,
                entity_id=entity_id,
                old_status=None,
                new_status=None,
                error_message=f"Homebrew #{entity_id} not found"
            )
        
        old_status = homebrew.status
        
        # Проверяем, можно ли одобрить
        if homebrew.status != HomebrewStatus.MODERATION:
            return ApproveResult(
                success=False,
                entity_id=entity_id,
                old_status=old_status,
                new_status=None,
                error_message=f"Cannot approve content with status {homebrew.status.value}"
            )
        
        try:
            # Используем бизнес-правило из сущности
            homebrew.approve(moderator_id)
            
            # Сохраняем изменения
            self.homebrew_repository.update(homebrew)
            
            # Добавляем запись в историю модерации
            self.moderation_repository.approve(entity_id, moderator_id)
            
            return ApproveResult(
                success=True,
                entity_id=entity_id,
                old_status=old_status,
                new_status=homebrew.status
            )
            
        except ValueError as e:
            return ApproveResult(
                success=False,
                entity_id=entity_id,
                old_status=old_status,
                new_status=None,
                error_message=str(e)
            )
        except Exception as e:
            return ApproveResult(
                success=False,
                entity_id=entity_id,
                old_status=old_status,
                new_status=None,
                error_message=f"Failed to approve: {str(e)}"
            )