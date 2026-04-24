from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from business.interfaces.readers import IHomebrewStatisticsReader


@dataclass
class NewHomebrewTodayResult:
    """Результат получения количества нового контента за сегодня"""
    success: bool
    count: int
    date: date
    error_message: Optional[str] = None


class GetNewHomebrewTodayUseCase:
    """
    Use Case: Получение количества нового homebrew контента за сегодня.
    """
    
    def __init__(self, homebrew_stats_reader: IHomebrewStatisticsReader):
        self.homebrew_stats_reader = homebrew_stats_reader
    
    def execute(self) -> NewHomebrewTodayResult:
        try:
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            count = self.homebrew_stats_reader.get_new_count_since(today_start)
            
            return NewHomebrewTodayResult(
                success=True,
                count=count,
                date=datetime.now().date()
            )
        except Exception as e:
            return NewHomebrewTodayResult(
                success=False,
                count=0,
                date=datetime.now().date(),
                error_message=str(e)
            )