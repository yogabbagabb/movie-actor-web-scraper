from bs4 import BeautifulSoup
from movie_actor_app.graphs.Graph import *
from collections import namedtuple
import urllib.request
import logging
import queue
import code
import re

from movie_actor_app.graphs.Record import *

ParseRecord = namedtuple("ParseRecord", "name parent_record times_accessed_in_past")

logging.basicConfig(filename='scraper.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(lineno)d - %('
                                                                        'message)s')
logging.info("\n\n\nStarting\n\n\n")


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

    @staticmethod
    def is_age_tag(tag):
        return tag.has_attr("class") and tag.name == "span" and "noprint" in tag["class"]


class Scraper(object):

    def __init__(self, degree=3):
        self.graph = Graph()
        self.movie_num = 0
        self.actor_num = 0
        self.degree = degree
        self.soup = None
        self.pending_nodes = queue.Queue()
        logging.info("\n\n\nStarting\n\n\n")

    @staticmethod
    def get_soup_from_name(name, final_string=""):
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

    def get_movies_of_actor(self, num, actor_name, old_soup=None):
        """
        Get tags corresponding to movies in which an actor worked.
        :param old_soup: An old soup that was obtained for the actor if it exists
        :param num: A particular number of movie tags to scrape
        :return: A list of num tags, or False if we were unsuccessful
        """
        logging.info("Getting Movies that {} played in".format(actor_name))

        if old_soup is None:
            soup = self.get_soup_from_name(actor_name, final_string="_filmography")
            if not soup:
                return False
        else:
            soup = old_soup
        try:
            movies = soup.find_all(Utilities.is_movie)
        except:
            logging.error("The actor's html structure did not meet our conventions if an error did not take place "
                          "earlier")
            return False

        if len(movies) < num:
            num = len(movies)
        return movies[0:num:1]

    def get_stars_of_movie(self, num, movie_name, old_soup=None):
        """
        Get tags corresponding to actors that worked in a movie.
        :param old_soup: An old soup that was obtained for the movie, if it exists.
        :param num: A particular number of movie tags to scrape
        :return: A list of num tags
        """

        logging.info("Getting Actors that played in {}".format(movie_name))

        if old_soup is None:
            soup = self.get_soup_from_name(movie_name, final_string="")
            if not soup:
                return False
        else:
            soup = old_soup
        try:
            starring_tag = soup.find(Utilities.has_starring_tag)
            starring_parent_tag = starring_tag.parent
            stars = starring_parent_tag.findChildren("a")
        except:
            logging.error("The movie's html structure did not meet our conventions if an error did not take place "
                          "earlier")
            return False

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

        return self.__get_actor_attributes(soup) if is_actor else self.__get_movie_attributes(soup)

    @staticmethod
    def __get_movie_attributes(soup):
        try:
            # Get data somewhere near the Release date title
            release_date_tag = soup.find("div", string="Release date")
            parent_release_date_tag = release_date_tag.parent
            sibling = parent_release_date_tag.next_sibling
            release_date_tag = sibling.find(name="li")
            release_date_year = release_date_tag.next_element
            year = int(release_date_year.string[-4:])
            logging.info("The movie was released on {}".format(year))

            # Get data somewhere near the Box office title
            box_office_tag = soup.find("th", string="Box office")
            parent_box_office_tag = box_office_tag.parent
            child = parent_box_office_tag.find_next(name="td")
            child_string = str(child.next_element)

            # Pattern match for numbers following '$' and before any whitespace
            pattern_matcher = re.compile('\d\S*')
            box_office_amount = pattern_matcher.search(child_string)

            box_office_amount = float(box_office_amount.group())
            logging.info("The movie earned {}".format(box_office_amount))
        except:
            logging.error("We could not parse the movie's attributes")
            return False

        return {"year": year, "grossing_amt": box_office_amount}

    @staticmethod
    def __get_actor_attributes(soup):
        try:
            age_tag = soup.find(Utilities.is_age_tag)
            age_string = str(age_tag.string)
            pattern_matcher = re.compile('\d\d')
            age_data = (pattern_matcher.search(age_string).group())
        except:
            logging.error("We could not parse the actor's attributes")
            return False

        return {"age": int(age_data)}

    def add_to_queue(self, tag_list, parent_record, parent_is_actor):
        """
        Add each url inside tag list to the queue along with its parent record
        :param tag_list: A list of tags; the list either exclusively contains tags referring to movies or to actors;
        each tag has an attribute title that can be used to construct a url.
        :param parent_record: The record (of an actor or movie) corresponding to the url from which tag_list was scraped
        :param parent_is_actor: Whether the parent_record is an ActorRecord
        :return: None
        """
        for tag in tag_list:
            title = tag["title"]
            logging.info("{} added {} to the queue".format(parent_record.name, title))
            self.pending_nodes.put_nowait(ParseRecord(title, parent_record, 0))

        if not parent_is_actor:
            # If the parent is a movie, then after its actors have their fields instantiated, we
            # we need to give them salaries
            dummy_parent_record = Record("", Type.ACTOR)
            self.pending_nodes.put_nowait(ParseRecord(parent_record.name, dummy_parent_record, 1))

    def apportion_contracts(self, movie_record_name, parent_record):
        """
        Distribute the profit of the movie corresponding to movie_record to the actors that worked in the movie. Each
        actor will subsequently have a contract.
        :param movie_record_name: The name of the movie record whose actors will be given contracts to
        :param parent_record: The actor that, when scraped, led to the movie corresponding to movie_record_name
        :return: None
        """
        pass

    def run(self, actor_limit, movie_limit, first_is_actor):
        """
        Run the scraper until we scrape movie_limit number of movies and actor_limit number of actors
        :return:
        """
        actors_added, movies_added = self.run_round(is_first_round=True, first_is_actor=first_is_actor)
        self.actor_num += actors_added
        self.movie_num += movies_added
        while self.actor_num < actor_limit or self.movie_num < movie_limit:
            actors_added, movies_added = self.run_round()
            self.actor_num += actors_added
            self.movie_num += movies_added

    def run_round(self, is_first_round=False, first_is_actor=False):
        """
        Take one element from the queue and scrape it.
        :param is_first_round: Whether this is the first round being run
        :param first_is_actor: Whether the first query corresponds to an actor
        :return: num_actors_scraped, num_movies_scraped
        """
        logging.info("Now beginning a round where {} actors have been added and {} movies".format(self.actor_num,
                                                                                                  self.movie_num))
        current_record = self.pending_nodes.get_nowait()

        if is_first_round:
            parent_record = None
            is_actor = first_is_actor
        else:
            # current_record is an actor iff its parent was not an actor
            parent_record = current_record.parent_record
            parent_is_actor = parent_record.rec_type == Type.ACTOR
            is_actor = not parent_is_actor

        # Check to see whether the current record is a movie and, if so, whether we can allot salaries to its stars
        is_movie = not is_actor
        if is_movie and current_record.times_accessed_in_past > 0:
            self.apportion_contracts(current_record.name, parent_record)
            return 0, 0

        # Check to see whether the current record has already been added to the graph

        # Get the attributes of the record that will be represented by the name
        final_string = "" if is_actor else ""
        record_soup = self.get_soup_from_name(current_record.name, final_string=final_string)

        # If there was an error earlier in the code, skip this record
        if not record_soup:
            return 0, 0

        # Get the attributes for the current record
        record_attr = self.get_attributes(record_soup, is_actor)
        # If there was an error earlier in the code, skip this record
        if not record_attr:
            return 0, 0

        # Make a Record to add to the graph
        if is_actor:
            record_for_graph = ActorRecord(current_record.name, Type.ACTOR)
        else:
            record_for_graph = MovieRecord(current_record.name, Type.MOVIE)

        # Update the attributes of the record represented by current_record for storage in a graph
        for attr in record_attr:
            setattr(record_for_graph, attr, record_attr[attr])
        self.graph.add(record_for_graph, parent_record)

        # Get the records (movies or actors) connected to teh current one
        if is_actor:
            tag_list = self.get_movies_of_actor(self.degree, current_record.name)
        else:
            tag_list = self.get_stars_of_movie(self.degree, current_record.name, old_soup=record_soup)

        # If there was an error earlier in the code, skip this record
        if not tag_list:
            return 0, 0

        # Add the nodes connected to the current record to the queue
        self.add_to_queue(tag_list, record_for_graph, is_actor)
        logging.debug(
            "tag list should have {} many entries; it actually has {} many entries".format(self.degree, len(tag_list)))

        # Complete the round and go to run another one
        if is_actor:
            return 1, 0
        else:
            return 0, 1

    def query(self, query_string, is_actor, actor_limit, movie_limit):
        """
        Initiate the scraper using query_string
        :param actor_limit: The maximum number of actors to parse
        :param movie_limit: The maximum number of movies to parse
        :param query_string: The name of the actor or movie that we will begin scraping at
        :param is_actor: True if query_string is the name of an actor; false otherwise
        :return: None
        """
        self.pending_nodes.put(ParseRecord(query_string, None, 0))
        self.run(actor_limit, movie_limit, is_actor)


if __name__ == "__main__":
    pass
