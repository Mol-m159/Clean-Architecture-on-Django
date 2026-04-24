from typing import List, Optional
from django.db import connection
from django.utils import timezone
from django.db import transaction
from django.db import models
from core.models import HomebrewEntities, HomebrewModerations
from business.entities.homebrew import Homebrew, HomebrewStatus
from business.interfaces.repositories import IModerationRepository
from business.value_objects import HomebrewModeration
from infrastructure.repositories.django_homebrew_repository import DjangoHomebrewRepository


class DjangoModerationRepository(IModerationRepository):
    """Реализация репозитория модерации"""
    
    def __init__(self):
        self.homebrew_repo = DjangoHomebrewRepository()
    
    def get_moderation_queue(self, sort_by_date_asc: bool = True) -> List[Homebrew]:
        order = 'created_date' if sort_by_date_asc else '-created_date'
        entities = HomebrewEntities.objects.filter(
            status=HomebrewStatus.MODERATION.value
        ).order_by(order)
        return self.homebrew_repo._to_entities(entities)
    
    def get_moderation_queue_with_days(self) -> List[dict]:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT entity_id, DATEDIFF(day, created_date, GETDATE()) as days_in_queue
                FROM homebrew_entities
                WHERE status = 'moderation'
            """)
            results = []
            for row in cursor.fetchall():
                homebrew = self.homebrew_repo.get_by_id(row[0])
                if homebrew:
                    results.append({
                        'homebrew': homebrew,
                        'days_in_queue': row[1]
                    })
            return results
    
    @transaction.atomic
    def approve(self, entity_id: int, moderator_id: int) -> None:
        entity = HomebrewEntities.objects.get(entity_id=entity_id)
        old_status = entity.status
        
        entity.status = HomebrewStatus.APPROVED.value
        entity.save()
        
        HomebrewModerations.objects.create(
            moderator_id=moderator_id,
            entity_id=entity_id,
            moderation_date=timezone.now(),
            old_status=old_status,
            new_status=HomebrewStatus.APPROVED.value
        )
    
    @transaction.atomic
    def reject(self, entity_id: int, moderator_id: int, reason: Optional[str] = None) -> None:
        entity = HomebrewEntities.objects.get(entity_id=entity_id)
        old_status = entity.status
        
        entity.status = HomebrewStatus.REJECTED.value
        entity.save()
        
        HomebrewModerations.objects.create(
            moderator_id=moderator_id,
            entity_id=entity_id,
            moderation_date=timezone.now(),
            old_status=old_status,
            new_status=HomebrewStatus.REJECTED.value
        )
    
    def get_moderation_history(self, entity_id: int) -> List[HomebrewModeration]:
        records = HomebrewModerations.objects.filter(entity_id=entity_id).order_by('-moderation_date')
        return [
            HomebrewModeration(
                moderation_id=r.moderation_id,
                moderator_id=r.moderator_id,
                entity_id=r.entity_id,
                moderation_date=r.moderation_date,
                old_status=r.old_status,
                new_status=r.new_status
            ) for r in records
        ]
    
    def get_moderator_stats(self, moderator_id: int) -> dict:
        stats = HomebrewModerations.objects.filter(moderator_id=moderator_id).aggregate(
            total_moderated=models.Count('moderation_id'),
            approved=models.Count('moderation_id', filter=models.Q(new_status='approved')),
            rejected=models.Count('moderation_id', filter=models.Q(new_status='rejected')),
            last_moderation_date=models.Max('moderation_date')
        )
        return stats
    
    def get_all_moderators_stats(self) -> List[dict]:
        stats = HomebrewModerations.objects.values('moderator_id').annotate(
            total_moderated=models.Count('moderation_id'),
            approved=models.Count('moderation_id', filter=models.Q(new_status='approved')),
            rejected=models.Count('moderation_id', filter=models.Q(new_status='rejected')),
            last_moderation_date=models.Max('moderation_date')
        )
        return list(stats)