from typing import List, Optional
from django.db import connection
from business.interfaces.readers import IGameSystemReader
from business.value_objects import GameSystem
from infrastructure.readers.base import dict_fetch_all


class DjangoGameSystemReader(IGameSystemReader):
    """Реализация читателя игровых систем"""
    
    def get_active_systems(self) -> List[GameSystem]:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT system_id, created_date, is_active
                FROM game_systems
                WHERE is_active = 1
                ORDER BY system_id
            """)
            
            return [
                GameSystem(
                    system_id=row[0],
                    created_date=row[1],
                    is_active=row[2]
                ) for row in cursor.fetchall()
            ]
    
    def get_by_id(self, system_id: int) -> Optional[GameSystem]:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT system_id, created_date, is_active
                FROM game_systems
                WHERE system_id = %s
            """, [system_id])
            
            row = cursor.fetchone()
            if row:
                return GameSystem(
                    system_id=row[0],
                    created_date=row[1],
                    is_active=row[2]
                )
            return None
    
    def get_system_statistics(self, system_id: int) -> dict:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM characters WHERE system_id = %s) as total_characters,
                    (SELECT COUNT(*) FROM homebrew_entities WHERE system_id = %s) as total_homebrew,
                    (SELECT COUNT(*) FROM entity_views ev 
                     JOIN homebrew_entities he ON ev.entity_id = he.entity_id 
                     WHERE he.system_id = %s) as total_views,
                    (SELECT COUNT(DISTINCT user_id) FROM characters WHERE system_id = %s) as active_users
            """, [system_id, system_id, system_id, system_id])
            
            row = cursor.fetchone()
            return {
                'total_characters': row[0] or 0,
                'total_homebrew': row[1] or 0,
                'total_views': row[2] or 0,
                'active_users': row[3] or 0
            }