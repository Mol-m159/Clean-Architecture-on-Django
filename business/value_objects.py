from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True) 
class GameSystem:
    """Справочная информация об игровой системе """
    system_id: int
    created_date: datetime
    is_active: bool

@dataclass(frozen=True)
class CharacterEdit:
    """Историческое событие изменения персонажа"""
    edit_id: int
    character_id: int
    edit_date: datetime
    edit_type: str

@dataclass(frozen=True)
class HomebrewEdit:
    """Историческое событие изменения контента"""
    edit_id: int
    entity_id: int
    edit_date: datetime
    version_number: int

@dataclass(frozen=True)
class HomebrewModeration:
    """Событие модерации"""
    moderation_id: int
    moderator_id: int
    entity_id: int
    moderation_date: datetime
    old_status: str
    new_status: str

@dataclass(frozen=True)
class EntityView:
    """Событие просмотра"""
    view_id: int
    user_id: int
    entity_id: int
    system_id: int
    view_date: datetime

@dataclass(frozen=True)
class UserSession:
    """Сессия пользователя"""
    session_id: int
    user_id: int
    login_date: datetime
    logout_date: Optional[datetime] = None
    
    @property
    def duration_minutes(self) -> Optional[float]:
        if self.logout_date:
            delta = self.logout_date - self.login_date
            return delta.total_seconds() / 60
        return None
    
    @property
    def is_active(self) -> bool:
        return self.logout_date is None

@dataclass(frozen=True)
class Notification:
    """Уведомление """
    notification_id: int
    user_id: int
    created_date: datetime
    notification_type: str

@dataclass(frozen=True)
class SystemEvent:
    """Системное событие"""
    event_id: int
    event_date: datetime
    event_type: str
    user_id: Optional[int] = None
    system_id: Optional[int] = None
