from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from business.entities.user import User, UserRole
from business.entities.character import Character
from business.entities.homebrew import Homebrew, HomebrewStatus, HomebrewType
from business.value_objects import CharacterEdit, HomebrewEdit, HomebrewModeration


class IUserRepository(ABC):
      
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID. Возвращает None, если не найден."""
        pass
    
    @abstractmethod
    def get_role(self, user_id: int) -> Optional[str]:
        """Получить роль пользователя."""
        pass
    
    @abstractmethod
    def update_last_activity(self, user_id: int) -> None:
        """Обновить дату последней активности пользователя."""
        pass
    
    @abstractmethod
    def exists(self, user_id: int) -> bool:
        """Проверить, существует ли пользователь."""
        pass


class ICharacterRepository(ABC):
       
    @abstractmethod
    def get_by_id(self, character_id: int) -> Optional[Character]:
        """Получить персонажа по ID. Возвращает None, если не найден."""
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Character]:
        """Получить всех персонажей пользователя."""
        pass
    
    @abstractmethod
    def create(self, user_id: int, system_id: int, name: Optional[str] = None) -> Character:
        """
        Создать нового персонажа.
        Возвращает созданную сущность Character.
        """
        pass
    
    @abstractmethod
    def update(self, character: Character) -> None:
        """Обновить персонажа."""
        pass
    
    @abstractmethod
    def delete(self, character_id: int) -> bool:
        """Удалить персонажа. Возвращает True, если удален."""
        pass
    
    # История изменений
    @abstractmethod
    def add_edit_history(self, character_id: int, edit_type: str) -> None:
        """Добавить запись в историю изменений персонажа."""
        pass
    
    @abstractmethod
    def get_edit_history(self, character_id: int) -> List[CharacterEdit]:
        """Получить историю изменений персонажа."""
        pass


class IHomebrewRepository(ABC):
       
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[Homebrew]:
        """Получить контент по ID."""
        pass
    
    @abstractmethod
    def get_by_author(self, author_id: int) -> List[Homebrew]:
        """Получить весь контент автора."""
        pass
    
    @abstractmethod
    def get_by_status(self, status: HomebrewStatus) -> List[Homebrew]:
        """Получить контент по статусу."""
        pass
    

    @abstractmethod
    def add_moderation_record(
        self, 
        entity_id: int, 
        moderator_id: int, 
        old_status: HomebrewStatus, 
        new_status: HomebrewStatus
    ) -> None:
        """Добавить запись в историю модерации."""
        pass

    @abstractmethod
    def get_moderation_history(self, entity_id: int) -> List[HomebrewModeration]:
        """Получить историю модерации контента."""
        pass
    
    @abstractmethod
    def create(
        self,
        author_id: int,
        system_id: int,
        entity_type: HomebrewType,
    ) -> Homebrew:
        """
        Создать новый homebrew контент в статусе DRAFT.
        Возвращает созданную сущность.
        """
        pass
    
    @abstractmethod
    def update(self, homebrew: Homebrew) -> None:
        """Обновить контент."""
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Удалить контент. Возвращает True, если удален."""
        pass

    @abstractmethod
    def add_edit_version(self, entity_id: int) -> None:
        """
        Добавить новую версию в историю изменений.
        """
        pass
    @abstractmethod
    def get_edit_history(self, entity_id: int) -> List[HomebrewEdit]:
        """Получить историю версий контента."""
        pass

    @abstractmethod
    def get_latest_version(self, entity_id: int) -> Optional[HomebrewEdit]:
        """Получить последнюю версию."""
        pass

    @abstractmethod
    def add_view(self, user_id: int, entity_id: int) -> None:
        """Записать просмотр контента."""
        pass

    @abstractmethod
    def get_view_count(self, entity_id: int) -> int:
        """Получить количество просмотров."""
        pass


class IModerationRepository(ABC):
    """Интерфейс репозитория для модерации"""
    
    @abstractmethod
    def get_moderation_queue(self, sort_by_date_asc: bool = True) -> List[Homebrew]:
        """Получить очередь на модерацию (статус MODERATION)."""
        pass
    
    @abstractmethod
    def get_moderation_queue_with_days(self) -> List[dict]:
        """
        Получить очередь с количеством дней в очереди.
        Возвращает список словарей: {'homebrew': Homebrew, 'days_in_queue': int}
        """
        pass
    
    @abstractmethod
    def approve(self, entity_id: int, moderator_id: int) -> None:
        """
        Одобрить контент.
        Обновляет статус и добавляет запись в историю модерации.
        """
        pass
    
    @abstractmethod
    def reject(self, entity_id: int, moderator_id: int, reason: Optional[str] = None) -> None:
        """
        Отклонить контент.
        Обновляет статус и добавляет запись в историю модерации.
        """
        pass
    
    @abstractmethod
    def get_moderation_history(self, entity_id: int) -> List[HomebrewModeration]:
        """Получить историю модерации контента."""
        pass
    
    @abstractmethod
    def get_moderator_stats(self, moderator_id: int) -> dict:
        """
        Получить статистику работы модератора.
        Возвращает словарь с полями:
        - total_moderated: int — всего проверено
        - approved: int — одобрено
        - rejected: int — отклонено
        - last_moderation_date: datetime — дата последней проверки
        """
        pass
    
    @abstractmethod
    def get_all_moderators_stats(self) -> List[dict]:
        """Получить статистику по всем модераторам."""
        pass



    