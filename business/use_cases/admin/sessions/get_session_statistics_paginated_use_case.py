from dataclasses import dataclass
from typing import List, Optional
from business.interfaces.readers import ISessionStatisticsReader, SessionStatsDTO


@dataclass
class PaginatedSessionStatsResult:
    """Результат получения пагинированной статистики сессий"""
    success: bool
    data: List[SessionStatsDTO]
    total: int
    page: int
    per_page: int
    pages: int
    error_message: Optional[str] = None


class GetSessionStatisticsPaginatedUseCase:
    """
    Use Case: Получение статистики сессий с пагинацией.
    
    Используется для отображения больших объемов данных.
    """
    
    def __init__(self, session_stats_reader: ISessionStatisticsReader):
        self.session_stats_reader = session_stats_reader
    
    def execute(self, page: int = 1, per_page: int = 20) -> PaginatedSessionStatsResult:
        try:
            result = self.session_stats_reader.get_statistics_paginated(page, per_page)
            
            return PaginatedSessionStatsResult(
                success=True,
                data=result.get('data', []),
                total=result.get('total', 0),
                page=result.get('page', page),
                per_page=result.get('per_page', per_page),
                pages=result.get('pages', 0)
            )
        except Exception as e:
            return PaginatedSessionStatsResult(
                success=False,
                data=[],
                total=0,
                page=page,
                per_page=per_page,
                pages=0,
                error_message=str(e)
            )