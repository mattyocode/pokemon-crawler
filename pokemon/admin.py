from django.contrib import admin

from .models import Pokemon


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "height",
        "weight",
        "stats",
        "sprite",
    )
    list_display = (
        "name",
        "height",
        "weight",
        "stats",
        "sprite",
    )

    def get_abilities(self, instance):
        return [ability.name for ability in instance.ability.all()]
