"""
Auth Views - аутентификация и главный дашборд

Соответствует старому login.py и DashboardView
Использует чистую архитектуру через DI контейнер
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.utils import timezone
from django.utils.decorators import method_decorator

from infrastructure.di_config import container
from .decorators import login_required


class LoginView(View):
    """Страница входа."""
    
    def get(self, request):
        if request.session.get('user_id'):
            return redirect('dashboard')
        return render(request, 'auth/login.html')
    
    def post(self, request):
        user_id = request.POST.get('user_id')
        user_type = request.POST.get('user_type')
        
        if not user_id or not user_type:
            messages.error(request, 'Пожалуйста, заполните все поля')
            return redirect('login')
        
        try:
            user_id_int = int(user_id)
            
            # Проверяем существование пользователя через use case
            result = container.login_uc.execute(user_id_int, user_type)
            
            if not result.success:
                # Создаем пользователя через репозиторий
                from business.entities.user import User
                new_user = User(
                    user_id=user_id_int,
                    registration_date=timezone.now(),
                    last_activity_date=timezone.now()
                )
                container.user_repository.create(new_user)
                messages.info(request, 'Новый пользователь зарегистрирован')
                
                # Повторяем вход
                result = container.login_uc.execute(user_id_int, user_type)
            
            if result.success:
                # Сохраняем данные в Django session
                request.session['user_id'] = user_id_int
                request.session['user_type'] = user_type
                request.session['user_name'] = f"{user_type.capitalize()} #{user_id}"
                
                # Создаем запись о сессии через инфраструктурный сервис
                container.session_service.create_session(user_id_int)
                
                messages.success(request, 'Вы успешно вошли в систему')
                return redirect('dashboard')
            else:
                messages.error(request, f'Ошибка входа: {result.error_message}')
                
        except ValueError:
            messages.error(request, 'ID пользователя должен быть числом')
        except Exception as e:
            messages.error(request, f'Ошибка входа: {str(e)}')
        
        return redirect('login')


class LogoutView(View):
    """Выход из системы."""
    
    def get(self, request):
        user_id = request.session.get('user_id')
        
        if user_id:
            # Закрываем сессии через инфраструктурный сервис
            container.session_service.close_user_sessions(user_id)
            
            # Вызываем use case для выхода (если нужно что-то в бизнес-логике)
            container.logout_uc.execute(user_id)
        
        # Очищаем Django сессию
        request.session.flush()
        messages.success(request, 'Вы вышли из системы')
        return redirect('login')


class DashboardView(View):
    """
    Главная панель - редирект на соответствующую роль.
    
    Админ -> admin_dashboard
    Модератор -> moderator_dashboard
    Пользователь -> user_dashboard
    """
    
    @method_decorator(login_required)
    def get(self, request):
        user_type = request.session.get('user_type')
        
        if user_type == 'admin':
            return redirect('admin_dashboard')
        elif user_type == 'moderator':
            return redirect('moderator_dashboard')
        else:
            return redirect('user_dashboard')