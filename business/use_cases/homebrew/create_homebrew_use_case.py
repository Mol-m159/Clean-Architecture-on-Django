from dataclasses import dataclass
from typing import Optional
from business.entities.homebrew import Homebrew, HomebrewType, HomebrewStatus
from business.interfaces.repositories import IHomebrewRepository


@dataclass
class CreateHomebrewResult:
    """Результат создания контента"""
    success: bool
    homebrew: Optional[Homebrew]
    error_message: Optional[str] = None


class CreateHomebrewUseCase:
    """
    Use Case: Создание нового homebrew контента.
    
    Бизнес-правила:
    - Контент создается в статусе DRAFT
    - Создается первая версия (version_number = 1)
    """
    
    def __init__(self, homebrew_repository: IHomebrewRepository):
        self.homebrew_repository = homebrew_repository
    
    def execute(
        self, 
        author_id: int, 
        system_id: int, 
        entity_type: str
    ) -> CreateHomebrewResult:
        """
        Создать новый контент.
        
        Args:
            author_id: ID автора
            system_id: ID игровой системы
            entity_type: Тип контента ('spell', 'item', 'class', 'race', 'other')
            
        Returns:
            CreateHomebrewResult с созданным контентом
        """
        # Преобразуем строку в Enum
        try:
            homebrew_type = HomebrewType.from_string(entity_type)
        except ValueError:
            homebrew_type = HomebrewType.OTHER
        
        try:
            # Создаем контент
            homebrew = self.homebrew_repository.create(
                author_id, system_id, homebrew_type
            )
            
            # Добавляем первую версию
            self.homebrew_repository.add_edit_version(
                homebrew.entity_id, 
                version_number=1
            )
            
            return CreateHomebrewResult(
                success=True,
                homebrew=homebrew
            )
            
        except Exception as e:
            return CreateHomebrewResult(
                success=False,
                homebrew=None,
                error_message=f"Failed to create homebrew: {str(e)}"
            )