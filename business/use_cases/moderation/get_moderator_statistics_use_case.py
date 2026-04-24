from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from business.interfaces.repositories import IModerationRepository

@dataclass
class ModeratorStats:
    """Статистика работы модератора"""
    moderator_id: int
    total_moderated: int      # всего проверено
    approved: int             # одобрено
    rejected: int             # отклонено
    approval_rate: float      # процент одобрений
    last_moderation_date: Optional[datetime]
    
    @property
    def rejection_rate(self) -> float:
        """Процент отклонений"""
        if self.total_moderated == 0:
            return 0.0
        return (self.rejected / self.total_moderated) * 100


@dataclass
class ModeratorStatsResult:
    """Результат получения статистики модератора"""
    success: bool
    stats: Optional[ModeratorStats]
    error_message: Optional[str] = None


@dataclass
class AllModeratorsStatsResult:
    """Результат получения статистики всех модераторов"""
    success: bool
    stats: List[ModeratorStats]
    total_moderators: int
    total_moderations: int
    error_message: Optional[str] = None


class GetModeratorStatisticsUseCase:
    """
    Use Case: Получение статистики работы модератора.
    
    Используется для:
    - Отображения эффективности работы модератора
    - Административной панели
    """
    
    def __init__(self, moderation_repository: IModerationRepository):
        self.moderation_repository = moderation_repository
    
    def execute_for_moderator(self, moderator_id: int) -> ModeratorStatsResult:
        """
        Получить статистику для конкретного модератора.
        
        Args:
            moderator_id: ID модератора
            
        Returns:
            ModeratorStatsResult со статистикой
        """
        try:
            stats_data = self.moderation_repository.get_moderator_stats(moderator_id)
            
            if not stats_data:
                return ModeratorStatsResult(
                    success=True,
                    stats=ModeratorStats(
                        moderator_id=moderator_id,
                        total_moderated=0,
                        approved=0,
                        rejected=0,
                        approval_rate=0.0,
                        last_moderation_date=None
                    )
                )
            
            total = stats_data.get('total_moderated', 0)
            approved = stats_data.get('approved', 0)
            approval_rate = (approved / total * 100) if total > 0 else 0.0
            
            stats = ModeratorStats(
                moderator_id=moderator_id,
                total_moderated=total,
                approved=approved,
                rejected=stats_data.get('rejected', 0),
                approval_rate=approval_rate,
                last_moderation_date=stats_data.get('last_moderation_date')
            )
            
            return ModeratorStatsResult(
                success=True,
                stats=stats
            )
            
        except Exception as e:
            return ModeratorStatsResult(
                success=False,
                stats=None,
                error_message=f"Failed to get moderator stats: {str(e)}"
            )
    
    def execute_for_all(self) -> AllModeratorsStatsResult:
        """
        Получить статистику для всех модераторов.
        
        Returns:
            AllModeratorsStatsResult со статистикой по всем модераторам
        """
        try:
            all_stats_data = self.moderation_repository.get_all_moderators_stats()
            
            stats_list = []
            total_moderations = 0
            
            for data in all_stats_data:
                moderator_id = data.get('moderator_id')
                total = data.get('total_moderated', 0)
                approved = data.get('approved', 0)
                approval_rate = (approved / total * 100) if total > 0 else 0.0
                
                total_moderations += total
                
                stats_list.append(ModeratorStats(
                    moderator_id=moderator_id,
                    total_moderated=total,
                    approved=approved,
                    rejected=data.get('rejected', 0),
                    approval_rate=approval_rate,
                    last_moderation_date=data.get('last_moderation_date')
                ))
            
            # Сортируем по количеству проверок (убывание)
            stats_list.sort(key=lambda x: x.total_moderated, reverse=True)
            
            return AllModeratorsStatsResult(
                success=True,
                stats=stats_list,
                total_moderators=len(stats_list),
                total_moderations=total_moderations
            )
            
        except Exception as e:
            return AllModeratorsStatsResult(
                success=False,
                stats=[],
                total_moderators=0,
                total_moderations=0,
                error_message=f"Failed to get all moderators stats: {str(e)}"
            )