from dataclasses import dataclass
from typing import Optional
from business.interfaces.repositories import IModerationRepository


@dataclass
class ModerationQueueCountResult:
    """Результат получения количества в очереди"""
    success: bool
    count: int
    error_message: Optional[str] = None


class GetModerationQueueCountUseCase:
    """
    Use Case: Получение количества элементов в очереди на модерацию.
    
    Используется для отображения счетчика на дашборде модератора.
    """
    
    def __init__(self, moderation_repository: IModerationRepository):
        self.moderation_repository = moderation_repository
    
    def execute(self) -> ModerationQueueCountResult:
        """
        Получить количество элементов в очереди.
        
        Returns:
            ModerationQueueCountResult с количеством
        """
        try:
            queue = self.moderation_repository.get_moderation_queue()
            count = len(queue)
            
            return ModerationQueueCountResult(
                success=True,
                count=count
            )
            
        except Exception as e:
            return ModerationQueueCountResult(
                success=False,
                count=0,
                error_message=f"Failed to get queue count: {str(e)}"
            )