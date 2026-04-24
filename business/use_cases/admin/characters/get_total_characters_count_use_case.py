from dataclasses import dataclass
from typing import Optional
from business.interfaces.readers import ICharacterStatisticsReader


@dataclass
class TotalCharactersCountResult:
    """Результат получения количества персонажей"""
    success: bool
    count: int
    error_message: Optional[str] = None


class GetTotalCharactersCountUseCase:
    """
    Use Case: Получение общего количества персонажей.
    """
    
    def __init__(self, character_stats_reader: ICharacterStatisticsReader):
        self.character_stats_reader = character_stats_reader
    
    def execute(self) -> TotalCharactersCountResult:
        try:
            count = self.character_stats_reader.get_total_count()
            return TotalCharactersCountResult(success=True, count=count)
        except Exception as e:
            return TotalCharactersCountResult(
                success=False, 
                count=0, 
                error_message=str(e)
            )