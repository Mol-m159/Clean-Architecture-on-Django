# business/use_cases/homebrew/get_homebrew_view_count_use_case.py
from typing import Optional
from business.interfaces.repositories import IHomebrewRepository


class GetHomebrewViewCountUseCase:
    """Use case для получения количества просмотров homebrew контента"""
    
    def __init__(self, homebrew_repository: IHomebrewRepository):
        self.homebrew_repository = homebrew_repository
    
    def execute(self, entity_id: int) -> int:
        return self.homebrew_repository.get_view_count(entity_id)