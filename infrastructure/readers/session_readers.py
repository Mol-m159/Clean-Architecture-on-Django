from typing import List, Dict, Any, Optional
from datetime import datetime
from django.db import connection
from django.utils import timezone
from business.interfaces.readers import ISessionStatisticsReader, SessionStatsDTO
from infrastructure.readers.base import PaginationHelper, dict_fetch_all


class DjangoSessionStatisticsReader(ISessionStatisticsReader):
    """Читатель статистики сессий"""
    
    def get_active_count(self) -> int:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM user_sessions WHERE logout_date IS NULL")
            return cursor.fetchone()[0]
    
    def get_all_statistics(self) -> List[SessionStatsDTO]:
        query = """
            SELECT 
                u.user_id, 
                us.session_id, 
                us.login_date, 
                us.logout_date,
                DATEDIFF(SECOND, us.login_date, ISNULL(us.logout_date, GETDATE())) as session_duration_seconds,
                DATEDIFF(MINUTE, us.login_date, ISNULL(us.logout_date, GETDATE())) as session_duration_minutes,
                COUNT(DISTINCT c.character_id) as characters_edited,
                COUNT(DISTINCT ev.view_id) as entities_viewed,
                CASE 
                    WHEN us.logout_date IS NULL THEN 'active'
                    ELSE 'completed'
                END as session_status
            FROM user_sessions us
            JOIN users u ON us.user_id = u.user_id
            LEFT JOIN characters c ON u.user_id = c.user_id 
                AND c.last_modified_date BETWEEN us.login_date AND ISNULL(us.logout_date, GETDATE())
            LEFT JOIN entity_views ev ON u.user_id = ev.user_id 
                AND ev.view_date BETWEEN us.login_date AND ISNULL(us.logout_date, GETDATE())
            GROUP BY u.user_id, us.session_id, us.login_date, us.logout_date
            ORDER BY session_duration_seconds DESC
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = dict_fetch_all(cursor)
            
            return [
                SessionStatsDTO(
                    session_id=r['session_id'],
                    user_id=r['user_id'],
                    login_date=r['login_date'],
                    logout_date=r['logout_date'],
                    session_duration_seconds=r['session_duration_seconds'],
                    session_duration_minutes=r['session_duration_minutes'],
                    characters_edited=r['characters_edited'],
                    entities_viewed=r['entities_viewed'],
                    session_status=r['session_status']
                ) for r in results
            ]
    
    def get_statistics_paginated(self, page: int, per_page: int) -> Dict[str, Any]:
        base_query = """
            SELECT 
                u.user_id, 
                us.session_id, 
                us.login_date, 
                us.logout_date,
                DATEDIFF(SECOND, us.login_date, ISNULL(us.logout_date, GETDATE())) as session_duration_seconds,
                DATEDIFF(MINUTE, us.login_date, ISNULL(us.logout_date, GETDATE())) as session_duration_minutes,
                COUNT(DISTINCT c.character_id) as characters_edited,
                COUNT(DISTINCT ev.view_id) as entities_viewed,
                CASE 
                    WHEN us.logout_date IS NULL THEN 'active'
                    ELSE 'completed'
                END as session_status
            FROM user_sessions us
            JOIN users u ON us.user_id = u.user_id
            LEFT JOIN characters c ON u.user_id = c.user_id 
                AND c.last_modified_date BETWEEN us.login_date AND ISNULL(us.logout_date, GETDATE())
            LEFT JOIN entity_views ev ON u.user_id = ev.user_id 
                AND ev.view_date BETWEEN us.login_date AND ISNULL(us.logout_date, GETDATE())
            GROUP BY u.user_id, us.session_id, us.login_date, us.logout_date
        """
        
        result = PaginationHelper.get_paginated_data(
            base_query=base_query,
            params=[],
            page=page,
            per_page=per_page,
            order_by="ORDER BY session_duration_seconds DESC"
        )
        
        result['data'] = [
            SessionStatsDTO(
                session_id=item['session_id'],
                user_id=item['user_id'],
                login_date=item['login_date'],
                logout_date=item['logout_date'],
                session_duration_seconds=item['session_duration_seconds'],
                session_duration_minutes=item['session_duration_minutes'],
                characters_edited=item['characters_edited'],
                entities_viewed=item['entities_viewed'],
                session_status=item['session_status']
            ) for item in result['data']
        ]
        
        return result
    
    def get_filtered_statistics(self, filters: Dict[str, Any], page: int, per_page: int) -> Dict[str, Any]:
        params = []
        where_clauses = ["1=1"]
        
        if filters.get('date_from'):
            where_clauses.append("us.login_date >= %s")
            params.append(filters['date_from'])
        
        if filters.get('date_to'):
            where_clauses.append("us.login_date <= %s")
            params.append(filters['date_to'])
        
        if filters.get('active_only'):
            where_clauses.append("us.logout_date IS NULL")
        
        where_sql = " AND ".join(where_clauses)
        
        base_query = f"""
            SELECT 
                u.user_id, 
                us.session_id, 
                us.login_date, 
                us.logout_date,
                DATEDIFF(SECOND, us.login_date, ISNULL(us.logout_date, GETDATE())) as session_duration_seconds,
                DATEDIFF(MINUTE, us.login_date, ISNULL(us.logout_date, GETDATE())) as session_duration_minutes,
                COUNT(DISTINCT c.character_id) as characters_edited,
                COUNT(DISTINCT ev.view_id) as entities_viewed,
                CASE 
                    WHEN us.logout_date IS NULL THEN 'active'
                    ELSE 'completed'
                END as session_status
            FROM user_sessions us
            JOIN users u ON us.user_id = u.user_id
            LEFT JOIN characters c ON u.user_id = c.user_id 
                AND c.last_modified_date BETWEEN us.login_date AND ISNULL(us.logout_date, GETDATE())
            LEFT JOIN entity_views ev ON u.user_id = ev.user_id 
                AND ev.view_date BETWEEN us.login_date AND ISNULL(us.logout_date, GETDATE())
            WHERE {where_sql}
            GROUP BY u.user_id, us.session_id, us.login_date, us.logout_date
        """
        
        result = PaginationHelper.get_paginated_data(
            base_query=base_query,
            params=params,
            page=page,
            per_page=per_page,
            order_by="ORDER BY session_duration_seconds DESC"
        )
        
        result['data'] = [
            SessionStatsDTO(
                session_id=item['session_id'],
                user_id=item['user_id'],
                login_date=item['login_date'],
                logout_date=item['logout_date'],
                session_duration_seconds=item['session_duration_seconds'],
                session_duration_minutes=item['session_duration_minutes'],
                characters_edited=item['characters_edited'],
                entities_viewed=item['entities_viewed'],
                session_status=item['session_status']
            ) for item in result['data']
        ]
        
        return result
    
    def get_by_user(self, user_id: int, limit: int = 50) -> List[SessionStatsDTO]:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    u.user_id, 
                    us.session_id, 
                    us.login_date, 
                    us.logout_date,
                    DATEDIFF(SECOND, us.login_date, ISNULL(us.logout_date, GETDATE())) as session_duration_seconds,
                    DATEDIFF(MINUTE, us.login_date, ISNULL(us.logout_date, GETDATE())) as session_duration_minutes,
                    COUNT(DISTINCT c.character_id) as characters_edited,
                    COUNT(DISTINCT ev.view_id) as entities_viewed,
                    CASE 
                        WHEN us.logout_date IS NULL THEN 'active'
                        ELSE 'completed'
                    END as session_status
                FROM user_sessions us
                JOIN users u ON us.user_id = u.user_id
                LEFT JOIN characters c ON u.user_id = c.user_id 
                    AND c.last_modified_date BETWEEN us.login_date AND ISNULL(us.logout_date, GETDATE())
                LEFT JOIN entity_views ev ON u.user_id = ev.user_id 
                    AND ev.view_date BETWEEN us.login_date AND ISNULL(us.logout_date, GETDATE())
                WHERE u.user_id = %s
                GROUP BY u.user_id, us.session_id, us.login_date, us.logout_date
                ORDER BY us.login_date DESC
            """, [user_id])
            
            results = dict_fetch_all(cursor)
            results = results[:limit]
            
            return [
                SessionStatsDTO(
                    session_id=r['session_id'],
                    user_id=r['user_id'],
                    login_date=r['login_date'],
                    logout_date=r['logout_date'],
                    session_duration_seconds=r['session_duration_seconds'],
                    session_duration_minutes=r['session_duration_minutes'],
                    characters_edited=r['characters_edited'],
                    entities_viewed=r['entities_viewed'],
                    session_status=r['session_status']
                ) for r in results
            ]
    
    def terminate_session(self, session_id: int) -> bool:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE user_sessions 
                SET logout_date = %s 
                WHERE session_id = %s AND logout_date IS NULL
            """, [timezone.now(), session_id])
            return cursor.rowcount > 0