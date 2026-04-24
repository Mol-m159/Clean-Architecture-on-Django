from dataclasses import dataclass
from typing import Optional
from business.interfaces.readers import ISessionStatisticsReader


@dataclass
class TerminateSessionResult:
    """Результат принудительного завершения сессии"""
    success: bool
    session_id: int
    error_message: Optional[str] = None


class TerminateSessionUseCase:
    """
    Use Case: Принудительное завершение сессии.
    
    Бизнес-правила:
    - Завершить можно только активную сессию
    - Устанавливается logout_date = текущее время
    - Используется администраторами для принудительного выхода пользователя
    """
    
    def __init__(self, session_stats_reader: ISessionStatisticsReader):
        self.session_stats_reader = session_stats_reader
    
    def execute(self, session_id: int) -> TerminateSessionResult:
        """
        Принудительно завершить сессию.
        
        Args:
            session_id: ID сессии
            
        Returns:
            TerminateSessionResult с результатом операции
        """
        try:
            success = self.session_stats_reader.terminate_session(session_id)
            
            if success:
                return TerminateSessionResult(
                    success=True,
                    session_id=session_id
                )
            else:
                return TerminateSessionResult(
                    success=False,
                    session_id=session_id,
                    error_message=f"Session #{session_id} not found or already terminated"
                )
        except Exception as e:
            return TerminateSessionResult(
                success=False,
                session_id=session_id,
                error_message=str(e)
            )