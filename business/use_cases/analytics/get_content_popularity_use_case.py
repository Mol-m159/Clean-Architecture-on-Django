from dataclasses import dataclass
from typing import List, Optional
from business.interfaces.readers import IAnalyticsReader, ContentPopularityDTO


@dataclass
class ContentPopularityResult:
    """Результат получения рейтинга популярности контента"""
    success: bool
    items: List[ContentPopularityDTO]
    count: int
    entity_type_filter: Optional[str]
    error_message: Optional[str] = None


class GetContentPopularityUseCase:
    """
    Use Case: Получение рейтинга популярности контента.
    
    Ранжирует контент по количеству просмотров.
    Используется для отображения самого популярного контента.
    """
    
    def __init__(self, analytics_reader: IAnalyticsReader):
        self.analytics_reader = analytics_reader
    
    def execute(
        self,
        limit: int = 50,
        entity_type: Optional[str] = None
    ) -> ContentPopularityResult:
        """
        Получить популярный контент.
        
        Args:
            limit: Максимальное количество элементов
            entity_type: Фильтр по типу контента ('spell', 'item', 'class', 'race', 'other')
        """
        try:
            items = self.analytics_reader.get_content_popularity(limit, entity_type)
            
            return ContentPopularityResult(
                success=True,
                items=items,
                count=len(items),
                entity_type_filter=entity_type
            )
        except Exception as e:
            return ContentPopularityResult(
                success=False,
                items=[],
                count=0,
                entity_type_filter=entity_type,
                error_message=str(e)
            )