from django.apps import AppConfig

class Blog2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog2'

    def ready(self):
        import blog2.signals  # This line is important
