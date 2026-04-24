from dataclasses import dataclass
from typing import List, Optional
from business.interfaces.readers import ISessionStatisticsReader, SessionStatsDTO


@dataclass
class UserSessionsResult:
    """Результат получения сессий пользователя"""
    success: bool
    user_id: int
    sessions: List[SessionStatsDTO]
    count: int
    error_message: Optional[str] = None


class GetUserSessionsUseCase:
    """
    Use Case: Получение сессий конкретного пользователя.
    
    Используется для:
    - анализа активности конкретного пользователя
    - административного мониторинга
    """
    
    def __init__(self, session_stats_reader: ISessionStatisticsReader):
        self.session_stats_reader = session_stats_reader
    
    def execute(self, user_id: int, limit: int = 50) -> UserSessionsResult:
        """
        Получить сессии пользователя.
        
        Args:
            user_id: ID пользователя
            limit: Максимальное количество сессий (по умолчанию 50)
        """
        try:
            sessions = self.session_stats_reader.get_by_user(user_id, limit)
            
            return UserSessionsResult(
                success=True,
                user_id=user_id,
                sessions=sessions,
                count=len(sessions)
            )
        except Exception as e:
            return UserSessionsResult(
                success=False,
                user_id=user_id,
                sessions=[],
                count=0,
                error_message=str(e)
            )