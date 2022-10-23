from django.urls import path

from .views import PokemonList

urlpatterns = [
    path("", PokemonList.as_view()),
]
