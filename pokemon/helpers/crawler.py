from django.db import transaction
from requests.exceptions import HTTPError, SSLError

from ..models import Ability, Pokemon
from .pokeapi import PokeAPI


class Crawler:
    def __init__(self, logger):
        self.api = PokeAPI()
        self.logger = logger

    def get_all_pokemon(self):
        available_pokemon = self.api.get_available_pokemon()

        with transaction.atomic():
            for pokemon in available_pokemon:
                try:
                    pokemon_data = self.api.get_pokemon_data(pokemon)
                    self.create_or_update_pokemon(pokemon_data)
                except (HTTPError, SSLError) as e:
                    self.logger.error(f"*** Error occurred catching {pokemon}: {e} ***")

    def create_or_update_pokemon(self, data):
        """
        Task helper to deal with adding/updating Pokemon and Abilities.
        """
        try:
            pokemon_obj, created = Pokemon.objects.get_or_create(name=data["name"])

            updated_abilities = []
            for ability in data["abilities"]:
                updated_abilities.append(Ability.objects.get_or_create(name=ability["ability"]["name"])[0])
            pokemon_obj.abilities.set(updated_abilities)

            pokemon_obj.height = data["height"]
            pokemon_obj.weight = data["weight"]
            pokemon_obj.stats = data["stats"]
            pokemon_obj.sprite = data["sprites"]["back_default"]
            pokemon_obj.save()

            if created:
                self.logger.info(f"*** Caught {pokemon_obj.name} ***")
            else:
                self.logger.info(f"*** Updated {pokemon_obj.name} ***")

        except KeyError as e:
            self.logger.error(f'KeyError when adding {data["name"]}: {e}')
