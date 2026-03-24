from django.apps import AppConfig


class PharmacistConfig(AppConfig):
    name = 'pharmacist'
class PharmacistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pharmacist'

    def ready(self):
        import pharmacist.signals