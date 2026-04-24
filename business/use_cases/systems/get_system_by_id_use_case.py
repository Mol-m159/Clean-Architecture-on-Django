from dataclasses import dataclass
from typing import Optional
from business.value_objects import GameSystem
from business.interfaces.readers import IGameSystemReader


@dataclass
class SystemByIdResult:
    """Результат получения системы по ID"""
    success: bool
    system: Optional[GameSystem]
    error_message: Optional[str] = None


class GetSystemByIdUseCase:
    """
    Use Case: Получение игровой системы по ID.
    """
    
    def __init__(self, game_system_reader: IGameSystemReader):
        self.game_system_reader = game_system_reader
    
    def execute(self, system_id: int) -> SystemByIdResult:
        try:
            system = self.game_system_reader.get_by_id(system_id)
            
            if not system:
                return SystemByIdResult(
                    success=False,
                    system=None,
                    error_message=f"System #{system_id} not found"
                )
            
            return SystemByIdResult(
                success=True,
                system=system
            )
        except Exception as e:
            return SystemByIdResult(
                success=False,
                system=None,
                error_message=str(e)
            )