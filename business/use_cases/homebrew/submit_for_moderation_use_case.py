from dataclasses import dataclass
from typing import Optional
from business.entities.homebrew import Homebrew, HomebrewStatus
from business.interfaces.repositories import IHomebrewRepository


@dataclass
class SubmitModerationResult:
    """Результат отправки на модерацию"""
    success: bool
    homebrew: Optional[Homebrew]
    error_message: Optional[str] = None


class SubmitHomebrewForModerationUseCase:
    """
    Use Case: Отправка контента на модерацию.
    
    Бизнес-правила (из homebrew.py):
    - Отправить можно только DRAFT или REJECTED контент
    - После отправки статус становится MODERATION
    """
    
    def __init__(self, homebrew_repository: IHomebrewRepository):
        self.homebrew_repository = homebrew_repository
    
    def execute(self, entity_id: int) -> SubmitModerationResult:
        """
        Отправить контент на модерацию.
        
        Args:
            entity_id: ID контента
            
        Returns:
            SubmitModerationResult с обновленным контентом
        """
        # Получаем контент
        homebrew = self.homebrew_repository.get_by_id(entity_id)
        
        if not homebrew:
            return SubmitModerationResult(
                success=False,
                homebrew=None,
                error_message=f"Homebrew #{entity_id} not found"
            )
        
        # Используем бизнес-правило из сущности
        try:
            homebrew.submit_for_moderation()
        except ValueError as e:
            return SubmitModerationResult(
                success=False,
                homebrew=homebrew,
                error_message=str(e)
            )
        
        # Сохраняем изменения
        self.homebrew_repository.update(homebrew)
        
        return SubmitModerationResult(
            success=True,
            homebrew=homebrew
        )