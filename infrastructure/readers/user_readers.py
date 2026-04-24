from typing import List, Dict, Any, Optional
from datetime import datetime
from django.db import connection
from business.interfaces.readers import IUserStatisticsReader
from business.interfaces.readers import UserStatsDTO
from infrastructure.readers.base import PaginationHelper, dict_fetch_all


class DjangoUserStatisticsReader(IUserStatisticsReader):
    """Читатель статистики пользователей"""
    
    def get_total_count(self) -> int:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users")
            return cursor.fetchone()[0]
    
    def get_new_count_since(self, date: datetime) -> int:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE registration_date >= %s",
                [date]
            )
            return cursor.fetchone()[0]
    
    def get_all_statistics(self) -> List[UserStatsDTO]:
        query = """
            SELECT user_id, system_id,
                COUNT(DISTINCT character_id) as character_count,
                COUNT(DISTINCT entity_id) as homebrew_count,
                MAX(last_activity_date) as last_activity
            FROM (
                SELECT u.user_id, c.system_id, c.character_id, NULL as entity_id, u.last_activity_date
                FROM users u
                LEFT JOIN characters c ON u.user_id = c.user_id
                INNER JOIN game_systems gs ON gs.system_id = c.system_id AND gs.is_active = 1
                UNION ALL 
                SELECT u.user_id, he.system_id, NULL as character_id, he.entity_id, u.last_activity_date
                FROM users u
                LEFT JOIN homebrew_entities he ON u.user_id = he.author_id
                INNER JOIN game_systems gs ON gs.system_id = he.system_id AND gs.is_active = 1
            ) as UserData
            GROUP BY user_id, system_id
            ORDER BY character_count DESC, homebrew_count DESC
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = dict_fetch_all(cursor)
            
            return [
                UserStatsDTO(
                    user_id=r['user_id'],
                    system_id=r['system_id'],
                    character_count=r['character_count'],
                    homebrew_count=r['homebrew_count'],
                    last_activity=r['last_activity']
                ) for r in results
            ]
    
    def get_statistics_paginated(self, page: int, per_page: int) -> Dict[str, Any]:
        base_query = """
            SELECT user_id, system_id,
                COUNT(DISTINCT character_id) as character_count,
                COUNT(DISTINCT entity_id) as homebrew_count,
                MAX(last_activity_date) as last_activity
            FROM (
                SELECT u.user_id, c.system_id, c.character_id, NULL as entity_id, u.last_activity_date
                FROM users u
                LEFT JOIN characters c ON u.user_id = c.user_id
                INNER JOIN game_systems gs ON gs.system_id = c.system_id AND gs.is_active = 1
                UNION ALL 
                SELECT u.user_id, he.system_id, NULL as character_id, he.entity_id, u.last_activity_date
                FROM users u
                LEFT JOIN homebrew_entities he ON u.user_id = he.author_id
                INNER JOIN game_systems gs ON gs.system_id = he.system_id AND gs.is_active = 1
            ) as UserData
            GROUP BY user_id, system_id
        """
        
        result = PaginationHelper.get_paginated_data(
            base_query=base_query,
            params=[],
            page=page,
            per_page=per_page,
            order_by="ORDER BY character_count DESC, homebrew_count DESC"
        )
        
        # Преобразуем в UserStatsDTO
        result['data'] = [
            UserStatsDTO(
                user_id=item['user_id'],
                system_id=item['system_id'],
                character_count=item['character_count'],
                homebrew_count=item['homebrew_count'],
                last_activity=item['last_activity']
            ) for item in result['data']
        ]
        
        return result
    
    def get_filtered_statistics(self, filters: Dict[str, Any], page: int, per_page: int) -> Dict[str, Any]:
        params = []
        where_clauses = ["1=1"]
        having_clauses = []
        
        # Фильтр по системе - через HAVING (после GROUP BY)
        if filters.get('system_id'):
            having_clauses.append("system_id = %s")
            params.append(filters['system_id'])
        
        where_sql = " AND ".join(where_clauses)
        
        base_query = f"""
            SELECT user_id, system_id,
                COUNT(DISTINCT character_id) as character_count,
                COUNT(DISTINCT entity_id) as homebrew_count,
                MAX(last_activity_date) as last_activity
            FROM (
                SELECT u.user_id, c.system_id, c.character_id, NULL as entity_id, u.last_activity_date
                FROM users u
                LEFT JOIN characters c ON u.user_id = c.user_id
                INNER JOIN game_systems gs ON gs.system_id = c.system_id AND gs.is_active = 1
                WHERE {where_sql}
                UNION ALL 
                SELECT u.user_id, he.system_id, NULL as character_id, he.entity_id, u.last_activity_date
                FROM users u
                LEFT JOIN homebrew_entities he ON u.user_id = he.author_id
                INNER JOIN game_systems gs ON gs.system_id = he.system_id AND gs.is_active = 1
                WHERE {where_sql}
            ) as UserData
            GROUP BY user_id, system_id
        """
        
        # Минимальное количество персонажей
        if filters.get('min_characters'):
            having_clauses.append("COUNT(DISTINCT character_id) >= %s")
            params.append(filters['min_characters'])
        
        # Только создавшие контент
        if filters.get('has_homebrew'):
            having_clauses.append("COUNT(DISTINCT entity_id) > 0")
        
        if having_clauses:
            base_query += " HAVING " + " AND ".join(having_clauses)
        
        result = PaginationHelper.get_paginated_data(
            base_query=base_query,
            params=params,
            page=page,
            per_page=per_page,
            order_by="ORDER BY character_count DESC, homebrew_count DESC"
        )
        
        result['data'] = [
            UserStatsDTO(
                user_id=item['user_id'],
                system_id=item['system_id'],
                character_count=item['character_count'],
                homebrew_count=item['homebrew_count'],
                last_activity=item['last_activity']
            ) for item in result['data']
        ]
        
        return result