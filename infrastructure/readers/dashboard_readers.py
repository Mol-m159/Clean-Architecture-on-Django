from typing import Dict, Any, List
from datetime import datetime
from django.db import connection
from business.interfaces.readers import ISystemDashboardReader, DashboardStatsDTO, RecentActivityDTO
from infrastructure.readers.base import dict_fetch_all


class DjangoSystemDashboardReader(ISystemDashboardReader):
    """Читатель для дашборда администратора"""
    
    def get_dashboard_stats(self) -> DashboardStatsDTO:
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM characters")
            total_characters = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM homebrew_entities")
            total_homebrew = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM user_sessions WHERE logout_date IS NULL")
            active_sessions = cursor.fetchone()[0]
            
            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE registration_date >= %s",
                [today_start]
            )
            new_users_today = cursor.fetchone()[0]
            
            cursor.execute(
                "SELECT COUNT(*) FROM characters WHERE created_date >= %s",
                [today_start]
            )
            new_characters_today = cursor.fetchone()[0]
            
            cursor.execute(
                "SELECT COUNT(*) FROM homebrew_entities WHERE created_date >= %s",
                [today_start]
            )
            new_homebrew_today = cursor.fetchone()[0]
            
            return DashboardStatsDTO(
                total_users=total_users,
                total_characters=total_characters,
                total_homebrew=total_homebrew,
                active_sessions=active_sessions,
                new_users_today=new_users_today,
                new_characters_today=new_characters_today,
                new_homebrew_today=new_homebrew_today
            )
    
    def get_recent_activities(self, limit: int = 10) -> List[RecentActivityDTO]:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT TOP %s 
                    us.user_id,
                    CASE 
                        WHEN us.user_id IN (40212) THEN 'admin'
                        WHEN us.user_id IN (40213, 40214) THEN 'moderator'
                        ELSE 'user'
                    END as user_type,
                    us.login_date,
                    us.logout_date
                FROM user_sessions us
                ORDER BY us.login_date DESC
            """, [limit])
            
            results = dict_fetch_all(cursor)
            
            return [
                RecentActivityDTO(
                    user_id=r['user_id'],
                    user_type=r['user_type'],
                    login_date=r['login_date'],
                    logout_date=r['logout_date']
                ) for r in results
            ]
    
    def get_system_health(self) -> Dict[str, Any]:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                db_ok = True
        except Exception:
            db_ok = False
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM user_sessions WHERE logout_date IS NULL")
            active_sessions = cursor.fetchone()[0]
        
        return {
            'status': 'healthy' if db_ok else 'unhealthy',
            'metrics': {
                'db_connected': db_ok,
                'active_sessions': active_sessions
            }
        }