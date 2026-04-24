from dataclasses import dataclass
from typing import Optional
from business.interfaces.readers import ISessionStatisticsReader


@dataclass
class ActiveSessionsCountResult:
    """Результат получения количества активных сессий"""
    success: bool
    count: int
    error_message: Optional[str] = None


class GetActiveSessionsCountUseCase:
    """
    Use Case: Получение количества активных сессий.
    
    Активная сессия — это сессия без logout_date.
    """
    
    def __init__(self, session_stats_reader: ISessionStatisticsReader):
        self.session_stats_reader = session_stats_reader
    
    def execute(self) -> ActiveSessionsCountResult:
        try:
            count = self.session_stats_reader.get_active_count()
            return ActiveSessionsCountResult(success=True, count=count)
        except Exception as e:
            return ActiveSessionsCountResult(
                success=False,
                count=0,
                error_message=str(e)
            )