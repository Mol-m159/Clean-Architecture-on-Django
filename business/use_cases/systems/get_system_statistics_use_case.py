from dataclasses import dataclass
from typing import Optional, Dict, Any
from business.interfaces.readers import IGameSystemReader


@dataclass
class SystemStatisticsResult:
    """Результат получения статистики по системе"""
    success: bool
    system_id: int
    total_characters: int
    total_homebrew: int
    total_views: int
    active_users: int
    error_message: Optional[str] = None


class GetSystemStatisticsUseCase:
    """
    Use Case: Получение статистики по игровой системе.
    
    Возвращает:
    - количество персонажей в системе
    - количество homebrew контента
    - количество просмотров
    - количество активных пользователей
    """
    
    def __init__(self, game_system_reader: IGameSystemReader):
        self.game_system_reader = game_system_reader
    
    def execute(self, system_id: int) -> SystemStatisticsResult:
        try:
            # Проверяем существование системы
            system = self.game_system_reader.get_by_id(system_id)
            
            if not system:
                return SystemStatisticsResult(
                    success=False,
                    system_id=system_id,
                    total_characters=0,
                    total_homebrew=0,
                    total_views=0,
                    active_users=0,
                    error_message=f"System #{system_id} not found"
                )
            
            stats = self.game_system_reader.get_system_statistics(system_id)
            
            return SystemStatisticsResult(
                success=True,
                system_id=system_id,
                total_characters=stats.get('total_characters', 0),
                total_homebrew=stats.get('total_homebrew', 0),
                total_views=stats.get('total_views', 0),
                active_users=stats.get('active_users', 0)
            )
        except Exception as e:
            return SystemStatisticsResult(
                success=False,
                system_id=system_id,
                total_characters=0,
                total_homebrew=0,
                total_views=0,
                active_users=0,
                error_message=str(e)
            )