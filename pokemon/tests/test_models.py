from django.test import TestCase

from ..models import Ability, Pokemon
from .test_data import POKEMON_1_DETAIL


class ModelTest(TestCase):
    def test_ability_model(self):
        ability = Ability.objects.create(name="write tests")
        self.assertEqual(ability.name, "write tests")

    def test_pokemon_model(self):
        pokemon = Pokemon.objects.create(
            name="bulbasaur",
            height=POKEMON_1_DETAIL["height"],
            weight=POKEMON_1_DETAIL["weight"],
            stats=POKEMON_1_DETAIL["stats"],
            sprite=POKEMON_1_DETAIL["sprites"]["back_default"],
        )
        self.assertEqual(pokemon.name, "bulbasaur")
        self.assertEqual(pokemon.height, POKEMON_1_DETAIL["height"])
        self.assertEqual(pokemon.weight, POKEMON_1_DETAIL["weight"])
        self.assertEqual(pokemon.stats, POKEMON_1_DETAIL["stats"])
        self.assertEqual(pokemon.sprite, POKEMON_1_DETAIL["sprites"]["back_default"])

    def test_add_ability_to_pokemon(self):
        ability = Ability.objects.create(name="write tests")
        pokemon = Pokemon.objects.create(name="bulbasaur")
        pokemon.abilities.add(ability)
        self.assertIn(ability, pokemon.abilities.all())
