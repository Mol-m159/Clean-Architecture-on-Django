from dataclasses import dataclass
from typing import List, Optional
from business.entities.homebrew import Homebrew
from business.interfaces.repositories import IModerationRepository


@dataclass
class ModerationQueueResult:
    """Результат получения очереди модерации"""
    success: bool
    queue: List[Homebrew]
    count: int
    error_message: Optional[str] = None


class GetModerationQueueUseCase:
    """
    Use Case: Получение очереди на модерацию.
    
    Возвращает список контента в статусе MODERATION,
    отсортированный по дате создания (старейшие первыми).
    """
    
    def __init__(self, moderation_repository: IModerationRepository):
        self.moderation_repository = moderation_repository
    
    def execute(self) -> ModerationQueueResult:
        """
        Получить очередь на модерацию.
        
        Returns:
            ModerationQueueResult со списком контента на модерации
        """
        try:
            queue = self.moderation_repository.get_moderation_queue(
                sort_by_date_asc=True
            )
            
            return ModerationQueueResult(
                success=True,
                queue=queue,
                count=len(queue)
            )
            
        except Exception as e:
            return ModerationQueueResult(
                success=False,
                queue=[],
                count=0,
                error_message=f"Failed to get moderation queue: {str(e)}"
            )