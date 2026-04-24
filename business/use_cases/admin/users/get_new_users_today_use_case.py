from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from business.interfaces.readers import IUserStatisticsReader


@dataclass
class NewUsersTodayResult:
    """Результат получения количества новых пользователей за сегодня"""
    success: bool
    count: int
    date: date
    error_message: Optional[str] = None


class GetNewUsersTodayUseCase:
    """
    Use Case: Получение количества новых пользователей за сегодня.
    """
    
    def __init__(self, user_stats_reader: IUserStatisticsReader):
        self.user_stats_reader = user_stats_reader
    
    def execute(self) -> NewUsersTodayResult:
        try:
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            count = self.user_stats_reader.get_new_count_since(today_start)
            
            return NewUsersTodayResult(
                success=True,
                count=count,
                date=datetime.now().date()
            )
        except Exception as e:
            return NewUsersTodayResult(
                success=False,
                count=0,
                date=datetime.now().date(),
                error_message=str(e)
            )