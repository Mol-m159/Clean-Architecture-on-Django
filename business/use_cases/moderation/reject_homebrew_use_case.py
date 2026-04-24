from dataclasses import dataclass
from typing import Optional
from business.entities.homebrew import Homebrew, HomebrewStatus
from business.interfaces.repositories import IModerationRepository, IHomebrewRepository


@dataclass
class RejectResult:
    """Результат отклонения контента"""
    success: bool
    entity_id: int
    old_status: Optional[HomebrewStatus]
    new_status: Optional[HomebrewStatus]
    reason: Optional[str]
    error_message: Optional[str] = None


class RejectHomebrewUseCase:
    """
    Use Case: Отклонение контента модератором.
    
    Бизнес-правила (из homebrew.py):
    - Отклонить можно только контент в статусе MODERATION
    - После отклонения статус становится REJECTED
    - Добавляется запись в историю модерации с указанием причины
    """
    
    def __init__(
        self, 
        moderation_repository: IModerationRepository,
        homebrew_repository: IHomebrewRepository
    ):
        self.moderation_repository = moderation_repository
        self.homebrew_repository = homebrew_repository
    
    def execute(
        self, 
        entity_id: int, 
        moderator_id: int, 
        reason: Optional[str] = None
    ) -> RejectResult:
        """
        Отклонить контент.
        
        Args:
            entity_id: ID контента
            moderator_id: ID модератора
            reason: Причина отклонения (опционально)
            
        Returns:
            RejectResult с результатом операции
        """
        # Получаем контент
        homebrew = self.homebrew_repository.get_by_id(entity_id)
        
        if not homebrew:
            return RejectResult(
                success=False,
                entity_id=entity_id,
                old_status=None,
                new_status=None,
                reason=reason,
                error_message=f"Homebrew #{entity_id} not found"
            )
        
        old_status = homebrew.status
        
        # Проверяем, можно ли отклонить
        if homebrew.status != HomebrewStatus.MODERATION:
            return RejectResult(
                success=False,
                entity_id=entity_id,
                old_status=old_status,
                new_status=None,
                reason=reason,
                error_message=f"Cannot reject content with status {homebrew.status.value}"
            )
        
        try:
            # Используем бизнес-правило из сущности
            homebrew.reject(moderator_id)
            
            # Сохраняем изменения
            self.homebrew_repository.update(homebrew)
            
            # Добавляем запись в историю модерации с причиной
            self.moderation_repository.reject(entity_id, moderator_id, reason)
            
            return RejectResult(
                success=True,
                entity_id=entity_id,
                old_status=old_status,
                new_status=homebrew.status,
                reason=reason
            )
            
        except ValueError as e:
            return RejectResult(
                success=False,
                entity_id=entity_id,
                old_status=old_status,
                new_status=None,
                reason=reason,
                error_message=str(e)
            )
        except Exception as e:
            return RejectResult(
                success=False,
                entity_id=entity_id,
                old_status=old_status,
                new_status=None,
                reason=reason,
                error_message=f"Failed to reject: {str(e)}"
            )