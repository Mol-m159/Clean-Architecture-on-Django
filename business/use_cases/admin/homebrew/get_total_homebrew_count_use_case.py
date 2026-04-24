from dataclasses import dataclass
from typing import Optional
from business.interfaces.readers import IHomebrewStatisticsReader


@dataclass
class TotalHomebrewCountResult:
    """Результат получения количества контента"""
    success: bool
    count: int
    error_message: Optional[str] = None


class GetTotalHomebrewCountUseCase:
    """
    Use Case: Получение общего количества homebrew контента.
    """
    
    def __init__(self, homebrew_stats_reader: IHomebrewStatisticsReader):
        self.homebrew_stats_reader = homebrew_stats_reader
    
    def execute(self) -> TotalHomebrewCountResult:
        try:
            count = self.homebrew_stats_reader.get_total_count()
            return TotalHomebrewCountResult(success=True, count=count)
        except Exception as e:
            return TotalHomebrewCountResult(
                success=False, 
                count=0, 
                error_message=str(e)
            )