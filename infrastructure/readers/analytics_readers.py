from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from django.db import connection
from business.interfaces.readers import IAnalyticsReader
from business.interfaces.readers import (
    UserActivityReportDTO, 
    ContentPopularityDTO, 
    UserEngagementDTO, 
    DailyStatsDTO
)
from infrastructure.readers.base import dict_fetch_all


class DjangoAnalyticsReader(IAnalyticsReader):
    """Реализация читателя для аналитики и отчетов"""
    
    def get_user_activity_report(
        self, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[UserActivityReportDTO]:
        """
        Отчет по активности пользователей.
        
        Адаптировано из старого view.py:
        - Статистика по сессиям пользователей
        - Количество созданных персонажей и контента
        """
        params = []
        where_clause = "1=1"
        
        if start_date:
            where_clause += " AND us.login_date >= %s"
            params.append(start_date)
        if end_date:
            where_clause += " AND us.login_date <= %s"
            params.append(end_date)
        
        query = f"""
            SELECT 
                u.user_id,
                COUNT(DISTINCT us.session_id) as total_sessions,
                COALESCE(SUM(DATEDIFF(MINUTE, us.login_date, ISNULL(us.logout_date, GETDATE()))), 0) as total_duration_minutes,
                COUNT(DISTINCT c.character_id) as characters_created,
                COUNT(DISTINCT he.entity_id) as homebrew_created,
                MAX(us.login_date) as last_active_date
            FROM users u
            LEFT JOIN user_sessions us ON u.user_id = us.user_id
            LEFT JOIN characters c ON u.user_id = c.user_id
            LEFT JOIN homebrew_entities he ON u.user_id = he.author_id
            WHERE {where_clause}
            GROUP BY u.user_id
            ORDER BY total_sessions DESC, total_duration_minutes DESC
            OFFSET 0 ROWS FETCH NEXT %s ROWS ONLY
        """
        params.append(limit)
        
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            results = dict_fetch_all(cursor)
            
            return [
                UserActivityReportDTO(
                    user_id=r['user_id'],
                    total_sessions=r['total_sessions'] or 0,
                    total_duration_minutes=float(r['total_duration_minutes'] or 0),
                    characters_created=r['characters_created'] or 0,
                    homebrew_created=r['homebrew_created'] or 0,
                    last_active_date=r['last_active_date']
                ) for r in results
            ]
    
    def get_content_popularity(
        self,
        limit: int = 50,
        entity_type: Optional[str] = None
    ) -> List[ContentPopularityDTO]:
        """
        Рейтинг популярности контента по просмотрам.
        
        Основано на старой логике подсчета просмотров:
        - JOIN entity_views для получения количества просмотров
        - Фильтр по типу контента
        """
        params = []
        type_filter = ""
        
        if entity_type:
            type_filter = " AND he.entity_type = %s"
            params.append(entity_type)
        
        query = f"""
            SELECT 
                he.entity_id,
                he.entity_type,
                he.author_id,
                COUNT(ev.view_id) as view_count,
                DATEDIFF(day, he.created_date, GETDATE()) as days_since_creation
            FROM homebrew_entities he
            LEFT JOIN entity_views ev ON he.entity_id = ev.entity_id
            WHERE he.status = 'approved' {type_filter}
            GROUP BY he.entity_id, he.entity_type, he.author_id, he.created_date
            ORDER BY view_count DESC
            OFFSET 0 ROWS FETCH NEXT %s ROWS ONLY
        """
        params.append(limit)
        
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            results = dict_fetch_all(cursor)
            
            return [
                ContentPopularityDTO(
                    entity_id=r['entity_id'],
                    entity_type=r['entity_type'],
                    author_id=r['author_id'],
                    view_count=r['view_count'] or 0,
                    days_since_creation=r['days_since_creation'] or 0
                ) for r in results
            ]
    
    def get_user_engagement(self, limit: int = 100) -> List[UserEngagementDTO]:
        """
        Метрики вовлеченности пользователей.
        
        Рассчитывает engagement_score на основе:
        - Количество сессий
        - Количество созданных персонажей
        - Количество созданного контента
        - Количество уникальных систем
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH UserMetrics AS (
                    SELECT 
                        u.user_id,
                        COUNT(DISTINCT us.session_id) as session_count,
                        COUNT(DISTINCT c.character_id) as character_count,
                        COUNT(DISTINCT he.entity_id) as homebrew_count,
                        COUNT(DISTINCT c.system_id) + COUNT(DISTINCT he.system_id) as unique_systems
                    FROM users u
                    LEFT JOIN user_sessions us ON u.user_id = us.user_id
                    LEFT JOIN characters c ON u.user_id = c.user_id
                    LEFT JOIN homebrew_entities he ON u.user_id = he.author_id
                    GROUP BY u.user_id
                )
                SELECT 
                    user_id,
                    (session_count + character_count + homebrew_count) as total_actions,
                    unique_systems,
                    CASE 
                        WHEN session_count = 0 THEN 0
                        ELSE (session_count * 20 + 
                              character_count * 15 + 
                              homebrew_count * 25 + 
                              unique_systems * 10)
                    END as engagement_score
                FROM UserMetrics
                WHERE session_count > 0 OR character_count > 0 OR homebrew_count > 0
                ORDER BY engagement_score DESC
                OFFSET 0 ROWS FETCH NEXT %s ROWS ONLY
            """, [limit])
            
            results = dict_fetch_all(cursor)
            
            return [
                UserEngagementDTO(
                    user_id=r['user_id'],
                    total_actions=r['total_actions'] or 0,
                    unique_systems=r['unique_systems'] or 0,
                    engagement_score=min(float(r['engagement_score'] or 0), 100.0)
                ) for r in results
            ]
    
    def get_daily_statistics(self, target_date: date) -> DailyStatsDTO:
        """
        Статистика за конкретный день.
        
        Адаптировано из старой логики подсчета новых сущностей за день.
        """
        start_of_day = datetime.combine(target_date, datetime.min.time())
        end_of_day = datetime.combine(target_date, datetime.max.time())
        
        with connection.cursor() as cursor:
            # Новые пользователи
            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE registration_date BETWEEN %s AND %s",
                [start_of_day, end_of_day]
            )
            new_users = cursor.fetchone()[0]
            
            # Новые персонажи
            cursor.execute(
                "SELECT COUNT(*) FROM characters WHERE created_date BETWEEN %s AND %s",
                [start_of_day, end_of_day]
            )
            new_characters = cursor.fetchone()[0]
            
            # Новый контент
            cursor.execute(
                "SELECT COUNT(*) FROM homebrew_entities WHERE created_date BETWEEN %s AND %s",
                [start_of_day, end_of_day]
            )
            new_homebrew = cursor.fetchone()[0]
            
            # Активные сессии (сессии, которые были активны в этот день)
            cursor.execute("""
                SELECT COUNT(*) FROM user_sessions 
                WHERE login_date <= %s AND (logout_date IS NULL OR logout_date >= %s)
            """, [end_of_day, start_of_day])
            active_sessions = cursor.fetchone()[0]
            
            # Всего просмотров за день
            cursor.execute(
                "SELECT COUNT(*) FROM entity_views WHERE view_date BETWEEN %s AND %s",
                [start_of_day, end_of_day]
            )
            total_views = cursor.fetchone()[0]
            
            return DailyStatsDTO(
                date=target_date,
                new_users=new_users,
                new_characters=new_characters,
                new_homebrew=new_homebrew,
                active_sessions=active_sessions,
                total_views=total_views
            )
    
    def get_weekly_statistics(self, week_start: date) -> Dict[str, Any]:
        daily_stats = {}
        totals = {
            'new_users': 0,
            'new_characters': 0,
            'new_homebrew': 0,
            'active_sessions': 0,
            'total_views': 0
        }
        
        for i in range(7):
            current_date = week_start + timedelta(days=i)
            stats = self.get_daily_statistics(current_date)
            daily_stats[current_date.isoformat()] = stats
            
            totals['new_users'] += stats.new_users
            totals['new_characters'] += stats.new_characters
            totals['new_homebrew'] += stats.new_homebrew
            totals['active_sessions'] += stats.active_sessions
            totals['total_views'] += stats.total_views
        
        return {
            'daily_stats': daily_stats,
            'totals': totals
        }
    
    def get_monthly_statistics(self, year: int, month: int) -> Dict[str, Any]:
        import calendar
        
        first_day = date(year, month, 1)
        last_day = date(year, month, calendar.monthrange(year, month)[1])
        
        daily_stats = {}
        totals = {
            'new_users': 0,
            'new_characters': 0,
            'new_homebrew': 0,
            'active_sessions': 0,
            'total_views': 0
        }
        
        current_date = first_day
        while current_date <= last_day:
            stats = self.get_daily_statistics(current_date)
            daily_stats[current_date.day] = stats
            
            totals['new_users'] += stats.new_users
            totals['new_characters'] += stats.new_characters
            totals['new_homebrew'] += stats.new_homebrew
            totals['active_sessions'] += stats.active_sessions
            totals['total_views'] += stats.total_views
            
            current_date += timedelta(days=1)
        
        return {
            'daily_stats': daily_stats,
            'totals': totals
        }
    
    def get_date_range_statistics(
        self,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:

        daily_stats = {}
        totals = {
            'new_users': 0,
            'new_characters': 0,
            'new_homebrew': 0,
            'active_sessions': 0,
            'total_views': 0
        }
        
        current_date = start_date
        while current_date <= end_date:
            stats = self.get_daily_statistics(current_date)
            daily_stats[current_date.isoformat()] = stats
            
            totals['new_users'] += stats.new_users
            totals['new_characters'] += stats.new_characters
            totals['new_homebrew'] += stats.new_homebrew
            totals['active_sessions'] += stats.active_sessions
            totals['total_views'] += stats.total_views
            
            current_date += timedelta(days=1)
        
        return {
            'daily_stats': daily_stats,
            'totals': totals
        }