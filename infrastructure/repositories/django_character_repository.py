from typing import List, Optional
from django.utils import timezone
from django.db import transaction
from core.models import Characters, CharacterEdits
from business.entities.character import Character
from business.interfaces.repositories import ICharacterRepository
from business.value_objects import CharacterEdit


class DjangoCharacterRepository(ICharacterRepository):
    """Реализация репозитория персонажей"""
    
    def get_by_id(self, character_id: int) -> Optional[Character]:
        try:
            char_model = Characters.objects.select_related('user', 'system').get(
                character_id=character_id
            )
            return Character(
                character_id=char_model.character_id,
                user_id=char_model.user_id,
                system_id=char_model.system_id,
                created_date=char_model.created_date,
                last_modified_date=char_model.last_modified_date
            )
        except Characters.DoesNotExist:
            return None
    
    def get_by_user(self, user_id: int) -> List[Character]:
        chars = Characters.objects.filter(user_id=user_id).order_by('-created_date')
        return [
            Character(
                character_id=c.character_id,
                user_id=c.user_id,
                system_id=c.system_id,
                created_date=c.created_date,
                last_modified_date=c.last_modified_date
            ) for c in chars
        ]
    
    @transaction.atomic
    def create(self, user_id: int, system_id: int, name: Optional[str] = None) -> Character:
        now = timezone.now()
        char_model = Characters.objects.create(
            user_id=user_id,
            system_id=system_id,
            created_date=now,
            last_modified_date=now
        )
        
        
        return Character(
            character_id=char_model.character_id,
            user_id=user_id,
            system_id=system_id,
            created_date=now,
            last_modified_date=now
        )
    
    def update(self, character: Character) -> None:
        Characters.objects.filter(character_id=character.character_id).update(
            system_id=character.system_id,
            last_modified_date=character.last_modified_date
        )
    
    def delete(self, character_id: int) -> bool:
        deleted, _ = Characters.objects.filter(character_id=character_id).delete()
        return deleted > 0
    
    def add_edit_history(self, character_id: int, edit_type: str) -> None:
        CharacterEdits.objects.create(
            character_id=character_id,
            edit_date=timezone.now(),
            edit_type=edit_type
        )
    
    def get_edit_history(self, character_id: int) -> List[CharacterEdit]:
        edits = CharacterEdits.objects.filter(character_id=character_id).order_by('-edit_date')
        return [
            CharacterEdit(
                edit_id=e.edit_id,
                character_id=e.character_id,
                edit_date=e.edit_date,
                edit_type=e.edit_type
            ) for e in edits
        ]