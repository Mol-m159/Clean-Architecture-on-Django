from dataclasses import dataclass
from typing import Optional
from business.entities.user import User
from business.interfaces.repositories import IUserRepository


@dataclass
class GetUserResult:
    """Результат получения пользователя"""
    success: bool
    user: Optional[User]
    error_message: Optional[str] = None


class GetUserByIdUseCase:
    """
    Use Case: Получение информации о пользователе по ID.
    """
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: int) -> GetUserResult:
        """
        Получить пользователя по ID.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            GetUserResult с информацией о пользователе
        """
        user = self.user_repository.get_by_id(user_id)
        
        if not user:
            return GetUserResult(
                success=False,
                user=None,
                error_message=f"User #{user_id} not found"
            )
        
        return GetUserResult(
            success=True,
            user=user
        )