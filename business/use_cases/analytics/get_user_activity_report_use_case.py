from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from business.interfaces.readers import IAnalyticsReader, UserActivityReportDTO


@dataclass
class UserActivityReportResult:
    """Результат получения отчета по активности пользователей"""
    success: bool
    report: List[UserActivityReportDTO]
    count: int
    period_start: Optional[datetime]
    period_end: Optional[datetime]
    error_message: Optional[str] = None


class GetUserActivityReportUseCase:
    """
    Use Case: Получение отчета по активности пользователей.
    
    Отчет включает:
    - количество сессий
    - общую длительность
    - созданные персонажи и контент
    - дату последней активности
    """
    
    def __init__(self, analytics_reader: IAnalyticsReader):
        self.analytics_reader = analytics_reader
    
    def execute(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> UserActivityReportResult:
        try:
            report = self.analytics_reader.get_user_activity_report(
                start_date, end_date, limit
            )
            
            return UserActivityReportResult(
                success=True,
                report=report,
                count=len(report),
                period_start=start_date,
                period_end=end_date
            )
        except Exception as e:
            return UserActivityReportResult(
                success=False,
                report=[],
                count=0,
                period_start=start_date,
                period_end=end_date,
                error_message=str(e)
            )