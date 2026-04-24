from .auth_views import LoginView, LogoutView, DashboardView
from .decorators import login_required, role_required
from .user_views import UserDashboardView
from .moderator_views import ModeratorDashboardView, ModerationQueueView, ModerateItemView
from .admin_views import AdminDashboardView, AdminUserStatsView, AdminSessionStatsView
from .character_views import (
    CharacterListView,
    CharacterDetailView,
    CharacterCreateAPIView,
    CharacterUpdateAPIView,
    CharacterDeleteAPIView,
)
from .homebrew_views import (
    HomebrewCreateAPIView,
    HomebrewUpdateAPIView,
    HomebrewSubmitAPIView,
    HomebrewDeleteAPIView,
    HomebrewListView,
    HomebrewDetailView,
)
from .notifications_views import NotificationsView

__all__ = [
    # Auth
    'LoginView',
    'LogoutView',
    'DashboardView',
    # Decorators
    'login_required',
    'role_required',
    # User
    'UserDashboardView',
    # Moderator
    'ModeratorDashboardView',
    'ModerationQueueView',
    'ModerateItemView',
    # Admin
    'AdminDashboardView',
    'AdminUserStatsView',
    'AdminSessionStatsView',
    # Characters
    'CharacterListView',
    'CharacterDetailView',
    'CharacterCreateAPIView',
    'CharacterUpdateAPIView',
    'CharacterDeleteAPIView',
    # Homebrew
    'HomebrewListView',
    'HomebrewDetailView',
    'HomebrewCreateAPIView',
    'HomebrewUpdateAPIView',
    'HomebrewSubmitAPIView',
    'HomebrewDeleteAPIView',
    # Notifications
    'NotificationsView',
    # API
    'UserCharactersViewSet',
    'UserHomebrewViewSet',
    'UserNotificationsViewSet',
]