from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from business.entities.character import Character
from business.interfaces.repositories import ICharacterRepository
from .can_user_edit_character_use_case import CanUserEditCharacterUseCase

@dataclass
class UpdateCharacterResult:
    """Результат обновления персонажа"""
    success: bool
    character: Optional[Character]
    error_message: Optional[str] = None


class UpdateCharacterUseCase:
    """
    Use Case: Обновление персонажа.
    
    Бизнес-правила:
    - Обновлять может только владелец (проверяется в CanUserEditCharacterUseCase)
    - При обновлении обновляется last_modified_date
    - Добавляется запись в историю изменений
    """
    
    def __init__(
        self, 
        character_repository: ICharacterRepository,
        can_edit_use_case: CanUserEditCharacterUseCase
    ):
        self.character_repository = character_repository
        self.can_edit_use_case = can_edit_use_case
    
    def execute(
        self, 
        character_id: int, 
        user_id: int,
        new_system_id: Optional[int] = None
    ) -> UpdateCharacterResult:
        """
        Обновить персонажа.
        
        Args:
            character_id: ID персонажа
            user_id: ID пользователя, выполняющего обновление
            new_system_id: Новая система (опционально)
            
        Returns:
            UpdateCharacterResult с обновленным персонажем
        """
        # Получаем персонажа
        character = self.character_repository.get_by_id(character_id)
        
        if not character:
            return UpdateCharacterResult(
                success=False,
                character=None,
                error_message=f"Character #{character_id} not found"
            )
        
        # Проверяем права
        can_edit = self.can_edit_use_case.execute(user_id, character)
        if not can_edit:
            return UpdateCharacterResult(
                success=False,
                character=character,
                error_message="User does not have permission to edit this character"
            )
        
        # Обновляем данные
        if new_system_id is not None:
            character.system_id = new_system_id
        
        # Обновляем дату модификации
        character.update_modification_date()
        
        # Сохраняем
        self.character_repository.update(character)
        
        # Добавляем запись в историю
        self.character_repository.add_edit_history(character_id, 'update')
        
        return UpdateCharacterResult(
            success=True,
            character=character
        )