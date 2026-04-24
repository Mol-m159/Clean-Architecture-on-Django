from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from business.entities.character import Character
from business.interfaces.repositories import ICharacterRepository


@dataclass
class CreateCharacterResult:
    """Результат создания персонажа"""
    success: bool
    character: Optional[Character]
    error_message: Optional[str] = None


class CreateCharacterUseCase:
    """
    Use Case: Создание нового персонажа.
    
    Бизнес-правила:
    - Пользователь может создавать персонажей
    - При создании автоматически добавляется запись в историю изменений
    """
    
    def __init__(self, character_repository: ICharacterRepository):
        self.character_repository = character_repository
    
    def execute(self, user_id: int, system_id: int) -> CreateCharacterResult:
        """
        Создать нового персонажа.
        
        Args:
            user_id: ID владельца персонажа
            system_id: ID игровой системы
            
        Returns:
            CreateCharacterResult с созданным персонажем
        """
        
        try:
            # Создаем персонажа
            character = self.character_repository.create(user_id, system_id)
            
            # Добавляем запись в историю
            self.character_repository.add_edit_history(
                character.character_id, 
                'creation'
            )
            
            return CreateCharacterResult(
                success=True,
                character=character
            )
            
        except Exception as e:
            return CreateCharacterResult(
                success=False,
                character=None,
                error_message=f"Failed to create character: {str(e)}"
            )