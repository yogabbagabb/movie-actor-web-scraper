from bs4 import BeautifulSoup
from movie_actor_app.graphs.Graph import *
import urllib.request
import logging
import queue
import code


class Utilities(object):

    @staticmethod
    def is_movie(tag):
        return tag.name == "a" and tag.parent.name == "i" and tag.has_attr("href") and tag.has_attr("title")

    @staticmethod
    def is_filmography_section_strict(tag):
        return tag.has_attr("href") and "filmography" in tag["href"].lower() and "wiki" in tag["href"].lower() \
               and tag.has_attr("rel") and "https" in tag["href"]

    @staticmethod
    def is_filmography_section(tag):
        return tag.has_attr("href") and "filmography" in tag["href"].lower() and "wiki" in tag["href"].lower()

    @staticmethod
    def has_starring_tag(tag):
        return tag.string == "Starring"


class Scraper(object):

    def __init__(self):
        self.graph = Graph()
        self.movie_num = 0
        self.actor_num = 0
        self.soup = None
        self.link_queue = queue.Queue()

    @staticmethod
    def __get_soup_from_url(name, final_string=""):
        """
        Get an instance of beautiful soup from the url corresponding to name
        :param name: The name of an actor or movie
        :param final_string: A string to be appended to name.
        :return: An instance of BeautifulSoup if BeautifulSoup is successful and false otherwise.
        """

        logging.info("Getting Soup From URL for {}".format(name))
        page = "https://en.wikipedia.org/wiki/"
        name = name.replace(" ", "_")

        page += (name + final_string)
        try:
            with urllib.request.urlopen(page) as url:
                html = url.read()
            soup = BeautifulSoup(html, 'lxml')
        except:
            soup = False
            logging.error("Connection to {} failed".format(name))
        finally:
            return soup

    def get_movies_of_actor(self, num, actor_name):
        """
        Get tags corresponding to movies in which an actor worked.
        :param num: A particular number of movie tags to scrape
        :return: A list of num tags
        """
        logging.info("Getting Movies that {} played in".format(actor_name))
        soup = self.__get_soup_from_url(actor_name, final_string="_filmography")
        try:
            movies = soup.find_all(Utilities.is_movie)
        except:
            logging.error("The actor's html structure did not meet our conventions")
            return
        if len(movies) < num:
            num = len(movies)
        return movies[0:num:1]

    def get_stars_of_movie(self, num, movie_name):
        """
        Get tags corresponding to actors that worked in a movie.
        :param num: A particular number of movie tags to scrape
        :return: A list of num tags
        """

        logging.info("Getting Actors that played in {}".format(movie_name))
        soup = self.__get_soup_from_url(movie_name, final_string="")
        try:
            starring_tag = soup.find(Utilities.has_starring_tag)
            starring_parent_tag = starring_tag.parent
            stars = starring_parent_tag.findChildren("a")
        except:
            logging.error("The movie's html structure did not meet our conventions")
            return
        if len(stars) < num:
            num = len(stars)
        return stars[0:num:1]

    def get_attributes(self, soup, is_actor):
        """
        Get the attributes of the object whose html tree has been parsed into soup
        :param soup: An instance of BeautifulSoup
        :param is_actor: Whether the object represented by soup is an actor
        :return: A dictionary of attributes to values for the object represented by soup or False if the attributes
        could not be scraped
        """

    def add_to_queue(self, tag_list, parent_record):
        """
        Add each url inside tag list to the queue along with its parent record
        :param tag_list: A list of tags; the list either exclusively contains tags referring to movies or to actors;
        each tag has an attribute title that can be used to construct a url.
        :param parent_record: The record (of an actor or movie) corresponding to the url from which tag_list was scraped
        :return: None
        """

    def apportion_contracts(self, movie_record, star_actors, parent_actor_record):
        """
        Distribute the profit of the movie corresponding to movie_record to the actors that worked in the movie. Each
        actor will subsequently have a contract.
        :param movie_record: The record of the movie whose profit is being split. We assume that movie_record has an
        initialized grossing_amt field.
        :param star_actors: A list of actors that worked in the movie corresponding to movie_record. We assume that
        these actors have already been added to the graph and had their fields initialized
        :param parent_actor_record: The record that, when scraped, led the scraper to progress to movie_record.
        :return: None
        """

    def run(self, actor_limit, movie_limit):
        """
        Run the scraper until we scrape movie_limit number of movies and actor_limit number of actors
        :return:
        """

    def run_round(self):
        """
        Take one element from the queue and scrape it.
        :return: num_actors_scraped, num_movies_scraped
        """

    def query(self, query_string, is_actor, actor_limit, movie_limit):
        """
        Initiate the scraper using query_string
        :param query_string: The name of the actor or movie that we will begin scraping at
        :param is_actor: True if query_string is the name of an actor; false otherwise
        :return: None
        """


if __name__ == "__main__":
    logging.basicConfig(filename='scraper.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("\n\n\nStarting\n\n\n")

    # page = "https://en.wikipedia.org/wiki/Matt_Damon_filmography"
    # page = "https://en.wikipedia.org/wiki/Matt_Damon"
    # page = "https://en.wikipedia.org/wiki/Morgan_Freeman"
    # page = "https://en.wikipedia.org/wiki/Ryan_Reynolds"
    # with urllib.request.urlopen(page) as url:
    #     html = url.read()
    # soup = BeautifulSoup(html, 'lxml')
    # print(soup.find_all(is_movie))
    # code.interact(local=locals())
    scraper = Scraper()
    print(scraper.get_stars_of_movie(3, "Mulan"))
    print(scraper.get_movies_of_actor(3, "Matt Damon"))
