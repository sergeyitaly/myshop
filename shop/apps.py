from django.apps import AppConfig
from django.core.management import call_command


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    def ready(self):
        import shop.signals
