import os

from django.apps import AppConfig


class PokemonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pokemon"

    def ready(self):
        if os.environ.get("RUN_MAIN"):
            from .tasks import catch_pokemon

            catch_pokemon.delay()
