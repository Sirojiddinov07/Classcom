from django.apps import AppConfig


class ClassComConfig(AppConfig):
<<<<<<< HEAD
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.apps.classcom"
=======
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.apps.classcom'

    def ready(self):
        from .signals import signals
        
>>>>>>> origin/dev
