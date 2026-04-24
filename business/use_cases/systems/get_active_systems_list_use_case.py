from dataclasses import dataclass
from typing import List, Optional
from business.value_objects import GameSystem
from business.interfaces.readers import IGameSystemReader


@dataclass
class ActiveSystemsResult:
    """Результат получения списка активных систем"""
    success: bool
    systems: List[GameSystem]
    count: int
    error_message: Optional[str] = None


class GetActiveSystemsListUseCase:
    """
    Use Case: Получение списка активных игровых систем.
    
    Используется для:
    - выпадающих списков при создании персонажа/контента
    - фильтрации статистики
    """
    
    def __init__(self, game_system_reader: IGameSystemReader):
        self.game_system_reader = game_system_reader
    
    def execute(self) -> ActiveSystemsResult:
        try:
            systems = self.game_system_reader.get_active_systems()
            
            return ActiveSystemsResult(
                success=True,
                systems=systems,
                count=len(systems)
            )
        except Exception as e:
            return ActiveSystemsResult(
                success=False,
                systems=[],
                count=0,
                error_message=str(e)
            )