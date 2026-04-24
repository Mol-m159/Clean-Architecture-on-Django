from dataclasses import dataclass
from typing import Optional
from business.entities.homebrew import HomebrewStatus
from business.interfaces.repositories import IHomebrewRepository


@dataclass
class ModerationStatusResult:
    """Результат получения статуса модерации"""
    success: bool
    entity_id: int
    status: Optional[HomebrewStatus]
    is_approved: bool = False
    is_pending: bool = False
    error_message: Optional[str] = None


class GetHomebrewModerationStatusUseCase:
    """
    Use Case: Получение статуса модерации контента.
    """
    
    def __init__(self, homebrew_repository: IHomebrewRepository):
        self.homebrew_repository = homebrew_repository
    
    def execute(self, entity_id: int) -> ModerationStatusResult:
        """
        Получить статус модерации.
        
        Args:
            entity_id: ID контента
            
        Returns:
            ModerationStatusResult со статусом
        """
        homebrew = self.homebrew_repository.get_by_id(entity_id)
        
        if not homebrew:
            return ModerationStatusResult(
                success=False,
                entity_id=entity_id,
                status=None,
                error_message=f"Homebrew #{entity_id} not found"
            )
        
        return ModerationStatusResult(
            success=True,
            entity_id=entity_id,
            status=homebrew.status,
            is_approved=homebrew.is_approved,
            is_pending=homebrew.is_pending
        )