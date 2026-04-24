from typing import List, Dict, Any
from datetime import datetime
from django.db import connection
from business.interfaces.readers import IHomebrewStatisticsReader, HomebrewStatsDTO


class DjangoHomebrewStatisticsReader(IHomebrewStatisticsReader):
    """Читатель статистики homebrew контента"""
    
    def get_total_count(self) -> int:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM homebrew_entities")
            return cursor.fetchone()[0]
    
    def get_new_count_since(self, date: datetime) -> int:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM homebrew_entities WHERE created_date >= %s",
                [date]
            )
            return cursor.fetchone()[0]
    
    def get_statistics(self) -> HomebrewStatsDTO:
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        with connection.cursor() as cursor:
            # По статусам
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM homebrew_entities
                GROUP BY status
            """)
            by_status = {row[0]: row[1] for row in cursor.fetchall()}
            
            # По типам
            cursor.execute("""
                SELECT entity_type, COUNT(*) as count
                FROM homebrew_entities
                GROUP BY entity_type
            """)
            by_type = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Создано сегодня
            cursor.execute(
                "SELECT COUNT(*) FROM homebrew_entities WHERE created_date >= %s",
                [today_start]
            )
            created_today = cursor.fetchone()[0]
            
            return HomebrewStatsDTO(
                total_count=self.get_total_count(),
                by_status=by_status,
                by_type=by_type,
                created_today=created_today
            )
    
    def get_by_status(self, status: str) -> List[Any]:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT entity_id, author_id, system_id, entity_type, created_date, status
                FROM homebrew_entities
                WHERE status = %s
                ORDER BY created_date ASC
            """, [status])
            
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]