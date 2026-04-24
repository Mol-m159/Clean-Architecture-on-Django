from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime
from business.interfaces.readers import ISessionStatisticsReader, SessionStatsDTO


@dataclass
class SessionStatsFilters:
    """Фильтры для статистики сессий"""
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    active_only: Optional[bool] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь для читателя"""
        result = {}
        if self.date_from is not None:
            result['date_from'] = self.date_from
        if self.date_to is not None:
            result['date_to'] = self.date_to
        if self.active_only is not None:
            result['active_only'] = self.active_only
        return result


@dataclass
class FilteredSessionStatsResult:
    """Результат получения отфильтрованной статистики сессий"""
    success: bool
    data: List[SessionStatsDTO]
    total: int
    page: int
    per_page: int
    pages: int
    filters: SessionStatsFilters
    error_message: Optional[str] = None


class GetFilteredSessionStatsUseCase:
    """
    Use Case: Получение отфильтрованной статистики сессий.
    
    Фильтры:
    - date_from: только сессии после указанной даты
    - date_to: только сессии до указанной даты
    - active_only: только активные сессии
    """
    
    def __init__(self, session_stats_reader: ISessionStatisticsReader):
        self.session_stats_reader = session_stats_reader
    
    def execute(
        self,
        filters: SessionStatsFilters,
        page: int = 1,
        per_page: int = 20
    ) -> FilteredSessionStatsResult:
        try:
            result = self.session_stats_reader.get_filtered_statistics(
                filters.to_dict(), page, per_page
            )
            
            return FilteredSessionStatsResult(
                success=True,
                data=result.get('data', []),
                total=result.get('total', 0),
                page=result.get('page', page),
                per_page=result.get('per_page', per_page),
                pages=result.get('pages', 0),
                filters=filters
            )
        except Exception as e:
            return FilteredSessionStatsResult(
                success=False,
                data=[],
                total=0,
                page=page,
                per_page=per_page,
                pages=0,
                filters=filters,
                error_message=str(e)
            )