"""
DI Container - Dependency Injection контейнер для чистой архитектуры.

Здесь собираются все зависимости:
- Репозитории (работа с данными)
- Читатели (сложные запросы)
- Use Cases (бизнес-логика)

Использование в views:
    from infrastructure.di_config import container
    result = container.login_uc.execute(user_id, role)
"""

from typing import Optional
from infrastructure.services.session_service import DjangoSessionService
# ========== ИМПОРТЫ ИЗ BUSINESS СЛОЯ ==========
# Auth Use Cases
from business.use_cases.auth import (
    LoginUseCase,
    LogoutUseCase,
    GetUserByIdUseCase,
    UpdateUserActivityUseCase,
)

# Characters Use Cases
from business.use_cases.characters import (
    GetCharacterByIdUseCase,
    GetUserCharactersListUseCase,
    CreateCharacterUseCase,
    UpdateCharacterUseCase,
    DeleteCharacterUseCase,
    CanUserEditCharacterUseCase,
    GetCharacterEditHistoryUseCase,
)

# Homebrew Use Cases
from business.use_cases.homebrew import (
    GetHomebrewByIdUseCase,
    GetUserHomebrewListUseCase,
    CreateHomebrewUseCase,
    UpdateHomebrewUseCase,
    DeleteHomebrewUseCase,
    SubmitHomebrewForModerationUseCase,
    GetHomebrewModerationStatusUseCase,
    CreateNewVersionUseCase,
    CanUserViewHomebrewUseCase,
    RecordHomebrewViewUseCase,
    GetHomebrewViewCountUseCase,
)

# Moderation Use Cases
from business.use_cases.moderation import (
    GetModerationQueueUseCase,
    GetModerationQueueCountUseCase,
    GetModerationQueuePriorityUseCase,
    ApproveHomebrewUseCase,
    RejectHomebrewUseCase,
    GetModerationHistoryUseCase,
    GetModeratorStatisticsUseCase,
)

# Admin Use Cases - Users
from business.use_cases.admin.users import (
    GetTotalUsersCountUseCase,
    GetUserStatisticsPaginatedUseCase,
    GetFilteredUserStatsUseCase,
)

# Admin Use Cases - Characters
from business.use_cases.admin.characters import (
    GetTotalCharactersCountUseCase,
    GetCharactersStatisticsUseCase,
)

# Admin Use Cases - Homebrew
from business.use_cases.admin.homebrew import (
    GetTotalHomebrewCountUseCase,
    GetHomebrewStatisticsUseCase,
)

# Admin Use Cases - Sessions
from business.use_cases.admin.sessions import (
    GetActiveSessionsCountUseCase,
    GetSessionStatisticsPaginatedUseCase,
    GetFilteredSessionStatsUseCase,
    GetUserSessionsUseCase,
    TerminateSessionUseCase,
)

# Admin Use Cases - Dashboard
from business.use_cases.admin.dashboard import (
    GetSystemDashboardStatsUseCase,
    GetRecentActivitiesUseCase,
    GetSystemHealthUseCase,
)

# Systems Use Cases
from business.use_cases.systems import (
    GetActiveSystemsListUseCase,
    GetSystemByIdUseCase,
    GetSystemStatisticsUseCase,
)

# Notifications Use Cases
from business.use_cases.notifications import (
    GetUserNotificationsUseCase,
)

# Analytics Use Cases
from business.use_cases.analytics import (
    GetDailyStatisticsUseCase,
    GetWeeklyStatisticsUseCase,
    GetMonthlyStatisticsUseCase,
    GetDateRangeStatisticsUseCase,
    GetUserActivityReportUseCase,
    GetUserEngagementUseCase,
    GetContentPopularityUseCase,
)

# ========== ИМПОРТЫ ИЗ INFRASTRUCTURE СЛОЯ ==========
# Репозитории
from infrastructure.repositories import (
    DjangoUserRepository,
    DjangoCharacterRepository,
    DjangoHomebrewRepository,
    DjangoModerationRepository,
)

# Читатели
from infrastructure.readers import (
    DjangoUserStatisticsReader,
    DjangoCharacterStatisticsReader,
    DjangoHomebrewStatisticsReader,
    DjangoSessionStatisticsReader,
    DjangoSystemDashboardReader,
    DjangoCharacterEditReader,
    DjangoHomebrewEditReader,
    DjangoHomebrewModerationReader,
    DjangoAnalyticsReader,
    DjangoGameSystemReader,     
    DjangoNotificationReader,
)


