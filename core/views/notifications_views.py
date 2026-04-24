"""
Notifications Views - уведомления пользователя
Соответствует шаблону user/notifications.html
"""

from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator

from infrastructure.di_config import container
from .decorators import role_required


class NotificationsView(View):
    """
    Список уведомлений пользователя.
    Соответствует шаблону user/notifications.html
    """
    
    @method_decorator(role_required(['user', 'moderator', 'admin']))
    def get(self, request):
        user_id = request.session.get('user_id')
        
        # Получаем уведомления
        result = container.get_user_notifications_uc.execute(user_id)
        
        # Преобразуем для шаблона
        notifications = []
        for n in result.notifications:
            # Определяем сообщение по типу
            message = None
            if n.notification_type == 'homebrew_approved':
                message = 'Ваш контент был одобрен'
            elif n.notification_type == 'homebrew_rejected':
                message = 'Ваш контент был отклонен'
            elif n.notification_type == 'welcome_message':
                message = 'Добро пожаловать в систему!'
            
            notifications.append({
                'notification_id': n.notification_id,
                'user_id': n.user_id,
                'created_date': n.created_date,
                'notification_type': n.notification_type,
                'message': message,
                'is_read': False,  # в текущей таблице нет поля is_read
            })
        
        context = {
            'notifications': notifications,
            'total_count': len(notifications),
            'user_id': user_id,
            'user_type': request.session.get('user_type'),
            'user_name': request.session.get('user_name'),
        }
        return render(request, 'user/notifications.html', context)