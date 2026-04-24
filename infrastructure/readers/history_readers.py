from typing import List, Optional
from django.db import connection
from core.models import CharacterEdits, HomebrewEdits, HomebrewModerations
from business.value_objects import CharacterEdit, HomebrewEdit, HomebrewModeration
from business.interfaces.readers import ICharacterEditReader, IHomebrewEditReader, IHomebrewModerationReader


class DjangoCharacterEditReader(ICharacterEditReader):
    """Читатель истории изменений персонажей"""
    
    def get_by_character(self, character_id: int, limit: int = 50) -> List[CharacterEdit]:
        edits = CharacterEdits.objects.filter(
            character_id=character_id
        ).order_by('-edit_date')[:limit]
        
        return [
            CharacterEdit(
                edit_id=e.edit_id,
                character_id=e.character_id,
                edit_date=e.edit_date,
                edit_type=e.edit_type
            ) for e in edits
        ]


class DjangoHomebrewEditReader(IHomebrewEditReader):
    """Читатель истории изменений homebrew контента"""
    
    def get_by_entity(self, entity_id: int) -> List[HomebrewEdit]:
        edits = HomebrewEdits.objects.filter(
            entity_id=entity_id
        ).order_by('-version_number')
        
        return [
            HomebrewEdit(
                edit_id=e.edit_id,
                entity_id=e.entity_id,
                edit_date=e.edit_date,
                version_number=e.version_number
            ) for e in edits
        ]
    
    def get_latest_version(self, entity_id: int) -> Optional[HomebrewEdit]:
        latest = HomebrewEdits.objects.filter(
            entity_id=entity_id
        ).order_by('-version_number').first()
        
        if latest:
            return HomebrewEdit(
                edit_id=latest.edit_id,
                entity_id=latest.entity_id,
                edit_date=latest.edit_date,
                version_number=latest.version_number
            )
        return None


class DjangoHomebrewModerationReader(IHomebrewModerationReader):
    """Читатель истории модерации"""
    
    def get_by_entity(self, entity_id: int) -> List[HomebrewModeration]:
        records = HomebrewModerations.objects.filter(
            entity_id=entity_id
        ).order_by('-moderation_date')
        
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