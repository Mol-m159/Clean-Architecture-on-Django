from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from business.interfaces.readers import ICharacterStatisticsReader


@dataclass
class NewCharactersTodayResult:
    """Результат получения количества новых персонажей за сегодня"""
    success: bool
    count: int
    date: date
    error_message: Optional[str] = None


class GetNewCharactersTodayUseCase:
    """
    Use Case: Получение количества новых персонажей за сегодня.
    """
    
    def __init__(self, character_stats_reader: ICharacterStatisticsReader):
        self.character_stats_reader = character_stats_reader
    
    def execute(self) -> NewCharactersTodayResult:
        try:
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            count = self.character_stats_reader.get_new_count_since(today_start)
            
            return NewCharactersTodayResult(
                success=True,
                count=count,
                date=datetime.now().date()
            )
        except Exception as e:
            return NewCharactersTodayResult(
                success=False,
                count=0,
                date=datetime.now().date(),
                error_message=str(e)
            )