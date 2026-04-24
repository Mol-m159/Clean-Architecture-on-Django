from dataclasses import dataclass
from typing import Optional
from business.interfaces.readers import IUserStatisticsReader


@dataclass
class TotalUsersCountResult:
    """Результат получения количества пользователей"""
    success: bool
    count: int
    error_message: Optional[str] = None


class GetTotalUsersCountUseCase:
    """
    Use Case: Получение общего количества пользователей.
    """
    
    def __init__(self, user_stats_reader: IUserStatisticsReader):
        self.user_stats_reader = user_stats_reader
    
    def execute(self) -> TotalUsersCountResult:
        try:
            count = self.user_stats_reader.get_total_count()
            return TotalUsersCountResult(success=True, count=count)
        except Exception as e:
            return TotalUsersCountResult(
                success=False, 
                count=0, 
                error_message=str(e)
            )