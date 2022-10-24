import logging

from django.test import TestCase

from ..helpers.crawler import Crawler
from ..models import Ability, Pokemon
from .test_data import POKEMON_1_DETAIL

logger = logging.getLogger("test")


class CrawlerTest(TestCase):
    def setUp(self):
        self.crawler = Crawler(logger)

    def test_create_or_update_pokemon(self):
        test_data = POKEMON_1_DETAIL
        test_data["name"] = "bulbasaur"
        self.crawler.create_or_update_pokemon(test_data)

        pokemon = Pokemon.objects.get(name="bulbasaur")

        self.assertEqual(pokemon.height, POKEMON_1_DETAIL["height"])
        self.assertEqual(pokemon.weight, POKEMON_1_DETAIL["weight"])
        self.assertEqual(pokemon.stats, POKEMON_1_DETAIL["stats"])
        self.assertEqual(pokemon.sprite, POKEMON_1_DETAIL["sprites"]["back_default"])

        abilities = Ability.objects.all()

        self.assertEqual(len(abilities), len(POKEMON_1_DETAIL["abilities"]))
        for ability in abilities:
            self.assertIn(ability, pokemon.abilities.all())
