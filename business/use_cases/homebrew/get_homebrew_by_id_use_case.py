from dataclasses import dataclass
from typing import Optional
from business.entities.homebrew import Homebrew
from business.interfaces.repositories import IHomebrewRepository


@dataclass
class GetHomebrewResult:
    """Результат получения контента"""
    success: bool
    homebrew: Optional[Homebrew]
    error_message: Optional[str] = None


class GetHomebrewByIdUseCase:
    """
    Use Case: Получение homebrew контента по ID.
    """
    
    def __init__(self, homebrew_repository: IHomebrewRepository):
        self.homebrew_repository = homebrew_repository
    
    def execute(self, entity_id: int) -> GetHomebrewResult:
        """
        Получить контент по ID.
        
        Args:
            entity_id: ID контента
            
        Returns:
            GetHomebrewResult с информацией о контенте
        """
        homebrew = self.homebrew_repository.get_by_id(entity_id)
        
        if not homebrew:
            return GetHomebrewResult(
                success=False,
                homebrew=None,
                error_message=f"Homebrew #{entity_id} not found"
            )
        
        return GetHomebrewResult(
            success=True,
            homebrew=homebrew
        )