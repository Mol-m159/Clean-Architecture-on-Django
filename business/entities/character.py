from dataclasses import dataclass
from datetime import datetime
from .user import User


@dataclass
class Character:
    character_id: int
    user_id: int
    system_id: int
    created_date: datetime
    last_modified_date: datetime
    
    @property
    def age_days(self) -> int:
        """Возраст персонажа в днях"""
        delta = datetime.now() - self.created_date
        return delta.days
    
    def can_be_edited_by(self, user: 'User') -> bool:
        """
        Бизнес-правило: может ли пользователь редактировать этого персонажа?
        """
        # Только владелец или администратор
        return user.user_id == self.user_id
    
    def can_be_edited_by_id(self, user_id: int) -> bool:
        """Может ли пользователь с данным ID редактировать персонажа?"""
        return user_id == self.user_id

    def update_modification_date(self) -> None:
        """Обновляет дату последнего изменения"""
        self.last_modified_date = datetime.now()