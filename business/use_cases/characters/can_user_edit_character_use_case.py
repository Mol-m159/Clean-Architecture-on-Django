from dataclasses import dataclass
from business.entities.character import Character
from business.entities.user import User
from business.interfaces.repositories import ICharacterRepository


@dataclass
class CanEditResult:
    """Результат проверки прав"""
    can_edit: bool
    reason: str = ""


class CanUserEditCharacterUseCase:
    """
    Use Case: Проверка, может ли пользователь редактировать персонажа.
    
    Бизнес-правила:
    - Только владелец персонажа может его редактировать
    """
    
    def __init__(self, character_repository: ICharacterRepository):
        self.character_repository = character_repository
    
    def execute(self, user_id: int, character: Character) -> bool:
        """
        Проверить, может ли пользователь редактировать персонажа.
        
        Args:
            user_id: ID пользователя
            character: Сущность персонажа
            
        Returns:
            bool: может ли редактировать
        """
        # Простая проверка: владелец ли пользователь
        return character.can_be_edited_by_id(user_id)
    
    def execute_by_id(self, user_id: int, character_id: int) -> CanEditResult:
        """
        Проверить по ID персонажа.
        
        Args:
            user_id: ID пользователя
            character_id: ID персонажа
            
        Returns:
            CanEditResult с результатом проверки
        """
        character = self.character_repository.get_by_id(character_id)
        
        if not character:
            return CanEditResult(
                can_edit=False,
                reason=f"Character #{character_id} not found"
            )
        
        can_edit = character.can_be_edited_by_id(user_id)
        
        if not can_edit:
            return CanEditResult(
                can_edit=False,
                reason="User is not the owner of this character"
            )
        
        return CanEditResult(can_edit=True)