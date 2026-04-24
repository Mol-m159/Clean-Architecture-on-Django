from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from business.entities.homebrew import Homebrew
from business.interfaces.repositories import IModerationRepository


class PriorityLevel(Enum):
    """Уровни приоритета для модерации"""
    HIGH = "high"      # 2+ дней в очереди
    MEDIUM = "medium"  # 1 день в очереди
    LOW = "low"        # менее дня в очереди


@dataclass
class PriorityQueueItem:
    """Элемент очереди с приоритетом"""
    homebrew: Homebrew
    days_in_queue: int
    priority: PriorityLevel


@dataclass
class PriorityQueueResult:
    """Результат получения очереди с приоритетами"""
    success: bool
    high_priority: List[PriorityQueueItem]
    medium_priority: List[PriorityQueueItem]
    low_priority: List[PriorityQueueItem]
    total_count: int
    high_count: int
    medium_count: int
    low_count: int
    error_message: Optional[str] = None


class GetModerationQueuePriorityUseCase:
    """
    Use Case: Получение очереди модерации с приоритетами.
    
    Бизнес-правила (из moder.py):
    - HIGH приоритет: контент в очереди 2+ дня
    - MEDIUM приоритет: контент в очереди 1 день
    - LOW приоритет: контент в очереди менее дня
    """
    
    def __init__(self, moderation_repository: IModerationRepository):
        self.moderation_repository = moderation_repository
    
    def execute(self) -> PriorityQueueResult:
        """
        Получить очередь с приоритетами.
        
        Returns:
            PriorityQueueResult с элементами, разделенными по приоритетам
        """
        try:
            # Получаем очередь с днями ожидания
            items_with_days = self.moderation_repository.get_moderation_queue_with_days()
            
            high = []
            medium = []
            low = []
            
            for item in items_with_days:
                homebrew = item['homebrew']
                days = item['days_in_queue']
                
                if days >= 2:
                    priority = PriorityLevel.HIGH
                    high.append(PriorityQueueItem(homebrew, days, priority))
                elif days == 1:
                    priority = PriorityLevel.MEDIUM
                    medium.append(PriorityQueueItem(homebrew, days, priority))
                else:
                    priority = PriorityLevel.LOW
                    low.append(PriorityQueueItem(homebrew, days, priority))
            
            return PriorityQueueResult(
                success=True,
                high_priority=high,
                medium_priority=medium,
                low_priority=low,
                total_count=len(high) + len(medium) + len(low),
                high_count=len(high),
                medium_count=len(medium),
                low_count=len(low)
            )
            
        except Exception as e:
            return PriorityQueueResult(
                success=False,
                high_priority=[],
                medium_priority=[],
                low_priority=[],
                total_count=0,
                high_count=0,
                medium_count=0,
                low_count=0,
                error_message=f"Failed to get priority queue: {str(e)}"
            )