from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from business.entities.user import User, UserRole
from business.interfaces.repositories import IUserRepository


@dataclass
class LoginResult:
    """Результат входа"""
    success: bool
    user: Optional[User]
    role: UserRole  # роль, выбранная пользователем
    error_message: Optional[str] = None


class LoginUseCase:
    """
    Use Case: Вход пользователя в систему.
    
    Проверяет существование пользователя, обновляет активность.
    Управление сессией — ответственность адаптера (Django).
    """
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: int, role_str: str) -> LoginResult:
        """
        Выполнить вход пользователя.
        
        Args:
            user_id: ID пользователя
            role_str: Роль пользователя из интерфейса ('user', 'moderator', 'admin')
            
        Returns:
            LoginResult с информацией о пользователе и его роли
        """
        # Проверяем существование пользователя
        user = self.user_repository.get_by_id(user_id)
        
        if not user:
            return LoginResult(
                success=False,
                user=None,
                role=UserRole.USER,
                error_message=f"User #{user_id} not found"
            )
        
        # Преобразуем строку роли в Enum
        try:
            role = UserRole.from_string(role_str)
        except ValueError:
            role = UserRole.USER
        
        # Обновляем активность пользователя
        user.update_last_activity()
        self.user_repository.update_last_activity(user_id)
        
        return LoginResult(
            success=True,
            user=user,
            role=role
        )