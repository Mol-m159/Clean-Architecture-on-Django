
from dataclasses import dataclass
from typing import List, Optional
from business.value_objects import Notification
from business.interfaces.readers import INotificationReader


@dataclass
class UserNotificationsResult:
    """Результат получения уведомлений пользователя"""
    success: bool
    user_id: int
    notifications: List[Notification]
    count: int
    error_message: Optional[str] = None


class GetUserNotificationsUseCase:
    """
    Use Case: Получение уведомлений пользователя.
    
    Уведомления — это Value Objects, только для чтения.
    """
    
    def __init__(self, notification_reader: INotificationReader):
        self.notification_reader = notification_reader
    
    def execute(self, user_id: int, unread_only: bool = False) -> UserNotificationsResult:
        """
        Получить уведомления пользователя.
        
        Args:
            user_id: ID пользователя
            unread_only: Только непрочитанные (если поддерживается)
        """
        try:
            notifications = self.notification_reader.get_by_user(user_id, unread_only)
            
            return UserNotificationsResult(
                success=True,
                user_id=user_id,
                notifications=notifications,
                count=len(notifications)
            )
        except Exception as e:
            return UserNotificationsResult(
                success=False,
                user_id=user_id,
                notifications=[],
                count=0,
                error_message=str(e)
            )