class Container:
    """
    DI контейнер, содержащий все зависимости.
    
    Инициализируется один раз при старте приложения.
    Доступ к use cases через атрибуты:
        container.login_uc
        container.create_character_uc
        container.get_moderation_queue_uc
        и т.д.
    """
    
    def __init__(self):
        # ========== РЕПОЗИТОРИИ (нижний уровень) ==========
        self.user_repository = DjangoUserRepository()
        self.character_repository = DjangoCharacterRepository()
        self.homebrew_repository = DjangoHomebrewRepository()
        self.moderation_repository = DjangoModerationRepository()
        
        # ========== ЧИТАТЕЛИ (нижний уровень) ==========
        self.user_stats_reader = DjangoUserStatisticsReader()
        self.character_stats_reader = DjangoCharacterStatisticsReader()
        self.homebrew_stats_reader = DjangoHomebrewStatisticsReader()
        self.session_stats_reader = DjangoSessionStatisticsReader()
        self.dashboard_reader = DjangoSystemDashboardReader()
        self.character_edit_reader = DjangoCharacterEditReader()
        self.homebrew_edit_reader = DjangoHomebrewEditReader()
        self.moderation_reader = DjangoHomebrewModerationReader()
        self.analytics_reader = DjangoAnalyticsReader()
        self.game_system_reader = DjangoGameSystemReader()
        self.notification_reader = DjangoNotificationReader()
        
        # ========== AUTH USE CASES ==========
        self.login_uc = LoginUseCase(self.user_repository)
        self.logout_uc = LogoutUseCase(self.user_repository)
        self.get_user_uc = GetUserByIdUseCase(self.user_repository)
        self.update_activity_uc = UpdateUserActivityUseCase(self.user_repository)
        
        # ========== CHARACTER USE CASES ==========
        self.get_character_uc = GetCharacterByIdUseCase(self.character_repository)
        self.get_user_characters_uc = GetUserCharactersListUseCase(self.character_repository)
        self.create_character_uc = CreateCharacterUseCase(self.character_repository)
        self.can_edit_character_uc = CanUserEditCharacterUseCase(self.character_repository)
        self.update_character_uc = UpdateCharacterUseCase(
            self.character_repository,
            self.can_edit_character_uc
        )
        self.delete_character_uc = DeleteCharacterUseCase(
            self.character_repository,
            self.can_edit_character_uc
        )
        self.get_character_edits_uc = GetCharacterEditHistoryUseCase(
            self.character_repository
        )
        
        # ========== HOMEBREW USE CASES ==========
        self.get_homebrew_uc = GetHomebrewByIdUseCase(self.homebrew_repository)
        self.get_user_homebrew_uc = GetUserHomebrewListUseCase(self.homebrew_repository)
        self.create_homebrew_uc = CreateHomebrewUseCase(
            self.homebrew_repository
        )
        self.update_homebrew_uc = UpdateHomebrewUseCase(
            self.homebrew_repository
        )
        self.delete_homebrew_uc = DeleteHomebrewUseCase(self.homebrew_repository)
        self.submit_moderation_uc = SubmitHomebrewForModerationUseCase(self.homebrew_repository)
        self.get_moderation_status_uc = GetHomebrewModerationStatusUseCase(self.homebrew_repository)
        self.create_version_uc = CreateNewVersionUseCase(
            self.homebrew_repository
        )
        self.can_view_homebrew_uc = CanUserViewHomebrewUseCase(self.homebrew_repository)
        self.record_view_uc = RecordHomebrewViewUseCase(
            self.homebrew_repository,
            self.can_view_homebrew_uc
        )
        
        # ========== MODERATION USE CASES ==========
        self.get_queue_uc = GetModerationQueueUseCase(self.moderation_repository)
        self.get_queue_count_uc = GetModerationQueueCountUseCase(self.moderation_repository)
        self.get_queue_priority_uc = GetModerationQueuePriorityUseCase(self.moderation_repository)
        self.approve_uc = ApproveHomebrewUseCase(
            self.moderation_repository,
            self.homebrew_repository
        )
        self.reject_uc = RejectHomebrewUseCase(
            self.moderation_repository,
            self.homebrew_repository
        )
        self.get_moderation_history_uc = GetModerationHistoryUseCase(self.moderation_reader)
        self.get_moderator_stats_uc = GetModeratorStatisticsUseCase(self.moderation_reader)
        
        # ========== ADMIN USE CASES - USERS ==========
        self.get_total_users_uc = GetTotalUsersCountUseCase(self.user_stats_reader)
        self.get_user_stats_paginated_uc = GetUserStatisticsPaginatedUseCase(self.user_stats_reader)
        self.get_filtered_user_stats_uc = GetFilteredUserStatsUseCase(self.user_stats_reader)
        
        # ========== ADMIN USE CASES - CHARACTERS ==========
        self.get_total_characters_uc = GetTotalCharactersCountUseCase(self.character_stats_reader)
        self.get_characters_stats_uc = GetCharactersStatisticsUseCase(self.character_stats_reader)
        
        # ========== ADMIN USE CASES - HOMEBREW ==========
        self.get_total_homebrew_uc = GetTotalHomebrewCountUseCase(self.homebrew_stats_reader)
        self.get_homebrew_stats_uc = GetHomebrewStatisticsUseCase(self.homebrew_stats_reader)
        
        # ========== ADMIN USE CASES - SESSIONS ==========
        self.get_active_sessions_uc = GetActiveSessionsCountUseCase(self.session_stats_reader)
        self.get_session_stats_paginated_uc = GetSessionStatisticsPaginatedUseCase(self.session_stats_reader)
        self.get_filtered_session_stats_uc = GetFilteredSessionStatsUseCase(self.session_stats_reader)
        self.get_user_sessions_uc = GetUserSessionsUseCase(self.session_stats_reader)
        self.terminate_session_uc = TerminateSessionUseCase(self.session_stats_reader)
        
        # ========== ADMIN USE CASES - DASHBOARD ==========
        self.get_dashboard_stats_uc = GetSystemDashboardStatsUseCase(self.dashboard_reader)
        self.get_recent_activities_uc = GetRecentActivitiesUseCase(self.dashboard_reader)
        self.get_system_health_uc = GetSystemHealthUseCase(self.dashboard_reader)
        
        # ========== SYSTEMS USE CASES ==========
        self.get_active_systems_uc = GetActiveSystemsListUseCase(self.game_system_reader)
        self.get_system_by_id_uc = GetSystemByIdUseCase(self.game_system_reader)
        self.get_system_stats_uc = GetSystemStatisticsUseCase(self.game_system_reader)
        
        # ========== NOTIFICATIONS USE CASES ==========
        self.get_user_notifications_uc = GetUserNotificationsUseCase(self.notification_reader)
        
        # ========== ANALYTICS USE CASES ==========
        self.get_daily_stats_uc = GetDailyStatisticsUseCase(self.analytics_reader)
        self.get_weekly_stats_uc = GetWeeklyStatisticsUseCase(self.analytics_reader)
        self.get_monthly_stats_uc = GetMonthlyStatisticsUseCase(self.analytics_reader)
        self.get_date_range_stats_uc = GetDateRangeStatisticsUseCase(self.analytics_reader)
        self.get_user_activity_report_uc = GetUserActivityReportUseCase(self.analytics_reader)
        self.get_user_engagement_uc = GetUserEngagementUseCase(self.analytics_reader)
        self.get_content_popularity_uc = GetContentPopularityUseCase(self.analytics_reader)

        # ========== СЕРВИСЫ (инфраструктурные) ==========
        self.session_service = DjangoSessionService()


