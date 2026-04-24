from dataclasses import dataclass
from typing import Optional
from business.interfaces.repositories import IUserRepository


@dataclass
class LogoutResult:
    """Результат выхода"""
    success: bool
    user_id: int
    error_message: Optional[str] = None


class LogoutUseCase:
    """
    Use Case: Выход пользователя из системы.
    
    Use case ничего не знает о сессиях — только фиксирует факт выхода.
    Управление сессией и очистка данных — ответственность адаптера.
    """
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: int) -> LogoutResult:
        """
        Зафиксировать выход пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            LogoutResult с информацией о результате
        """
        # Проверяем существование пользователя
        if not self.user_repository.exists(user_id):
            return LogoutResult(
                success=False,
                user_id=user_id,
                error_message=f"User #{user_id} not found"
            )
        
        
        return LogoutResult(
            success=True,
            user_id=user_id
        )