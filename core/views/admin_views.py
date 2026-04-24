"""
Admin Views - панель администратора и статистика
Соответствует старому admin.py
"""

from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator

from infrastructure.di_config import container
from .decorators import role_required


class AdminDashboardView(View):
    """Панель администратора"""
    
    @method_decorator(role_required(['admin']))
    def get(self, request):
        # Получаем статистику для дашборда
        dashboard_result = container.get_dashboard_stats_uc.execute()
        
        # Получаем последние активности
        recent_result = container.get_recent_activities_uc.execute(limit=10)
        
        recent_activities = []
        if recent_result.success:
            for act in recent_result.activities:
                recent_activities.append({
                    'user_id': act.user_id,
                    'user_type': act.user_type,
                    'login_date': act.login_date,
                    'logout_date': act.logout_date,
                })
        
        stats = dashboard_result.stats
        context = {
            'total_users': stats.total_users if stats else 0,
            'total_characters': stats.total_characters if stats else 0,
            'total_homebrew': stats.total_homebrew if stats else 0,
            'active_sessions': stats.active_sessions if stats else 0,
            'new_users_today': stats.new_users_today if stats else 0,
            'new_characters_today': stats.new_characters_today if stats else 0,
            'new_homebrew_today': stats.new_homebrew_today if stats else 0,
            'recent_activities': recent_activities,
            'user_id': request.session.get('user_id'),
            'user_type': request.session.get('user_type'),
            'user_name': request.session.get('user_name'),
        }
        return render(request, 'admin/dashboard.html', context)


class AdminUserStatsView(View):
    """Статистика пользователей с пагинацией"""
    
    @method_decorator(role_required(['admin']))
    def get(self, request):
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        
        # Получаем фильтры
        from business.use_cases.admin.users import UserStatsFilters
        
        filters = {}
        if request.GET.get('system_id'):
            filters['system_id'] = int(request.GET.get('system_id'))
        if request.GET.get('min_characters'):
            filters['min_characters'] = int(request.GET.get('min_characters'))
        if request.GET.get('has_homebrew'):
            filters['has_homebrew'] = True
        if request.GET.get('active_only'):
            filters['active_only'] = True
        
        if filters:
            filter_obj = UserStatsFilters(
                system_id=filters.get('system_id'),
                min_characters=filters.get('min_characters'),
                has_homebrew=filters.get('has_homebrew'),
                active_only=filters.get('active_only')
            )
            result = container.get_filtered_user_stats_uc.execute(filter_obj, page, per_page)
        else:
            result = container.get_user_stats_paginated_uc.execute(page, per_page)
        
        # Получаем системы для фильтра
        systems_result = container.get_active_systems_uc.execute()
        systems = []
        if systems_result.success:
            for s in systems_result.systems:
                systems.append({
                    'system_id': s.system_id,
                    'created_date': s.created_date,
                    'is_active': s.is_active,
                })
        
        context = {
            'user_stats': result.data,
            'total_count': result.total,
            'current_page': result.page,
            'per_page': result.per_page,
            'total_pages': result.pages,
            'start_index': (result.page - 1) * result.per_page + 1 if result.data else 0,
            'end_index': min(result.page * result.per_page, result.total),
            'systems': systems,
            'filters': filters,
            'user_id': request.session.get('user_id'),
            'user_type': request.session.get('user_type'),
            'user_name': request.session.get('user_name'),
        }
        return render(request, 'admin/user_stats.html', context)


class AdminSessionStatsView(View):
    """Статистика сессий с пагинацией"""
    
    @method_decorator(role_required(['admin']))
    def get(self, request):
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        
        # Получаем фильтры
        from business.use_cases.admin.sessions import SessionStatsFilters
        from datetime import datetime
        
        filters = {}
        if request.GET.get('date_from'):
            filters['date_from'] = request.GET.get('date_from')
        if request.GET.get('date_to'):
            filters['date_to'] = request.GET.get('date_to')
        if request.GET.get('active_only'):
            filters['active_only'] = True
        
        if filters:
            filter_obj = SessionStatsFilters(
                date_from=datetime.fromisoformat(filters['date_from']) if filters.get('date_from') else None,
                date_to=datetime.fromisoformat(filters['date_to']) if filters.get('date_to') else None,
                active_only=filters.get('active_only')
            )
            result = container.get_filtered_session_stats_uc.execute(filter_obj, page, per_page)
        else:
            result = container.get_session_stats_paginated_uc.execute(page, per_page)
        
        # Получаем сводную статистику по сессиям
        active_count_result = container.get_active_sessions_uc.execute()
        
        context = {
            'session_stats': result.data,
            'total_count': result.total,
            'current_page': result.page,
            'per_page': result.per_page,
            'total_pages': result.pages,
            'start_index': (result.page - 1) * result.per_page + 1 if result.data else 0,
            'end_index': min(result.page * result.per_page, result.total),
            'filters': filters,
            'session_summary': {
                'active_sessions': active_count_result.count if active_count_result.success else 0,
            },
            'user_id': request.session.get('user_id'),
            'user_type': request.session.get('user_type'),
            'user_name': request.session.get('user_name'),
        }
        return render(request, 'admin/session_stats.html', context)