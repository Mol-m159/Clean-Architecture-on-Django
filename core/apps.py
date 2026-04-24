
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Core Application'
    
    def ready(self):
        """
        Инициализация DI контейнера при запуске Django.
        Это позволяет использовать use cases во всех views.
        """
        from infrastructure.di_config import init_container
        container = init_container()
        
        import logging
        logger = logging.getLogger(__name__)
        logger.info("DI Container initialized successfully")