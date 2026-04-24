from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def role_required(allowed_roles):

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_type = request.session.get('user_type')
            user_id = request.session.get('user_id')
            
            if not user_id or not user_type:
                messages.error(request, 'Пожалуйста, войдите в систему')
                return redirect('login')
            
            if user_type not in allowed_roles:
                messages.error(request, 'У вас нет доступа к этой странице')
                return redirect('dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def login_required(view_func):
    """
    Декоратор для проверки авторизации.
    
    Использование:
        @method_decorator(login_required)
        def get(self, request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.error(request, 'Пожалуйста, войдите в систему')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper