from dataclasses import dataclass
from typing import Optional
from business.interfaces.repositories import IHomebrewRepository


@dataclass
class DeleteHomebrewResult:
    """Результат удаления контента"""
    success: bool
    entity_id: int
    error_message: Optional[str] = None


class DeleteHomebrewUseCase:
    """
    Use Case: Удаление homebrew контента.
    
    Бизнес-правила:
    - Удалять может только автор (проверка в адаптере)
    - Удалить можно контент в любом статусе
    """
    
    def __init__(self, homebrew_repository: IHomebrewRepository):
        self.homebrew_repository = homebrew_repository
    
    def execute(self, entity_id: int) -> DeleteHomebrewResult:
        """
        Удалить контент.
        
        Args:
            entity_id: ID контента
            
        Returns:
            DeleteHomebrewResult с результатом операции
        """
        # Проверяем существование
        homebrew = self.homebrew_repository.get_by_id(entity_id)
        
        if not homebrew:
            return DeleteHomebrewResult(
                success=False,
                entity_id=entity_id,
                error_message=f"Homebrew #{entity_id} not found"
            )
        
        # Удаляем
        deleted = self.homebrew_repository.delete(entity_id)
        
        if not deleted:
            return DeleteHomebrewResult(
                success=False,
                entity_id=entity_id,
                error_message="Failed to delete homebrew"
            )
        
        return DeleteHomebrewResult(
            success=True,
            entity_id=entity_id
        )