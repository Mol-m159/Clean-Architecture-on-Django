from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import date
from business.interfaces import DailyStatsDTO, IAnalyticsReader

@dataclass
class MonthlyStatisticsResult:
    """Результат получения статистики за месяц"""
    success: bool
    year: int
    month: int
    month_name: str
    daily_stats: Dict[int, DailyStatsDTO]
    totals: Dict[str, int]
    error_message: Optional[str] = None


class GetMonthlyStatisticsUseCase:
    """
    Use Case: Получение статистики за месяц.
    
    Возвращает дневную разбивку и итоги за месяц.
    """
    
    MONTH_NAMES = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
        5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
        9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }
    
    def __init__(self, analytics_reader: IAnalyticsReader):
        self.analytics_reader = analytics_reader
    
    def execute(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> MonthlyStatisticsResult:
        """
        Получить статистику за месяц.
        
        Args:
            year: Год (по умолчанию текущий)
            month: Месяц (1-12, по умолчанию текущий)
        """
        try:
            today = date.today()
            if year is None:
                year = today.year
            if month is None:
                month = today.month
            
            data = self.analytics_reader.get_monthly_statistics(year, month)
            
            return MonthlyStatisticsResult(
                success=True,
                year=year,
                month=month,
                month_name=self.MONTH_NAMES.get(month, ''),
                daily_stats=data.get('daily_stats', {}),
                totals=data.get('totals', {})
            )
        except Exception as e:
            return MonthlyStatisticsResult(
                success=False,
                year=year if year else date.today().year,
                month=month if month else date.today().month,
                month_name='',
                daily_stats={},
                totals={},
                error_message=str(e)
            )