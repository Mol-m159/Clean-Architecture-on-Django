# core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import (
    # Web views
    LoginView,
    LogoutView,
    DashboardView,
    UserDashboardView,
    ModeratorDashboardView,
    ModerationQueueView,
    ModerateItemView,
    AdminDashboardView,
    AdminUserStatsView,
    AdminSessionStatsView,
    CharacterListView,
    CharacterDetailView,
    CharacterCreateAPIView,
    CharacterUpdateAPIView,
    CharacterDeleteAPIView,
    HomebrewListView,
    HomebrewDetailView,
    HomebrewCreateAPIView,
    HomebrewUpdateAPIView,
    HomebrewSubmitAPIView,
    HomebrewDeleteAPIView,
    NotificationsView,

)





urlpatterns = [
    # ================== WEB ==================
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Admin web
    path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/user-stats/', AdminUserStatsView.as_view(), name='admin_user_stats'),
    path('admin/session-stats/', AdminSessionStatsView.as_view(), name='admin_session_stats'),
    
    # Moderator web
    path('moderator/', ModeratorDashboardView.as_view(), name='moderator_dashboard'),
    path('moderator/queue/', ModerationQueueView.as_view(), name='moderation_queue'),
    path('moderator/moderate/<int:entity_id>/', ModerateItemView.as_view(), name='moderate_item'),
    
    # User web
    path('user/', UserDashboardView.as_view(), name='user_dashboard'),
    
    # Персонажи (web)
    path('user/characters/', CharacterListView.as_view(), name='character_list'),
    path('user/characters/<int:character_id>/', CharacterDetailView.as_view(), name='character_detail'),
    
    # API для персонажей 
    path('user/api/characters/create/', CharacterCreateAPIView.as_view(), name='api_character_create'),
    path('user/api/characters/<int:character_id>/update/', CharacterUpdateAPIView.as_view(), name='api_character_update'),
    path('user/api/characters/<int:character_id>/delete/', CharacterDeleteAPIView.as_view(), name='api_character_delete'),
    
    # Homebrew (web)
    path('user/homebrew/', HomebrewListView.as_view(), name='homebrew_list'),
    path('user/homebrew/<int:entity_id>/', HomebrewDetailView.as_view(), name='homebrew_detail'),
    
    # API для homebrew 
    path('user/api/homebrew/create/', HomebrewCreateAPIView.as_view(), name='api_homebrew_create'),
    path('user/api/homebrew/<int:entity_id>/update/', HomebrewUpdateAPIView.as_view(), name='api_homebrew_update'),
    path('user/api/homebrew/<int:entity_id>/submit/', HomebrewSubmitAPIView.as_view(), name='api_homebrew_submit'),
    path('user/api/homebrew/<int:entity_id>/delete/', HomebrewDeleteAPIView.as_view(), name='api_homebrew_delete'),
    
    # Notifications (web)
    path('user/notifications/', NotificationsView.as_view(), name='notifications'),
    
]