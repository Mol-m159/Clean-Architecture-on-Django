from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from business.interfaces.readers import ISystemDashboardReader


@dataclass
class SystemHealthResult:
    """Результат проверки состояния системы"""
    success: bool
    status: str  # 'healthy', 'degraded', 'unhealthy'
    metrics: Dict[str, Any]
    checked_at: datetime
    error_message: Optional[str] = None


class GetSystemHealthUseCase:
    """
    Use Case: Получение информации о состоянии системы.
    
    Возвращает метрики здоровья системы:
    - статус БД
    - количество активных сессий
    - и другие системные метрики
    """
    
    def __init__(self, dashboard_reader: ISystemDashboardReader):
        self.dashboard_reader = dashboard_reader
    
    def execute(self) -> SystemHealthResult:
        try:
            health_data = self.dashboard_reader.get_system_health()
            
            status = health_data.get('status', 'unknown')
            metrics = health_data.get('metrics', {})
            
            return SystemHealthResult(
                success=True,
                status=status,
                metrics=metrics,
                checked_at=datetime.now()
            )
        except Exception as e:
            return SystemHealthResult(
                success=False,
                status='unhealthy',
                metrics={},
                checked_at=datetime.now(),
                error_message=str(e)
            )