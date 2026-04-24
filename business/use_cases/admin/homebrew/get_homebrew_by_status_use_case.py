from dataclasses import dataclass
from typing import List, Optional, Any
from business.interfaces.readers import IHomebrewStatisticsReader


@dataclass
class HomebrewByStatusResult:
    """Результат получения контента по статусу"""
    success: bool
    status: str
    items: List[Any]
    count: int
    error_message: Optional[str] = None


class GetHomebrewByStatusUseCase:
    """
    Use Case: Получение homebrew контента по статусу.
    
    Используется для:
    - просмотра черновиков
    - просмотра очереди модерации
    - просмотра отклоненного контента
    """
    
    def __init__(self, homebrew_stats_reader: IHomebrewStatisticsReader):
        self.homebrew_stats_reader = homebrew_stats_reader
    
    def execute(self, status: str) -> HomebrewByStatusResult:
        """
        Получить контент по статусу.
        
        Args:
            status: Статус ('draft', 'moderation', 'approved', 'rejected')
        """
        try:
            items = self.homebrew_stats_reader.get_by_status(status)
            
            return HomebrewByStatusResult(
                success=True,
                status=status,
                items=items,
                count=len(items)
            )
        except Exception as e:
            return HomebrewByStatusResult(
                success=False,
                status=status,
                items=[],
                count=0,
                error_message=str(e)
            )