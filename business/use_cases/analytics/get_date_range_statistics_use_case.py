from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import date
from business.interfaces import DailyStatsDTO, IAnalyticsReader


@dataclass
class DateRangeStatisticsResult:
    """Результат получения статистики за период"""
    success: bool
    start_date: date
    end_date: date
    days_count: int
    daily_stats: Dict[date, DailyStatsDTO]
    totals: Dict[str, int]
    error_message: Optional[str] = None


class GetDateRangeStatisticsUseCase:
    """
    Use Case: Получение статистики за произвольный период.
    
    Позволяет анализировать данные за любой интервал времени.
    """
    
    def __init__(self, analytics_reader: IAnalyticsReader):
        self.analytics_reader = analytics_reader
    
    def execute(self, start_date: date, end_date: date) -> DateRangeStatisticsResult:
        """
        Получить статистику за период.
        
        Args:
            start_date: Начальная дата
            end_date: Конечная дата
        """
        try:
            if start_date > end_date:
                return DateRangeStatisticsResult(
                    success=False,
                    start_date=start_date,
                    end_date=end_date,
                    days_count=0,
                    daily_stats={},
                    totals={},
                    error_message="Start date must be before end date"
                )
            
            days_count = (end_date - start_date).days + 1
            data = self.analytics_reader.get_date_range_statistics(start_date, end_date)
            
            return DateRangeStatisticsResult(
                success=True,
                start_date=start_date,
                end_date=end_date,
                days_count=days_count,
                daily_stats=data.get('daily_stats', {}),
                totals=data.get('totals', {})
            )
        except Exception as e:
            return DateRangeStatisticsResult(
                success=False,
                start_date=start_date,
                end_date=end_date,
                days_count=0,
                daily_stats={},
                totals={},
                error_message=str(e)
            )