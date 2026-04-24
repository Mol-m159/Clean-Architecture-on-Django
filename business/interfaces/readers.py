
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from dataclasses import dataclass
from business.value_objects import (
    GameSystem,
    CharacterEdit,
    HomebrewEdit,
    HomebrewModeration,
    EntityView,
    UserSession,
    Notification,
    SystemEvent
)

@dataclass
class UserStatsDTO:
    """DTO для статистики пользователя"""
    user_id: int
    system_id: int
    character_count: int
    homebrew_count: int
    last_activity: Optional[datetime]


@dataclass
class CharacterStatsDTO:
    """DTO для статистики персонажей"""
    system_id: int
    character_count: int
    created_today: int
    avg_age_days: float


@dataclass
class HomebrewStatsDTO:
    """DTO для статистики контента"""
    total_count: int
    by_status: Dict[str, int]      # {'draft': 5, 'moderation': 3, ...}
    by_type: Dict[str, int]        # {'spell': 10, 'item': 5, ...}
    created_today: int


@dataclass
class SessionStatsDTO:
    """DTO для статистики сессии"""
    session_id: int
    user_id: int
    login_date: datetime
    logout_date: Optional[datetime]
    session_duration_seconds: Optional[int]
    session_duration_minutes: Optional[int]
    characters_edited: int
    entities_viewed: int
    session_status: str  # 'active' or 'completed'


@dataclass
class DashboardStatsDTO:
    """DTO для дашборда администратора"""
    total_users: int
    total_characters: int
    total_homebrew: int
    active_sessions: int
    new_users_today: int
    new_characters_today: int
    new_homebrew_today: int


@dataclass
class RecentActivityDTO:
    """DTO для последней активности"""
    user_id: int
    user_type: str
    login_date: datetime
    logout_date: Optional[datetime]



@dataclass
class UserActivityReportDTO:
    """DTO для отчета по активности пользователей"""
    user_id: int
    total_sessions: int
    total_duration_minutes: float
    characters_created: int
    homebrew_created: int
    last_active_date: Optional[datetime]


@dataclass
class ContentPopularityDTO:
    """DTO для популярности контента"""
    entity_id: int
    entity_type: str
    author_id: int
    view_count: int
    days_since_creation: int


@dataclass
class UserEngagementDTO:
    """DTO для вовлеченности пользователей"""
    user_id: int
    total_actions: int
    unique_systems: int
    engagement_score: float  # 0-100


@dataclass
class DailyStatsDTO:
    """DTO для дневной статистики"""
    date: date
    new_users: int
    new_characters: int
    new_homebrew: int
    active_sessions: int
    total_views: int

class IGameSystemReader(ABC):
    """Читатель справочной информации об игровых системах."""
    
    @abstractmethod
    def get_active_systems(self) -> List[GameSystem]:
        """Получить все активные игровые системы."""
        pass
    
    @abstractmethod
    def get_by_id(self, system_id: int) -> Optional[GameSystem]:
        """Получить систему по ID."""
        pass

    @abstractmethod
    def get_system_statistics(self, system_id: int) -> dict:
        """
        Получить статистику по системе.
        Возвращает словарь с полями:
        - total_characters: int
        - total_homebrew: int
        - total_views: int
        - active_users: int
        """
        pass


class ICharacterEditReader(ABC):
    """Читатель истории изменений персонажей."""
    
    @abstractmethod
    def get_by_character(self, character_id: int, limit: int = 50) -> List[CharacterEdit]:
        """Получить историю изменений персонажа."""
        pass


class IHomebrewEditReader(ABC):
    """Читатель истории изменений homebrew контента."""
    
    @abstractmethod
    def get_by_entity(self, entity_id: int) -> List[HomebrewEdit]:
        """Получить все версии контента."""
        pass
    
    @abstractmethod
    def get_latest_version(self, entity_id: int) -> Optional[HomebrewEdit]:
        """Получить последнюю версию контента."""
        pass


class IHomebrewModerationReader(ABC):
    """Читатель истории модерации."""
    
    @abstractmethod
    def get_by_entity(self, entity_id: int) -> List[HomebrewModeration]:
        """Получить историю модерации контента."""
        pass


class IEntityViewReader(ABC):
    """Читатель статистики просмотров."""
    
    @abstractmethod
    def get_view_count(self, entity_id: int) -> int:
        """Получить количество просмотров сущности."""
        pass
    
    @abstractmethod
    def get_views_by_user(self, user_id: int, limit: int = 100) -> List[EntityView]:
        """Получить историю просмотров пользователя."""
        pass
    
    @abstractmethod
    def get_views_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[EntityView]:
        """Получить просмотры за период."""
        pass


class ISessionReader(ABC):
    """Читатель сессий пользователей."""
    
    @abstractmethod
    def get_by_user(self, user_id: int, limit: int = 50) -> List[UserSession]:
        """Получить сессии пользователя."""
        pass
    
    @abstractmethod
    def get_active_sessions(self) -> List[UserSession]:
        """Получить все активные сессии."""
        pass
    
    @abstractmethod
    def get_session_statistics(self) -> dict:
        """
        Получить статистику по сессиям.
        Возвращает словарь с агрегированными данными.
        """
        pass


class INotificationReader(ABC):
    """Читатель уведомлений."""
    
    @abstractmethod
    def get_by_user(self, user_id: int, unread_only: bool = False) -> List[Notification]:
        """Получить уведомления пользователя."""
        pass


