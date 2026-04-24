from dataclasses import dataclass
from typing import List, Optional
from business.interfaces.readers import IUserStatisticsReader, UserStatsDTO


@dataclass
class UserStatisticsResult:
    """Результат получения статистики пользователей"""
    success: bool
    statistics: List[UserStatsDTO]
    count: int
    error_message: Optional[str] = None


class GetUserStatisticsUseCase:
    """
    Use Case: Получение детальной статистики пользователей.
    
    Возвращает для каждого пользователя и системы:
    - количество персонажей
    - количество homebrew контента
    - дату последней активности
    """
    
    def __init__(self, user_stats_reader: IUserStatisticsReader):
        self.user_stats_reader = user_stats_reader
    
    def execute(self) -> UserStatisticsResult:
        try:
            stats = self.user_stats_reader.get_all_statistics()
            
            return UserStatisticsResult(
                success=True,
                statistics=stats,
                count=len(stats)
            )
        except Exception as e:
            return UserStatisticsResult(
                success=False,
                statistics=[],
                count=0,
                error_message=str(e)
            )