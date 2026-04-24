from dataclasses import dataclass
from typing import Optional
from business.interfaces.readers import ISystemDashboardReader, DashboardStatsDTO


@dataclass
class DashboardStatsResult:
    """Результат получения статистики для дашборда"""
    success: bool
    stats: Optional[DashboardStatsDTO]
    error_message: Optional[str] = None


class GetSystemDashboardStatsUseCase:
    """
    Use Case: Получение всех данных для дашборда администратора.
    
    Объединяет основные метрики системы:
    - общее количество пользователей
    - общее количество персонажей
    - общее количество homebrew контента
    - количество активных сессий
    - новые пользователи за сегодня
    - новые персонажи за сегодня
    - новый контент за сегодня
    """
    
    def __init__(self, dashboard_reader: ISystemDashboardReader):
        self.dashboard_reader = dashboard_reader
    
    def execute(self) -> DashboardStatsResult:
        try:
            stats = self.dashboard_reader.get_dashboard_stats()
            
            return DashboardStatsResult(
                success=True,
                stats=stats
            )
        except Exception as e:
            return DashboardStatsResult(
                success=False,
                stats=None,
                error_message=str(e)
            )