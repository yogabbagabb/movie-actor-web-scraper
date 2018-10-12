import time
import logging
import code
from movie_actor_app.scraper.Scraper import Scraper


if __name__ == "__main__":
    logging.basicConfig(filename='scraper.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info("\n\n\nStarting\n\n\n")

    t0 = time.time()
    scraper = Scraper(movie_degree=8, actor_degree=20)
    scraper.query("Matt Damon", is_actor=True, actor_limit=5, movie_limit=5)
    print(time.time() - t0)
    code.interact(local=locals())

    # t0 = time.time()
    # scraper = Scraper(movie_degree=8, actor_degree=20)
    # scraper.query("Morgan Freeman", is_actor=True, actor_limit=251, movie_limit=126)
    # print(time.time() - t0)
    # code.interact(local=locals())


