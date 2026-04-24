from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from business.interfaces.readers import IUserStatisticsReader, UserStatsDTO


@dataclass
class UserStatsFilters:
    """Фильтры для статистики пользователей"""
    system_id: Optional[int] = None
    min_characters: Optional[int] = None
    has_homebrew: Optional[bool] = None
    active_only: Optional[bool] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь для читателя"""
        result = {}
        if self.system_id is not None:
            result['system_id'] = self.system_id
        if self.min_characters is not None:
            result['min_characters'] = self.min_characters
        if self.has_homebrew is not None:
            result['has_homebrew'] = self.has_homebrew
        if self.active_only is not None:
            result['active_only'] = self.active_only
        return result


@dataclass
class FilteredUserStatsResult:
    """Результат получения отфильтрованной статистики"""
    success: bool
    data: List[UserStatsDTO]
    total: int
    page: int
    per_page: int
    pages: int
    filters: UserStatsFilters
    error_message: Optional[str] = None


class GetFilteredUserStatsUseCase:
    """
    Use Case: Получение отфильтрованной статистики пользователей.
    
    Фильтры:
    - system_id: только пользователи, активные в указанной системе
    - min_characters: минимум персонажей
    - has_homebrew: только создавшие хотя бы один контент
    - active_only: только активные пользователи
    """
    
    def __init__(self, user_stats_reader: IUserStatisticsReader):
        self.user_stats_reader = user_stats_reader
    
    def execute(
        self,
        filters: UserStatsFilters,
        page: int = 1,
        per_page: int = 20
    ) -> FilteredUserStatsResult:
        try:
            result = self.user_stats_reader.get_filtered_statistics(
                filters.to_dict(), page, per_page
            )
            
            return FilteredUserStatsResult(
                success=True,
                data=result.get('data', []),
                total=result.get('total', 0),
                page=result.get('page', page),
                per_page=result.get('per_page', per_page),
                pages=result.get('pages', 0),
                filters=filters
            )
        except Exception as e:
            return FilteredUserStatsResult(
                success=False,
                data=[],
                total=0,
                page=page,
                per_page=per_page,
                pages=0,
                filters=filters,
                error_message=str(e)
            )