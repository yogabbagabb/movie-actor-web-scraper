from unittest import TestCase
from movie_actor_app.scraper.Scraper import *


class TestScraper(TestCase):

    # def test_get_actors_movies(self):
    #     scraper = Scraper()
    #     expected_output = False
    #     self.assertEqual(expected_output, scraper.get_stars_of_movie(3, "Mulan"))
    #     expected_output = "[<a href=\"/wiki/The_Martian_(film)\" title=\"The Martian (film)\">The Martian</a>," \
    #                       " <a href=\"/wiki/Mystic_Pizza\" title=\"Mystic Pizza\">Mystic Pizza</a>," \
    #                       " <a href=\"/wiki/The_Rainmaker_(1997_film)\" title=\"The Rainmaker (1997 film)\">The " \
    #                       "Rainmaker</a>]"
    #     movie_list = scraper.get_movies_of_actor(3, "Matt Damon")
    #     movie_list = list(map(lambda x : "" + x, movie_list))
    #     actual_output = "[" + movie_list[0] +"," + movie_list[1] + "," + movie_list[2] + "]"
    #     self.assertEqual(expected_output,actual_output)
    #     # self.assertEqual(expected_output.strip("\n").strip("\r"), scraper.get_movies_of_actor(3, "Matt Damon").strip("\n").strip("\r"))

    def test_get_attributes(self):
        scraper = Scraper()
        soup = scraper.get_soup_from_name("Crouching Tiger, Hidden Dragon", "")
        expected_output = {'year': 2000, 'grossing_amt': 213.5}
        self.assertEqual(expected_output,scraper.get_attributes(soup, is_actor=False))

        scraper = Scraper()
        soup = scraper.get_soup_from_name("300 (film)", "")
        expected_output = {'year': 2006, 'grossing_amt': 456.1}
        self.assertEqual(expected_output,scraper.get_attributes(soup, is_actor=False))

        scraper = Scraper()
        soup = scraper.get_soup_from_name("Matt Damon", "")
        expected_output = {'age': 47}
        self.assertEqual(expected_output, scraper.get_attributes(soup, is_actor=True))

    def test_add_to_queue(self):
        scraper = Scraper()
        movie_stars = scraper.get_stars_of_movie(3, "Invictus (film)")
        movies_of_actor = scraper.get_movies_of_actor(3, "Matt Damon")

        scraper.add_to_queue(movie_stars, parent_record=MovieRecord("Invictus", Type.MOVIE), parent_is_actor=False)
        while not scraper.pending_nodes.empty():
            print(scraper.pending_nodes.get_nowait())

        scraper.add_to_queue(movies_of_actor, parent_record=ActorRecord("Matt Damon", Type.ACTOR), parent_is_actor=True)
        while not scraper.pending_nodes.empty():
            print(scraper.pending_nodes.get_nowait())

    # def test_apportion_contracts(self):
    #     self.fail()
