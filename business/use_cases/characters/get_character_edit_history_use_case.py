from dataclasses import dataclass
from typing import List, Optional
from business.value_objects import CharacterEdit
from business.interfaces.repositories import ICharacterRepository


@dataclass
class GetEditHistoryResult:
    """Результат получения истории изменений"""
    success: bool
    character_id: int
    edits: List[CharacterEdit]
    count: int
    error_message: Optional[str] = None


class GetCharacterEditHistoryUseCase:
    """
    Use Case: Получение истории изменений персонажа.
    """
    
    def __init__(self, character_repository: ICharacterRepository):
        self.character_repository = character_repository
    
    def execute(self, character_id: int) -> GetEditHistoryResult:
        """
        Получить историю изменений персонажа.
        
        Args:
            character_id: ID персонажа
            
        Returns:
            GetEditHistoryResult со списком изменений
        """
        # Проверяем существование персонажа
        character = self.character_repository.get_by_id(character_id)
        
        if not character:
            return GetEditHistoryResult(
                success=False,
                character_id=character_id,
                edits=[],
                count=0,
                error_message=f"Character #{character_id} not found"
            )
        
        edits = self.character_repository.get_edit_history(character_id)
        
        return GetEditHistoryResult(
            success=True,
            character_id=character_id,
            edits=edits,
            count=len(edits)
        )