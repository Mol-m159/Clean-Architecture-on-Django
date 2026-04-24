from dataclasses import dataclass
from typing import List, Optional
from business.interfaces.readers import ICharacterStatisticsReader, CharacterStatsDTO


@dataclass
class CharactersStatisticsResult:
    """Результат получения статистики персонажей"""
    success: bool
    statistics: List[CharacterStatsDTO]
    total_characters: int
    error_message: Optional[str] = None


class GetCharactersStatisticsUseCase:
    """
    Use Case: Получение статистики по персонажам.
    
    Возвращает статистику в разрезе игровых систем:
    - количество персонажей
    - количество созданных сегодня
    - средний возраст персонажа в днях
    """
    
    def __init__(self, character_stats_reader: ICharacterStatisticsReader):
        self.character_stats_reader = character_stats_reader
    
    def execute(self) -> CharactersStatisticsResult:
        try:
            stats = self.character_stats_reader.get_statistics_by_system()
            total = sum(s.character_count for s in stats)
            
            return CharactersStatisticsResult(
                success=True,
                statistics=stats,
                total_characters=total
            )
        except Exception as e:
            return CharactersStatisticsResult(
                success=False,
                statistics=[],
                total_characters=0,
                error_message=str(e)
            )