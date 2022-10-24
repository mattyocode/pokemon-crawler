from celery import shared_task
from celery.utils.log import get_task_logger

from .helpers.crawler import Crawler

logger = get_task_logger(__name__)


@shared_task(bind=True)
def catch_pokemon(self):
    logger.info("*** Catching pokemon!!! ***")
    crawler = Crawler(logger)
    crawler.get_all_pokemon()
    logger.info("*** Finished catching pokemon!!! ***")
