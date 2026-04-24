from dataclasses import dataclass
from typing import Optional
from business.interfaces.repositories import IHomebrewRepository
from .can_user_view_homebrew_use_case import CanUserViewHomebrewUseCase

@dataclass
class RecordViewResult:
    """Результат записи просмотра"""
    success: bool
    entity_id: int
    user_id: int
    error_message: Optional[str] = None


class RecordHomebrewViewUseCase:
    """
    Use Case: Запись просмотра контента.
    
    Бизнес-правила:
    - Просмотр записывается только если пользователь имеет право просмотра
    - Запись используется для аналитики
    """
    
    def __init__(
        self, 
        homebrew_repository: IHomebrewRepository,
        can_view_use_case: CanUserViewHomebrewUseCase
    ):
        self.homebrew_repository = homebrew_repository
        self.can_view_use_case = can_view_use_case
    
    def execute(
        self, 
        user_id: int, 
        user_role: str, 
        entity_id: int
    ) -> RecordViewResult:
        """
        Записать просмотр контента.
        
        Args:
            user_id: ID пользователя
            user_role: Роль пользователя
            entity_id: ID контента
            
        Returns:
            RecordViewResult с результатом операции
        """
        # Проверяем существование контента
        homebrew = self.homebrew_repository.get_by_id(entity_id)
        
        if not homebrew:
            return RecordViewResult(
                success=False,
                entity_id=entity_id,
                user_id=user_id,
                error_message=f"Homebrew #{entity_id} not found"
            )
        
        # Проверяем права просмотра
        can_view = self.can_view_use_case.execute(user_id, user_role, homebrew)
        
        if not can_view:
            return RecordViewResult(
                success=False,
                entity_id=entity_id,
                user_id=user_id,
                error_message="User does not have permission to view this content"
            )
        
        # Записываем просмотр
        self.homebrew_repository.add_view(user_id, entity_id)
        
        return RecordViewResult(
            success=True,
            entity_id=entity_id,
            user_id=user_id
        )