# Pokemon Challenge

## How to install and run

1. Clone from Github

	 ```bash
	 cd <projects>
	 git clone <repo-tag>
	 cd pokemon-crawler
	 ```

2. Launch Docker containers

	 ```bash
	 docker-compose up
	 ```

Once launched, requirements will be installed, Django migrations will be applied, then Celery should launch and begin catching Pokemon after a few moments.

3. Run tests

	 ```bash
	 docker-compose exec web ./manage.py test
	 ```

4. Visit the frontend

Once Pokemon and Ability objects have started to populate the database, you can visit the 'Pokemon Zoo' (a hastily put together frontend) at `localhost:8000`.

## Explainer/Thoughts

To stay more or less within the stated timeframe, the design is simple - abstracting the PokeAPI interaction and crawling to helper modules and using a class-based ListView to display the captured Pokemon visually.

I'm enthusiastic about testing, and test drove the PokeAPI class, but took the decision to test more lightly elsewhere. I'd add more tests given more time and implement a clear separation between unit tests and integration tests.

Celery is currently handling catching Pokemon regularly, and this could be deployed as auto-scaling EC2 workers or Lambda tasks if a more robust and up-to-date reflection of Pokemon activity and attributes was necessary. A VPC with a greater range of IP addresses would also help with rate limiting.

The frontend is in need of a lot of work (but hopefully has a little charm in a gRaPhIc DesIgN iS mY paSSiOn sort of way...). With more time and with an eye on scaling, I'd separate the front- and backends, serving data from a REST API and consuming it with a bit more style and functionality on the frontend.

Overall, this was really fun to do - and I'm now much more aware of the diversity in the Pokemon world! :grin:

## TO DO (Key points)

- Increase test coverage.
- Set up CI processes to run tests and linting on pushes/PRs.
- Refactor crawler - moving away from the large number of database hits currently used to populate/update the Abilities many-to-many field.
- Hide secrets currently in Django settings/transfer more values to env variables.
- Move to independent database, i.e. not just persisting data in Docker volume.