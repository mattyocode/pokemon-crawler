from unittest import mock

from django.test import TestCase
from requests.exceptions import HTTPError

from ..helpers.pokeapi import PokeAPI
from .test_data import POKEMON_1_DETAIL, POKEMON_LIST


# Helper function for mocking requests to PokeAPI
def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    received_url = args[0]
    pokemon_endpoint = "https://pokeapi.co/api/v2/pokemon"

    if "missing-keys" in received_url:
        return MockResponse({"badkey": "This is not the key you're looking for"}, 200)
    elif "not-found" in received_url:
        return MockResponse("Not Found", 404)
    elif "pokemon-name" in received_url:
        return MockResponse(POKEMON_1_DETAIL, 200)
    elif received_url.startswith(pokemon_endpoint):
        return MockResponse(POKEMON_LIST, 200)


class PokeAPITest(TestCase):
    """Tests for pokeapi.PokeAPI class."""

    def setUp(self):
        self.api = PokeAPI()

    def test_get_base_url(self):
        url = self.api.get_url()
        self.assertEqual(f"{self.api.PROTOCOL}://{self.api.URL_BASE}/", url)

    @mock.patch("requests.get", side_effect=mocked_requests)
    def test_get_results_count(self, mock_get):
        count = self.api.get_results_count(self.api.POKEMON_ENDPOINT)
        self.assertEqual(len(POKEMON_LIST["results"]), count)

    @mock.patch("requests.get", side_effect=mocked_requests)
    def test_get_results_count_missing_key(self, mock_get):
        count = self.api.get_results_count("missing-keys")
        self.assertEqual(0, count)

    @mock.patch("requests.get", side_effect=mocked_requests)
    def test_get_results_count_non_200_response(self, mock_get):
        with self.assertRaises(HTTPError):
            self.api.get_results_count("not-found")

    @mock.patch("requests.get", side_effect=mocked_requests)
    def test_get_available_pokemon(self, mock_get):
        result = self.api.get_available_pokemon()
        test_results = POKEMON_LIST["results"]
        for i in range(len(test_results)):
            self.assertEqual(POKEMON_LIST["results"][i]["name"], result[i])

    @mock.patch("requests.get", side_effect=mocked_requests)
    def test_get_available_pokemon_missing_key(self, mock_get):
        self.api.POKEMON_ENDPOINT = "missing-keys"
        result = self.api.get_available_pokemon()
        self.assertEqual(result, [])

    @mock.patch("requests.get", side_effect=mocked_requests)
    def test_get_available_pokemon_non_200_response(self, mock_get):
        self.api.POKEMON_ENDPOINT = "not-found"
        with self.assertRaises(HTTPError):
            self.api.get_available_pokemon()

    @mock.patch("requests.get", side_effect=mocked_requests)
    def test_get_pokemon_data(self, mock_get):
        result = self.api.get_pokemon_data("pokemon-name")
        self.assertEqual(POKEMON_1_DETAIL, result)

    @mock.patch("requests.get", side_effect=mocked_requests)
    def test_get_pokemon_data_non_200_response(self, mock_get):
        self.api.POKEMON_ENDPOINT = "not-found"
        with self.assertRaises(HTTPError):
            self.api.get_pokemon_data("pokemon-name")
