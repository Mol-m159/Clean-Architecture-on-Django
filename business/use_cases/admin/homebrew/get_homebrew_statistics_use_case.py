from dataclasses import dataclass
from typing import Optional, Dict
from business.interfaces.readers import IHomebrewStatisticsReader, HomebrewStatsDTO


@dataclass
class HomebrewStatisticsResult:
    """Результат получения статистики контента"""
    success: bool
    total_count: int
    by_status: Dict[str, int]
    by_type: Dict[str, int]
    created_today: int
    error_message: Optional[str] = None


class GetHomebrewStatisticsUseCase:
    """
    Use Case: Получение статистики по homebrew контенту.
    
    Возвращает:
    - общее количество контента
    - распределение по статусам (draft, moderation, approved, rejected)
    - распределение по типам (spell, item, class, race, other)
    - количество созданного сегодня
    """
    
    def __init__(self, homebrew_stats_reader: IHomebrewStatisticsReader):
        self.homebrew_stats_reader = homebrew_stats_reader
    
    def execute(self) -> HomebrewStatisticsResult:
        try:
            stats = self.homebrew_stats_reader.get_statistics()
            
            return HomebrewStatisticsResult(
                success=True,
                total_count=stats.total_count,
                by_status=stats.by_status,
                by_type=stats.by_type,
                created_today=stats.created_today
            )
        except Exception as e:
            return HomebrewStatisticsResult(
                success=False,
                total_count=0,
                by_status={},
                by_type={},
                created_today=0,
                error_message=str(e)
            )