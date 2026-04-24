from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from .user import User

class HomebrewStatus(Enum):
    """Статусы homebrew контента"""
    DRAFT = "draft"
    MODERATION = "moderation"
    APPROVED = "approved"
    REJECTED = "rejected"
    
    @classmethod
    def from_string(cls, status_str: str) -> 'HomebrewStatus':
        try:
            return cls(status_str.lower())
        except ValueError:
            return cls.DRAFT


class HomebrewType(Enum):
    """Типы homebrew контента"""
    SPELL = "spell"
    ITEM = "item"
    CLASS = "class"
    RACE = "race"
    OTHER = "other"
    
    @classmethod
    def from_string(cls, type_str: str) -> 'HomebrewType':
        try:
            return cls(type_str.lower())
        except ValueError:
            return cls.OTHER


@dataclass
class Homebrew:
    entity_id: int
    author_id: int
    system_id: int
    entity_type: HomebrewType
    created_date: datetime
    status: HomebrewStatus

    
    @property
    def is_approved(self) -> bool:
        """Одобрен ли контент"""
        return self.status == HomebrewStatus.APPROVED
    
    @property
    def is_pending(self) -> bool:
        """Ожидает ли модерации"""
        return self.status == HomebrewStatus.MODERATION
    
    @property
    def can_be_edited(self) -> bool:
        """Можно ли редактировать контент"""
        return self.status in [HomebrewStatus.DRAFT, HomebrewStatus.REJECTED]
    
    def submit_for_moderation(self) -> None:
        """
        Бизнес-правило: отправка на модерацию
        """
        if not self.can_be_edited:
            raise ValueError(f"Cannot submit {self.status.value} content for moderation")
        
        
        self.status = HomebrewStatus.MODERATION
    
    def approve(self, moderator_id: int) -> None:
        """
        Бизнес-правило: одобрение контента модератором
        """
        if self.status != HomebrewStatus.MODERATION:
            raise ValueError(f"Cannot approve content with status {self.status.value}")
        
        self.status = HomebrewStatus.APPROVED
    
    def reject(self, moderator_id: int) -> None:
        """
        Бизнес-правило: отклонение контента с указанием причины
        """
        if self.status != HomebrewStatus.MODERATION:
            raise ValueError(f"Cannot reject content with status {self.status.value}")
        
        
        self.status = HomebrewStatus.REJECTED
    
    def can_be_viewed_by(self, user: 'User') -> bool:
        """
        Бизнес-правило: может ли пользователь просматривать контент
        """
        # Автор всегда может просмотреть
        if user.user_id == self.author_id:
            return True
        
        # Одобренный контент могут просматривать все
        if self.is_approved:
            return True
        
        # Модераторы и админы могут просматривать любой контент
        if user.is_moderator:
            return True
        
        return False