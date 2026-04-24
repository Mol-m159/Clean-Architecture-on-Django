from typing import List, Optional
from django.utils import timezone
from django.db import transaction
from core.models import HomebrewEntities, HomebrewEdits, HomebrewModerations, EntityViews
from business.entities.homebrew import Homebrew, HomebrewStatus, HomebrewType
from business.interfaces.repositories import IHomebrewRepository
from business.value_objects import HomebrewEdit, HomebrewModeration


class DjangoHomebrewRepository(IHomebrewRepository):
    """Реализация репозитория homebrew контента"""
    
    def get_by_id(self, entity_id: int) -> Optional[Homebrew]:
        try:
            entity = HomebrewEntities.objects.select_related('author', 'system').get(
                entity_id=entity_id
            )
            return Homebrew(
                entity_id=entity.entity_id,
                author_id=entity.author_id,
                system_id=entity.system_id,
                entity_type=HomebrewType.from_string(entity.entity_type),
                created_date=entity.created_date,
                status=HomebrewStatus.from_string(entity.status)
            )
        except HomebrewEntities.DoesNotExist:
            return None
    
    def get_by_author(self, author_id: int) -> List[Homebrew]:
        entities = HomebrewEntities.objects.filter(author_id=author_id).order_by('-created_date')
        return [
            Homebrew(
                entity_id=e.entity_id,
                author_id=e.author_id,
                system_id=e.system_id,
                entity_type=HomebrewType.from_string(e.entity_type),
                created_date=e.created_date,
                status=HomebrewStatus.from_string(e.status)
            ) for e in entities
        ]
    
    def get_by_status(self, status: HomebrewStatus) -> List[Homebrew]:
        entities = HomebrewEntities.objects.filter(status=status.value)
        return self._to_entities(entities)
    
    @transaction.atomic
    def create(
        self,
        author_id: int,
        system_id: int,
        entity_type: HomebrewType,
    ) -> Homebrew:
        now = timezone.now()
        entity = HomebrewEntities.objects.create(
            author_id=author_id,
            system_id=system_id,
            entity_type=entity_type.value,
            created_date=now,
            status=HomebrewStatus.DRAFT.value
        )
        return Homebrew(
            entity_id=entity.entity_id,
            author_id=author_id,
            system_id=system_id,
            entity_type=entity_type,
            created_date=now,
            status=HomebrewStatus.DRAFT
        )
    
    def update(self, homebrew: Homebrew) -> None:
        HomebrewEntities.objects.filter(entity_id=homebrew.entity_id).update(
            system_id=homebrew.system_id,
            entity_type=homebrew.entity_type.value,
            status=homebrew.status.value
        )
    
    def delete(self, entity_id: int) -> bool:
        deleted, _ = HomebrewEntities.objects.filter(entity_id=entity_id).delete()
        return deleted > 0
    
    def add_edit_version(self, entity_id: int, version_number: int) -> None:
        HomebrewEdits.objects.create(
            entity_id=entity_id,
            edit_date=timezone.now(),
            version_number=version_number
        )
    
    def get_edit_history(self, entity_id: int) -> List[HomebrewEdit]:
        edits = HomebrewEdits.objects.filter(entity_id=entity_id).order_by('-version_number')
        return [
            HomebrewEdit(
                edit_id=e.edit_id,
                entity_id=e.entity_id,
                edit_date=e.edit_date,
                version_number=e.version_number
            ) for e in edits
        ]
    
    def get_latest_version(self, entity_id: int) -> Optional[HomebrewEdit]:
        latest = HomebrewEdits.objects.filter(entity_id=entity_id).order_by('-version_number').first()
        if latest:
            return HomebrewEdit(
                edit_id=latest.edit_id,
                entity_id=latest.entity_id,
                edit_date=latest.edit_date,
                version_number=latest.version_number
            )
        return None
    
    def add_moderation_record(
        self, 
        entity_id: int, 
        moderator_id: int, 
        old_status: HomebrewStatus, 
        new_status: HomebrewStatus
    ) -> None:
        HomebrewModerations.objects.create(
            moderator_id=moderator_id,
            entity_id=entity_id,
            moderation_date=timezone.now(),
            old_status=old_status.value,
            new_status=new_status.value
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
    
    def add_view(self, user_id: int, entity_id: int) -> None:
        EntityViews.objects.create(
            user_id=user_id,
            entity_id=entity_id,
            view_date=timezone.now()
        )
    
    def get_view_count(self, entity_id: int) -> int:
        return EntityViews.objects.filter(entity_id=entity_id).count()
    
    def _to_entities(self, queryset) -> List[Homebrew]:
        return [
            Homebrew(
                entity_id=e.entity_id,
                author_id=e.author_id,
                system_id=e.system_id,
                entity_type=HomebrewType.from_string(e.entity_type),
                created_date=e.created_date,
                status=HomebrewStatus.from_string(e.status)
            ) for e in queryset
        ]