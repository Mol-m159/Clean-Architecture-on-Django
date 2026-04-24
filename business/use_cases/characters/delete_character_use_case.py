from dataclasses import dataclass
from typing import Optional
from business.entities.character import Character
from business.interfaces.repositories import ICharacterRepository
from .can_user_edit_character_use_case import CanUserEditCharacterUseCase


@dataclass
class DeleteCharacterResult:
    """Результат удаления персонажа"""
    success: bool
    character_id: int
    error_message: Optional[str] = None


class DeleteCharacterUseCase:
    """
    Use Case: Удаление персонажа.
    
    Бизнес-правила:
    - Удалять может только владелец (проверяется в CanUserEditCharacterUseCase)
    """
    
    def __init__(
        self, 
        character_repository: ICharacterRepository,
        can_edit_use_case: CanUserEditCharacterUseCase
    ):
        self.character_repository = character_repository
        self.can_edit_use_case = can_edit_use_case
    
    def execute(self, character_id: int, user_id: int) -> DeleteCharacterResult:
        """
        Удалить персонажа.
        
        Args:
            character_id: ID персонажа
            user_id: ID пользователя, выполняющего удаление
            
        Returns:
            DeleteCharacterResult с результатом операции
        """
        # Получаем персонажа
        character = self.character_repository.get_by_id(character_id)
        
        if not character:
            return DeleteCharacterResult(
                success=False,
                character_id=character_id,
                error_message=f"Character #{character_id} not found"
            )
        
        # Проверяем права
        can_edit = self.can_edit_use_case.execute(user_id, character)
        if not can_edit:
            return DeleteCharacterResult(
                success=False,
                character_id=character_id,
                error_message="User does not have permission to delete this character"
            )
        
        # Удаляем
        deleted = self.character_repository.delete(character_id)
        
        if not deleted:
            return DeleteCharacterResult(
                success=False,
                character_id=character_id,
                error_message="Failed to delete character"
            )
        
        return DeleteCharacterResult(
            success=True,
            character_id=character_id
        )