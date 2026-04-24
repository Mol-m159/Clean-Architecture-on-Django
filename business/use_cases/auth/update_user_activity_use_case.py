from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from business.interfaces.repositories import IUserRepository


@dataclass
class UpdateActivityResult:
    """Результат обновления активности"""
    success: bool
    user_id: int
    last_activity_date: Optional[datetime]
    error_message: Optional[str] = None


class UpdateUserActivityUseCase:
    """
    Use Case: Обновление времени последней активности пользователя.
    
    Используется для отслеживания активности пользователя в системе.
    """
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: int) -> UpdateActivityResult:
        """
        Обновить дату последней активности пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            UpdateActivityResult с информацией о результате
        """
        # Проверяем существование пользователя
        if not self.user_repository.exists(user_id):
            return UpdateActivityResult(
                success=False,
                user_id=user_id,
                last_activity_date=None,
                error_message=f"User #{user_id} not found"
            )
        
        # Обновляем активность
        self.user_repository.update_last_activity(user_id)
        
        # Получаем обновленного пользователя для возврата даты
        user = self.user_repository.get_by_id(user_id)
        
        return UpdateActivityResult(
            success=True,
            user_id=user_id,
            last_activity_date=user.last_activity_date if user else None
        )