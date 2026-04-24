from dataclasses import dataclass
from typing import Optional
from business.entities.homebrew import Homebrew
from business.entities.user import User, UserRole
from business.interfaces.repositories import IHomebrewRepository


@dataclass
class CanViewResult:
    """Результат проверки прав просмотра"""
    can_view: bool
    reason: str = ""


class CanUserViewHomebrewUseCase:
    """
    Use Case: Проверка, может ли пользователь просматривать контент.
    
    Бизнес-правила (из homebrew.py):
    - Автор всегда может просмотреть
    - Одобренный контент могут просматривать все
    - Модераторы и админы могут просматривать любой контент
    """
    
    def __init__(self, homebrew_repository: IHomebrewRepository):
        self.homebrew_repository = homebrew_repository
    
    def execute(
        self, 
        user_id: int, 
        user_role: str, 
        homebrew: Homebrew
    ) -> bool:
        """
        Проверить, может ли пользователь просматривать контент.
        
        Args:
            user_id: ID пользователя
            user_role: Роль пользователя ('user', 'moderator', 'admin')
            homebrew: Сущность контента
            
        Returns:
            bool: может ли просматривать
        """

        user = User(
            user_id=user_id,
            registration_date=None,  # не нужно для проверки
            last_activity_date=None,  # не нужно для проверки
            role=UserRole.from_string(user_role)
        )
        
        return homebrew.can_be_viewed_by(user)
    
    def execute_by_id(
        self, 
        user_id: int, 
        user_role: str, 
        entity_id: int
    ) -> CanViewResult:
        """
        Проверить по ID контента.
        
        Args:
            user_id: ID пользователя
            user_role: Роль пользователя
            entity_id: ID контента
            
        Returns:
            CanViewResult с результатом проверки
        """
        homebrew = self.homebrew_repository.get_by_id(entity_id)
        
        if not homebrew:
            return CanViewResult(
                can_view=False,
                reason=f"Homebrew #{entity_id} not found"
            )
        
        can_view = self.execute(user_id, user_role, homebrew)
        
        if not can_view:
            return CanViewResult(
                can_view=False,
                reason="User does not have permission to view this content"
            )
        
        return CanViewResult(can_view=True)