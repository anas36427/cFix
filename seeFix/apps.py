from django.apps import AppConfig
from mongoengine import connect


class SeefixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seeFix'

    def ready(self):
        # Connect to MongoDB when the app is ready (placeholder - update with real credentials)
        # connect('cfix_db', host='mongodb+srv://<username>:<password>@<cluster>.mongodb.net/')
        pass  # Temporarily disabled MongoDB connection
