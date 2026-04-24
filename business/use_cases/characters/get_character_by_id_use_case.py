from dataclasses import dataclass
from typing import Optional
from business.entities.character import Character
from business.interfaces.repositories import ICharacterRepository


@dataclass
class GetCharacterResult:
    """Результат получения персонажа"""
    success: bool
    character: Optional[Character]
    error_message: Optional[str] = None


class GetCharacterByIdUseCase:
    """
    Use Case: Получение персонажа по ID.
    """
    
    def __init__(self, character_repository: ICharacterRepository):
        self.character_repository = character_repository
    
    def execute(self, character_id: int) -> GetCharacterResult:
        """
        Получить персонажа по ID.
        
        Args:
            character_id: ID персонажа
            
        Returns:
            GetCharacterResult с информацией о персонаже
        """
        character = self.character_repository.get_by_id(character_id)
        
        if not character:
            return GetCharacterResult(
                success=False,
                character=None,
                error_message=f"Character #{character_id} not found"
            )
        
        return GetCharacterResult(
            success=True,
            character=character
        )