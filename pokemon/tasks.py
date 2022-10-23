from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction
from requests.exceptions import HTTPError, SSLError

from .helpers.pokeapi import PokeAPI
from .models import Ability, Pokemon

logger = get_task_logger(__name__)


@shared_task
def catch_pokemon():
    logger.info("*** Catching pokemon!!! ***")
    api = PokeAPI()
    available_pokemon = api.get_available_pokemon()
    with transaction.atomic():
        for pokemon in available_pokemon:
            try:
                pokemon_data = api.get_pokemon_data(pokemon)
                create_or_update_pokemon(pokemon_data)
            except (HTTPError, SSLError) as e:
                logger.error(f"*** Error occurred catching {pokemon}: {e} ***")

    logger.info("*** Finished catching pokemon!!! ***")


def create_or_update_pokemon(data):
    """Task helper to deal with adding/updating Pokemon and Abilities.
    This method of adding the m-2-m Ability objects requires a lot
    of hitting the database, and should be refactored.
    """
    try:
        pokemon_obj, created = Pokemon.objects.get_or_create(name=data["name"])

        abilities = []
        for ability in data["abilities"]:
            abilities.append(
                Ability.objects.get_or_create(name=ability["ability"]["name"])[0]
            )
        pokemon_obj.abilities.set(abilities)

        pokemon_obj.height = data["height"]
        pokemon_obj.weight = data["weight"]
        pokemon_obj.stats = data["stats"]
        pokemon_obj.sprite = data["sprites"]["back_default"]
        pokemon_obj.save()

        if created:
            logger.info(f"*** Caught {pokemon_obj.name} ***")
        else:
            logger.info(f"*** Updated {pokemon_obj.name} ***")

    except KeyError as e:
        logger.error(f'KeyError when adding {data["name"]}: {e}')
