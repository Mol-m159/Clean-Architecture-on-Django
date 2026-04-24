# Users
from business.use_cases.admin.users import (
    GetTotalUsersCountUseCase,
    TotalUsersCountResult,
    GetNewUsersTodayUseCase,
    NewUsersTodayResult,
    GetUserStatisticsUseCase,
    UserStatisticsResult,
    GetUserStatisticsPaginatedUseCase,
    PaginatedUserStatsResult,
    GetFilteredUserStatsUseCase,
    FilteredUserStatsResult,
    UserStatsFilters,
)

# Characters
from business.use_cases.admin.characters import (
    GetTotalCharactersCountUseCase,
    TotalCharactersCountResult,
    GetNewCharactersTodayUseCase,
    NewCharactersTodayResult,
    GetCharactersStatisticsUseCase,
    CharactersStatisticsResult,
)

# Homebrew
from business.use_cases.admin.homebrew import (
    GetTotalHomebrewCountUseCase,
    TotalHomebrewCountResult,
    GetNewHomebrewTodayUseCase,
    NewHomebrewTodayResult,
    GetHomebrewStatisticsUseCase,
    HomebrewStatisticsResult,
    GetHomebrewByStatusUseCase,
    HomebrewByStatusResult,
)

# Sessions
from business.use_cases.admin.sessions import (
    GetActiveSessionsCountUseCase,
    ActiveSessionsCountResult,
    GetSessionStatisticsUseCase,
    SessionStatisticsResult,
    GetSessionStatisticsPaginatedUseCase,
    PaginatedSessionStatsResult,
    GetFilteredSessionStatsUseCase,
    FilteredSessionStatsResult,
    SessionStatsFilters,
    GetUserSessionsUseCase,
    UserSessionsResult,
    TerminateSessionUseCase,
    TerminateSessionResult,
)

# Dashboard
from business.use_cases.admin.dashboard import (
    GetSystemDashboardStatsUseCase,
    DashboardStatsResult,
    GetRecentActivitiesUseCase,
    RecentActivitiesResult,
    GetSystemHealthUseCase,
    SystemHealthResult,
)

__all__ = [
    # Users
    'GetTotalUsersCountUseCase',
    'TotalUsersCountResult',
    'GetNewUsersTodayUseCase',
    'NewUsersTodayResult',
    'GetUserStatisticsUseCase',
    'UserStatisticsResult',
    'GetUserStatisticsPaginatedUseCase',
    'PaginatedUserStatsResult',
    'GetFilteredUserStatsUseCase',
    'FilteredUserStatsResult',
    'UserStatsFilters',
    # Characters
    'GetTotalCharactersCountUseCase',
    'TotalCharactersCountResult',
    'GetNewCharactersTodayUseCase',
    'NewCharactersTodayResult',
    'GetCharactersStatisticsUseCase',
    'CharactersStatisticsResult',
    # Homebrew
    'GetTotalHomebrewCountUseCase',
    'TotalHomebrewCountResult',
    'GetNewHomebrewTodayUseCase',
    'NewHomebrewTodayResult',
    'GetHomebrewStatisticsUseCase',
    'HomebrewStatisticsResult',
    'GetHomebrewByStatusUseCase',
    'HomebrewByStatusResult',
    # Sessions
    'GetActiveSessionsCountUseCase',
    'ActiveSessionsCountResult',
    'GetSessionStatisticsUseCase',
    'SessionStatisticsResult',
    'GetSessionStatisticsPaginatedUseCase',
    'PaginatedSessionStatsResult',
    'GetFilteredSessionStatsUseCase',
    'FilteredSessionStatsResult',
    'SessionStatsFilters',
    'GetUserSessionsUseCase',
    'UserSessionsResult',
    'TerminateSessionUseCase',
    'TerminateSessionResult',
    # Dashboard
    'GetSystemDashboardStatsUseCase',
    'DashboardStatsResult',
    'GetRecentActivitiesUseCase',
    'RecentActivitiesResult',
    'GetSystemHealthUseCase',
    'SystemHealthResult',
]