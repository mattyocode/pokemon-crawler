import urllib

import requests
from requests.exceptions import HTTPError


class PokeAPI:
    """Class to handle fetching data from PokeAPI."""

    PROTOCOL = "https"
    URL_BASE = "pokeapi.co/api/v2"
    POKEMON_ENDPOINT = "pokemon"

    def get_available_pokemon(self):
        count = self.get_pokemon_count()
        number_of_pokemon = {"limit": count}
        url = self.get_url(path=self.POKEMON_ENDPOINT, params=number_of_pokemon)
        response = requests.get(url)
        data = self.json_if_status_code_equals(response)
        results = data.get("results", [])
        return [pokemon["name"] for pokemon in results]

    def get_pokemon_data(self, name):
        url = self.get_url(f"{self.POKEMON_ENDPOINT}/{name}")
        response = requests.get(url)
        data = self.json_if_status_code_equals(response)
        return data

    def get_results_count(self, endpoint):
        url = self.get_url(endpoint)
        response = requests.get(url)
        data = self.json_if_status_code_equals(response)
        count = data.get("count", 0)
        return count

    def get_pokemon_count(self):
        return self.get_results_count(self.POKEMON_ENDPOINT)

    def get_url(self, path="", params=None):
        base = f"{self.PROTOCOL}://{self.URL_BASE}/{path}"
        if params:
            return f"{base}?{urllib.parse.urlencode(params)}"
        return base

    def json_if_status_code_equals(self, response, status_code=200):
        if response.status_code == status_code:
            return response.json()
        raise HTTPError(f"Non-{status_code} status code from PokeAPI.")
