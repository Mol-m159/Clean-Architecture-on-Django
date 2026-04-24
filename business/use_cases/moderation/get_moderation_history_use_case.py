from dataclasses import dataclass
from typing import List, Optional
from business.value_objects import HomebrewModeration
from business.interfaces.repositories import IModerationRepository


@dataclass
class ModerationHistoryResult:
    """Результат получения истории модерации"""
    success: bool
    entity_id: int
    history: List[HomebrewModeration]
    count: int
    error_message: Optional[str] = None


class GetModerationHistoryUseCase:
    """
    Use Case: Получение истории модерации контента.
    
    Возвращает все события модерации для указанного контента,
    отсортированные по дате (сначала новые).
    """
    
    def __init__(self, moderation_repository: IModerationRepository):
        self.moderation_repository = moderation_repository
    
    def execute(self, entity_id: int) -> ModerationHistoryResult:
        """
        Получить историю модерации контента.
        
        Args:
            entity_id: ID контента
            
        Returns:
            ModerationHistoryResult со списком событий модерации
        """
        try:
            history = self.moderation_repository.get_moderation_history(entity_id)
            
            return ModerationHistoryResult(
                success=True,
                entity_id=entity_id,
                history=history,
                count=len(history)
            )
            
        except Exception as e:
            return ModerationHistoryResult(
                success=False,
                entity_id=entity_id,
                history=[],
                count=0,
                error_message=f"Failed to get moderation history: {str(e)}"
            )