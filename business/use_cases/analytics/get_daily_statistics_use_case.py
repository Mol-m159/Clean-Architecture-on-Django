from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime
from business.interfaces.readers import IAnalyticsReader, DailyStatsDTO


@dataclass
class DailyStatisticsResult:
    """Результат получения статистики за день"""
    success: bool
    date: date
    stats: Optional[DailyStatsDTO]
    error_message: Optional[str] = None


class GetDailyStatisticsUseCase:
    """
    Use Case: Получение статистики за конкретный день.
    
    Возвращает:
    - новых пользователей
    - новых персонажей
    - нового контента
    - активных сессий
    - просмотров
    """
    
    def __init__(self, analytics_reader: IAnalyticsReader):
        self.analytics_reader = analytics_reader
    
    def execute(self, target_date: Optional[date] = None) -> DailyStatisticsResult:
        """
        Получить статистику за день.
        
        Args:
            target_date: Дата (по умолчанию сегодня)
        """
        try:
            if target_date is None:
                target_date = datetime.now().date()
            
            stats = self.analytics_reader.get_daily_statistics(target_date)
            
            return DailyStatisticsResult(
                success=True,
                date=target_date,
                stats=stats
            )
        except Exception as e:
            return DailyStatisticsResult(
                success=False,
                date=target_date if target_date else datetime.now().date(),
                stats=None,
                error_message=str(e)
            )