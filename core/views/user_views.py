"""
User Views - панель пользователя и связанные страницы
Соответствует старому user.py
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator

from infrastructure.di_config import container
from .decorators import role_required, login_required


class UserDashboardView(View):
    """Панель пользователя"""
    
    @method_decorator(role_required(['user', 'moderator', 'admin']))
    def get(self, request):
        user_id = request.session.get('user_id')
        
        # Получаем персонажей пользователя
        characters_result = container.get_user_characters_uc.execute(user_id)
        
        # Получаем homebrew пользователя
        homebrew_result = container.get_user_homebrew_uc.execute(user_id)
        
        container.update_activity_uc.execute(user_id)
        
        # Преобразуем объекты Homebrew в словари для шаблона
        homebrew_items = []
        for h in homebrew_result.homebrew_items:
            homebrew_items.append({
                'entity_id': h.entity_id,
                'author_id': h.author_id,
                'system_id': h.system_id,
                'entity_type': h.entity_type.value,
                'created_date': h.created_date,
                'status': h.status.value,
            })
        
        context = {
            'characters': characters_result.characters[:5],
            'homebrew_items': homebrew_items[:5],
            'character_count': characters_result.count,
            'homebrew_count': homebrew_result.count,
            'user_id': user_id,
            'user_type': request.session.get('user_type'),
            'user_name': request.session.get('user_name'),
        }
        return render(request, 'user/dashboard.html', context)