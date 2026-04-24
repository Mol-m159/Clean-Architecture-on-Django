from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class UserRole(Enum):
    """Роли пользователей в системе"""
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    
    @classmethod
    def from_string(cls, role_str: str) -> 'UserRole':
        """Преобразует строку из базы в Enum"""
        try:
            return cls(role_str.lower())
        except ValueError:
            return cls.USER


@dataclass
class User:
    user_id: int
    registration_date: datetime
    last_activity_date: datetime
    role: UserRole = UserRole.USER  # роль по умолчанию
    
    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
    
    @property
    def is_moderator(self) -> bool:
        return self.role in [UserRole.MODERATOR, UserRole.ADMIN]
    
    @property
    def days_since_registration(self) -> int:
        delta = datetime.now() - self.registration_date
        return delta.days
    
    
    def can_moderate(self) -> bool:
        """Может ли пользователь модерировать контент?"""
        return self.is_moderator
    
    def update_last_activity(self) -> None:
        """Обновляет время последней активности"""
        self.last_activity_date = datetime.now()
    
    def __str__(self) -> str:
        return f"User #{self.user_id} ({self.role.value})"