from django.views.generic import ListView

from .models import Pokemon


class PokemonList(ListView):
    model = Pokemon
    template_name = "pokemon_list.html"
    paginate_by = 30
    ordering = ["sprite"]
