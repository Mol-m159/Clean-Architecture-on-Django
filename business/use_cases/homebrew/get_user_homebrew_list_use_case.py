from dataclasses import dataclass
from typing import List, Optional
from business.entities.homebrew import Homebrew
from business.interfaces.repositories import IHomebrewRepository


@dataclass
class GetUserHomebrewResult:
    """Результат получения списка контента пользователя"""
    success: bool
    homebrew_items: List[Homebrew]
    count: int
    error_message: Optional[str] = None


class GetUserHomebrewListUseCase:
    """
    Use Case: Получение списка всего homebrew контента пользователя.
    """
    
    def __init__(self, homebrew_repository: IHomebrewRepository):
        self.homebrew_repository = homebrew_repository
    
    def execute(self, author_id: int) -> GetUserHomebrewResult:
        """
        Получить весь контент автора.
        
        Args:
            author_id: ID автора
            
        Returns:
            GetUserHomebrewResult со списком контента
        """
        items = self.homebrew_repository.get_by_author(author_id)
        
        return GetUserHomebrewResult(
            success=True,
            homebrew_items=items,
            count=len(items)
        )