class ISystemEventReader(ABC):
    """Читатель системных событий."""
    
    @abstractmethod
    def get_by_type(self, event_type: str, limit: int = 100) -> List[SystemEvent]:
        """Получить события по типу."""
        pass
    
    @abstractmethod
    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[SystemEvent]:
        """Получить события за период."""
        pass


class IUserStatisticsReader(ABC):
    """Читатель статистики пользователей"""
    
    @abstractmethod
    def get_total_count(self) -> int:
        """Общее количество пользователей"""
        pass
    
    @abstractmethod
    def get_new_count_since(self, date: datetime) -> int:
        """Количество новых пользователей с указанной даты"""
        pass
    
    @abstractmethod
    def get_all_statistics(self) -> List[UserStatsDTO]:
        """Получить статистику по всем пользователям"""
        pass
    
    @abstractmethod
    def get_statistics_paginated(
        self, 
        page: int, 
        per_page: int
    ) -> Dict[str, Any]:
        """
        Получить статистику пользователей с пагинацией.
        Возвращает: {'data': List[UserStatsDTO], 'total': int, 'page': int, 'pages': int}
        """
        pass
    
    @abstractmethod
    def get_filtered_statistics(
        self, 
        filters: Dict[str, Any],
        page: int,
        per_page: int
    ) -> Dict[str, Any]:
        """
        Получить отфильтрованную статистику пользователей.
        Filters может содержать: system_id, min_characters, has_homebrew, active_only
        """
        pass

class ICharacterStatisticsReader(ABC):
    """Читатель статистики персонажей"""
    
    @abstractmethod
    def get_total_count(self) -> int:
        """Общее количество персонажей"""
        pass
    
    @abstractmethod
    def get_new_count_since(self, date: datetime) -> int:
        """Количество новых персонажей с указанной даты"""
        pass
    
    @abstractmethod
    def get_statistics_by_system(self) -> List[CharacterStatsDTO]:
        """Статистика по персонажам в разрезе игровых систем"""
        pass


class IHomebrewStatisticsReader(ABC):
    """Читатель статистики homebrew контента"""
    
    @abstractmethod
    def get_total_count(self) -> int:
        """Общее количество контента"""
        pass
    
    @abstractmethod
    def get_new_count_since(self, date: datetime) -> int:
        """Количество нового контента с указанной даты"""
        pass
    
    @abstractmethod
    def get_statistics(self) -> HomebrewStatsDTO:
        """Полная статистика по контенту (по статусам и типам)"""
        pass
    
    @abstractmethod
    def get_by_status(self, status: str) -> List[Any]:
        """Получить контент по статусу"""
        pass


class ISessionStatisticsReader(ABC):
    """Читатель статистики сессий"""
    
    @abstractmethod
    def get_active_count(self) -> int:
        """Количество активных сессий"""
        pass
    
    @abstractmethod
    def get_all_statistics(self) -> List[SessionStatsDTO]:
        """Получить статистику по всем сессиям"""
        pass
    
    @abstractmethod
    def get_statistics_paginated(
        self, 
        page: int, 
        per_page: int
    ) -> Dict[str, Any]:
        """Получить статистику сессий с пагинацией"""
        pass
    
    @abstractmethod
    def get_filtered_statistics(
        self, 
        filters: Dict[str, Any],
        page: int,
        per_page: int
    ) -> Dict[str, Any]:
        """
        Получить отфильтрованную статистику сессий.
        Filters может содержать: date_from, date_to, active_only
        """
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: int, limit: int = 50) -> List[SessionStatsDTO]:
        """Получить сессии конкретного пользователя"""
        pass
    
    @abstractmethod
    def terminate_session(self, session_id: int) -> bool:
        """Принудительно завершить сессию (установить logout_date)"""
        pass


class ISystemDashboardReader(ABC):
    """Читатель для системного дашборда"""
    
    @abstractmethod
    def get_dashboard_stats(self) -> DashboardStatsDTO:
        """Получить все основные метрики для дашборда"""
        pass
    
    @abstractmethod
    def get_recent_activities(self, limit: int = 10) -> List[RecentActivityDTO]:
        """Получить последние активности в системе"""
        pass
    
    @abstractmethod
    def get_system_health(self) -> Dict[str, Any]:
        """Получить информацию о состоянии системы"""
        pass

class IAnalyticsReader(ABC):
    """Читатель для аналитики и отчетов"""
    
    # Общая аналитика
    @abstractmethod
    def get_user_activity_report(
        self, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[UserActivityReportDTO]:
        """Получить отчет по активности пользователей."""
        pass
    
    @abstractmethod
    def get_content_popularity(
        self,
        limit: int = 50,
        entity_type: Optional[str] = None
    ) -> List[ContentPopularityDTO]:
        """Получить рейтинг популярности контента (по просмотрам)."""
        pass
    
    @abstractmethod
    def get_user_engagement(
        self,
        limit: int = 100
    ) -> List[UserEngagementDTO]:
        """Получить метрики вовлеченности пользователей."""
        pass
    
    # Временные отчеты
    @abstractmethod
    def get_daily_statistics(self, target_date: date) -> DailyStatsDTO:
        """Получить статистику за конкретный день."""
        pass
    
    @abstractmethod
    def get_weekly_statistics(self, week_start: date) -> Dict[str, Any]:
        """Получить статистику за неделю."""
        pass
    
    @abstractmethod
    def get_monthly_statistics(self, year: int, month: int) -> Dict[str, Any]:
        """Получить статистику за месяц."""
        pass
    
    @abstractmethod
    def get_date_range_statistics(
        self,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Получить статистику за произвольный период."""
        pass