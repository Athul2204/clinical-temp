from django.apps import AppConfig

class AdministrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'administration'

    def ready(self):
        # This imports the signals when Django starts
        import administration.signals