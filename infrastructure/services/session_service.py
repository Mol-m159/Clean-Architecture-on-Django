from typing import Optional
from django.utils import timezone
from core.models import UserSessions


class DjangoSessionService:
    """Сервис для работы с сессиями (только инфраструктурный слой)"""
    
    def create_session(self, user_id: int) -> None:
        """Создать сессию при входе"""
        UserSessions.objects.create(
            user_id=user_id,
            login_date=timezone.now()
        )
    
    def close_user_sessions(self, user_id: int) -> int:
        """Закрыть все активные сессии пользователя"""
        return UserSessions.objects.filter(
            user_id=user_id,
            logout_date__isnull=True
        ).update(logout_date=timezone.now())
    
    def get_active_session(self, user_id: int) -> Optional[dict]:
        """Получить активную сессию (если нужно)"""
        session = UserSessions.objects.filter(
            user_id=user_id,
            logout_date__isnull=True
        ).first()
        
        if session:
            return {
                'session_id': session.session_id,
                'login_date': session.login_date,
            }
        return None