# ========== ГЛОБАЛЬНЫЙ ЭКЗЕМПЛЯР КОНТЕЙНЕРА ==========
# Создается один раз при импорте модуля
_container: Optional[Container] = None


def get_container() -> Container:
    """
    Получить экземпляр контейнера (ленивая инициализация).
    
    Использование:
        container = get_container()
        result = container.login_uc.execute(user_id, role)
    """
    global _container
    if _container is None:
        _container = Container()
    return _container


def init_container() -> Container:
    """
    Инициализировать контейнер (вызывается при старте приложения).
    
    Использование в core/apps.py:
        def ready(self):
            from infrastructure.di_config import init_container
            init_container()
    """
    global _container
    _container = Container()
    return _container


container = get_container()


# ========== ДЛЯ ОТЛАДКИ ==========
if __name__ == '__main__':
    c = get_container()
    
    print("=== DI Container initialized ===")
    print(f"LoginUseCase: {c.login_uc}")
    print(f"CreateCharacterUseCase: {c.create_character_uc}")
    print(f"GetModerationQueueUseCase: {c.get_queue_uc}")
    print(f"GetDashboardStatsUseCase: {c.get_dashboard_stats_uc}")
    print(f"GetDailyStatisticsUseCase: {c.get_daily_stats_uc}")
    print(f"GetUserStatisticsPaginatedUseCase: {c.get_user_stats_paginated_uc}")
    print("=== All use cases loaded successfully ===")