# business/interfaces/__init__.py

# ==================== Репозитории ====================
from business.interfaces.repositories import (
    IUserRepository,
    ICharacterRepository,
    IHomebrewRepository,
    IModerationRepository,
)

# ==================== Readers (основные) ====================
from business.interfaces.readers import (
    IGameSystemReader,
    ICharacterEditReader,
    IHomebrewEditReader,
    IHomebrewModerationReader,
    IEntityViewReader,
    ISessionReader,
    INotificationReader,
    ISystemEventReader,
)

# ==================== Readers (статистика) ====================
from business.interfaces.readers import (
    IUserStatisticsReader,
    ICharacterStatisticsReader,
    IHomebrewStatisticsReader,
    ISessionStatisticsReader,
    ISystemDashboardReader,
    IAnalyticsReader,
)

# ==================== DTO ====================
from business.interfaces.readers import (
    UserStatsDTO,
    CharacterStatsDTO,
    HomebrewStatsDTO,
    SessionStatsDTO,
    DashboardStatsDTO,
    RecentActivityDTO,
    UserActivityReportDTO,
    ContentPopularityDTO,
    UserEngagementDTO,
    DailyStatsDTO,
)

__all__ = [
    # Репозитории
    'IUserRepository',
    'ICharacterRepository',
    'IHomebrewRepository',
    'IModerationRepository',
    
    # Readers (основные)
    'IGameSystemReader',
    'ICharacterEditReader',
    'IHomebrewEditReader',
    'IHomebrewModerationReader',
    'IEntityViewReader',
    'ISessionReader',
    'INotificationReader',
    'ISystemEventReader',
    
    # Readers (статистика)
    'IUserStatisticsReader',
    'ICharacterStatisticsReader',
    'IHomebrewStatisticsReader',
    'ISessionStatisticsReader',
    'ISystemDashboardReader',
    'IAnalyticsReader',
    
    # DTO
    'UserStatsDTO',
    'CharacterStatsDTO',
    'HomebrewStatsDTO',
    'SessionStatsDTO',
    'DashboardStatsDTO',
    'RecentActivityDTO',
    'UserActivityReportDTO',
    'ContentPopularityDTO',
    'UserEngagementDTO',
    'DailyStatsDTO',
]