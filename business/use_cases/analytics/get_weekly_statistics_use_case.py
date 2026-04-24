from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import date, timedelta
from business.interfaces.readers import DailyStatsDTO, IAnalyticsReader

@dataclass
class WeeklyStatisticsResult:
    """Результат получения статистики за неделю"""
    success: bool
    week_start: date
    week_end: date
    daily_stats: Dict[str, DailyStatsDTO]
    totals: Dict[str, int]
    error_message: Optional[str] = None


class GetWeeklyStatisticsUseCase:
    """
    Use Case: Получение статистики за неделю.
    
    Возвращает дневную разбивку и итоги за неделю.
    """
    
    def __init__(self, analytics_reader: IAnalyticsReader):
        self.analytics_reader = analytics_reader
    
    def execute(self, week_start: Optional[date] = None) -> WeeklyStatisticsResult:
        """
        Получить статистику за неделю.
        
        Args:
            week_start: Дата понедельника (по умолчанию текущая неделя)
        """
        try:
            if week_start is None:
                # Получаем понедельник текущей недели
                today = date.today()
                week_start = today - timedelta(days=today.weekday())
            
            week_end = week_start + timedelta(days=6)
            
            data = self.analytics_reader.get_weekly_statistics(week_start)
            
            return WeeklyStatisticsResult(
                success=True,
                week_start=week_start,
                week_end=week_end,
                daily_stats=data.get('daily_stats', {}),
                totals=data.get('totals', {})
            )
        except Exception as e:
            return WeeklyStatisticsResult(
                success=False,
                week_start=week_start if week_start else date.today(),
                week_end=week_start + timedelta(days=6) if week_start else date.today(),
                daily_stats={},
                totals={},
                error_message=str(e)
            )