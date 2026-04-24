from dataclasses import dataclass
from typing import List, Optional
from business.interfaces.readers import ISessionStatisticsReader, SessionStatsDTO


@dataclass
class SessionStatisticsResult:
    """Результат получения статистики сессий"""
    success: bool
    statistics: List[SessionStatsDTO]
    count: int
    error_message: Optional[str] = None


class GetSessionStatisticsUseCase:
    """
    Use Case: Получение детальной статистики всех сессий.
    
    Возвращает для каждой сессии:
    - ID сессии и пользователя
    - время входа и выхода
    - длительность
    - количество отредактированных персонажей
    - количество просмотренных сущностей
    """
    
    def __init__(self, session_stats_reader: ISessionStatisticsReader):
        self.session_stats_reader = session_stats_reader
    
    def execute(self) -> SessionStatisticsResult:
        try:
            stats = self.session_stats_reader.get_all_statistics()
            
            return SessionStatisticsResult(
                success=True,
                statistics=stats,
                count=len(stats)
            )
        except Exception as e:
            return SessionStatisticsResult(
                success=False,
                statistics=[],
                count=0,
                error_message=str(e)
            )