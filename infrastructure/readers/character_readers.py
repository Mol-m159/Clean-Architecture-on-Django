from typing import List
from datetime import datetime
from django.db import connection
from business.interfaces.readers import ICharacterStatisticsReader, CharacterStatsDTO


class DjangoCharacterStatisticsReader(ICharacterStatisticsReader):
    """Читатель статистики персонажей"""
    
    def get_total_count(self) -> int:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM characters")
            return cursor.fetchone()[0]
    
    def get_new_count_since(self, date: datetime) -> int:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM characters WHERE created_date >= %s",
                [date]
            )
            return cursor.fetchone()[0]
    
    def get_statistics_by_system(self) -> List[CharacterStatsDTO]:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    system_id,
                    COUNT(*) as character_count,
                    SUM(CASE WHEN CAST(created_date as DATE) = CAST(GETDATE() as DATE) THEN 1 ELSE 0 END) as created_today,
                    AVG(DATEDIFF(day, created_date, GETDATE())) as avg_age_days
                FROM characters
                WHERE system_id IN (SELECT system_id FROM game_systems WHERE is_active = 1)
                GROUP BY system_id
                ORDER BY character_count DESC
            """)
            
            results = []
            for row in cursor.fetchall():
                results.append(CharacterStatsDTO(
                    system_id=row[0],
                    character_count=row[1],
                    created_today=row[2],
                    avg_age_days=float(row[3]) if row[3] else 0.0
                ))
            return results