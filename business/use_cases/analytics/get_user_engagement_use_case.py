from dataclasses import dataclass
from typing import List, Optional
from business.interfaces.readers import IAnalyticsReader, UserEngagementDTO


@dataclass
class UserEngagementResult:
    """Результат получения метрик вовлеченности пользователей"""
    success: bool
    users: List[UserEngagementDTO]
    count: int
    average_engagement_score: float
    error_message: Optional[str] = None


class GetUserEngagementUseCase:
    """
    Use Case: Получение метрик вовлеченности пользователей.
    
    Метрики:
    - общее количество действий
    - количество уникальных систем
    - скоринг вовлеченности (0-100)
    """
    
    def __init__(self, analytics_reader: IAnalyticsReader):
        self.analytics_reader = analytics_reader
    
    def execute(self, limit: int = 100) -> UserEngagementResult:
        try:
            users = self.analytics_reader.get_user_engagement(limit)
            
            avg_score = 0.0
            if users:
                avg_score = sum(u.engagement_score for u in users) / len(users)
            
            return UserEngagementResult(
                success=True,
                users=users,
                count=len(users),
                average_engagement_score=round(avg_score, 2)
            )
        except Exception as e:
            return UserEngagementResult(
                success=False,
                users=[],
                count=0,
                average_engagement_score=0.0,
                error_message=str(e)
            )