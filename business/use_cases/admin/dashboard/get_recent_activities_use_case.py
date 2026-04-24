from dataclasses import dataclass
from typing import List, Optional
from business.interfaces.readers import ISystemDashboardReader, RecentActivityDTO


@dataclass
class RecentActivitiesResult:
    """Результат получения последних активностей"""
    success: bool
    activities: List[RecentActivityDTO]
    count: int
    error_message: Optional[str] = None


class GetRecentActivitiesUseCase:
    """
    Use Case: Получение последних активностей в системе.
    
    Возвращает последние сессии пользователей для отображения
    на дашборде администратора.
    """
    
    def __init__(self, dashboard_reader: ISystemDashboardReader):
        self.dashboard_reader = dashboard_reader
    
    def execute(self, limit: int = 10) -> RecentActivitiesResult:
        """
        Получить последние активности.
        
        Args:
            limit: Максимальное количество активностей (по умолчанию 10)
        """
        try:
            activities = self.dashboard_reader.get_recent_activities(limit)
            
            return RecentActivitiesResult(
                success=True,
                activities=activities,
                count=len(activities)
            )
        except Exception as e:
            return RecentActivitiesResult(
                success=False,
                activities=[],
                count=0,
                error_message=str(e)
            )