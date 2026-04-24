from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from business.interfaces.readers import IUserStatisticsReader, UserStatsDTO


@dataclass
class PaginatedUserStatsResult:
    """Результат получения пагинированной статистики пользователей"""
    success: bool
    data: List[UserStatsDTO]
    total: int
    page: int
    per_page: int
    pages: int
    error_message: Optional[str] = None


class GetUserStatisticsPaginatedUseCase:
    """
    Use Case: Получение статистики пользователей с пагинацией.
    
    Используется для отображения больших объемов данных.
    """
    
    def __init__(self, user_stats_reader: IUserStatisticsReader):
        self.user_stats_reader = user_stats_reader
    
    def execute(self, page: int = 1, per_page: int = 20) -> PaginatedUserStatsResult:
        try:
            result = self.user_stats_reader.get_statistics_paginated(page, per_page)
            
            return PaginatedUserStatsResult(
                success=True,
                data=result.get('data', []),
                total=result.get('total', 0),
                page=result.get('page', page),
                per_page=result.get('per_page', per_page),
                pages=result.get('pages', 0)
            )
        except Exception as e:
            return PaginatedUserStatsResult(
                success=False,
                data=[],
                total=0,
                page=page,
                per_page=per_page,
                pages=0,
                error_message=str(e)
            )