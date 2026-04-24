from dataclasses import dataclass
from typing import List, Optional
from business.entities.character import Character
from business.interfaces.repositories import ICharacterRepository


@dataclass
class GetUserCharactersResult:
    """Результат получения списка персонажей"""
    success: bool
    characters: List[Character]
    count: int
    error_message: Optional[str] = None


class GetUserCharactersListUseCase:
    """
    Use Case: Получение списка всех персонажей пользователя.
    """
    
    def __init__(self, character_repository: ICharacterRepository):
        self.character_repository = character_repository
    
    def execute(self, user_id: int) -> GetUserCharactersResult:
        """
        Получить всех персонажей пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            GetUserCharactersResult со списком персонажей
        """
        characters = self.character_repository.get_by_user(user_id)
        
        return GetUserCharactersResult(
            success=True,
            characters=characters,
            count=len(characters)
        )