from typing import List
from django.db import connection
from business.interfaces.readers import INotificationReader
from business.value_objects import Notification
from infrastructure.readers.base import dict_fetch_all


class DjangoNotificationReader(INotificationReader):
    """Реализация читателя уведомлений"""
    
    def get_by_user(self, user_id: int, unread_only: bool = False) -> List[Notification]:
        # У тебя в таблице notifications нет поля is_read
        # Параметр unread_only пока игнорируем, если нет такого поля
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT notification_id, user_id, created_date, notification_type
                FROM notifications
                WHERE user_id = %s
                ORDER BY created_date DESC
            """, [user_id])
            
            return [
                Notification(
                    notification_id=row[0],
                    user_id=row[1],
                    created_date=row[2],
                    notification_type=row[3]
                ) for row in cursor.fetchall()
            ]