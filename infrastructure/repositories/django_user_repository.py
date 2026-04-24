from typing import Optional
from django.utils import timezone
from core.models import Users
from business.entities.user import User, UserRole
from business.interfaces.repositories import IUserRepository


class DjangoUserRepository(IUserRepository):
    """Реализация репозитория пользователей через Django ORM"""
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        try:
            user_model = Users.objects.get(user_id=user_id)
            return User(
                user_id=user_model.user_id,
                registration_date=user_model.registration_date,
                last_activity_date=user_model.last_activity_date,
                role=UserRole.USER  # роль по умолчанию, т.к. в таблице users нет поля role
            )
        except Users.DoesNotExist:
            return None
    
    def get_role(self, user_id: int) -> Optional[str]:
        """Получить роль пользователя (из сессии или хардкод для демо)"""
        # Временное решение для демонстрации
        # В реальном проекте роль может храниться в отдельной таблице
        admin_users = [40212]  # ID админов из твоего кода
        moderator_users = [40213, 40214]  # ID модераторов
        
        if user_id in admin_users:
            return 'admin'
        elif user_id in moderator_users:
            return 'moderator'
        else:
            return 'user'
    
    def update_last_activity(self, user_id: int) -> None:
        Users.objects.filter(user_id=user_id).update(
            last_activity_date=timezone.now()
        )
    
    def exists(self, user_id: int) -> bool:
        return Users.objects.filter(user_id=user_id).exists()