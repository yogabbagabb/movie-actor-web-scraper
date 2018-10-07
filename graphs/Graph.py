from . import Record


class Graph(object):

    def __init__(self):
        # A dictionary that maps the key associated with a particular movie to a set of actors connected to the movie
        self.__movie_records = dict()
        # A dictionary that maps the key associated with a particular actor to a set of movies connected to the actor
        self.__actor_records = dict()

    @staticmethod
    def get_name(some_record):
        return some_record.name

    @staticmethod
    def get_first(some_iterable):
        return some_iterable[0]

    def __repr__(self):
        """
        :return: A string representation of movie records and actor records such that
        movies are sorted alphabetically, and the set of movies connected to each movie is also sorted alphabetically.
        """

        the_rep = ""

        # Get the keys for the movie dictionary and sort them by their name
        movie_record_keys = self.__movie_records.keys()
        movie_record_keys = sorted(movie_record_keys, key=self.get_name)

        # For each movie, sort its actors and add them to the set
        for movie in movie_record_keys:
            actor_set = self.__movie_records[movie]
            actor_list = sorted(actor_set, key=self.get_name)

            the_rep += self.get_name(movie) + ":"
            the_rep += repr(actor_list)

        the_rep += "\n"

        actor_record_keys = self.__actor_records.keys()
        actor_record_keys = sorted(actor_record_keys, key=self.get_name)
        for actor in actor_record_keys:
            movie_set = self.__actor_records[actor]
            movie_list = sorted(movie_set, key=self.get_name)

            the_rep += self.get_name(actor) + ":"
            the_rep += repr(movie_list)

        return the_rep

    def get_movie_records(self):
        return self.__movie_records

    def get_actor_records(self):
        return self.__actor_records

    def add(self, first_record, second_record=None):
        """
    Add an actor to a movie node or a movie to an actor node. We assume that first_record is not None.
        We assume that both first_record and second_record are not of the same rec_type.
        :param first_record: Either an instance of MovieRecord or ActorRecord.
        :param second_record: If first_record is a MovieRecord, then second_record is an ActorRecord or vice vera
        :return: Nothing.
        """
        if second_record is None:
            self.__add_node(first_record)
        else:
            self.__add_edge(first_record, second_record)

    def __add_node(self, first_record):
        """
        Add a single node to the graph.
        :param first_record: The node to add, either an actor or movie.
        :return: Nothing.
        """
        first_is_actor = first_record.rec_type == Record.Type.ACTOR

        # Check to see whether the first_record exists in the graph
        if first_is_actor:
            first_record_set = self.__actor_records.get(first_record)
        else:
            first_record_set = self.__movie_records.get(first_record)

        # The first_record does not exist in the graph. We need to add it to the graph.
        # If it does exist, then we do nothing.
        if first_record_set is None:
            new_set = set()
            if first_is_actor:
                self.__actor_records[first_record] = new_set
            else:
                self.__movie_records[first_record] = new_set

    def __add_edge(self, first_record, second_record):

        """
        Add first_record to the graph if it does not already exist.
        Add second_record to the graph if it does not already exist.
        Then connect first_record to second_record and second_record to first_record.
        We assume that both first_record and second_record are not of the same rec_type.
        :param first_record:
        :param second_record:
        :return: Nothing
        """

        first_is_actor = first_record.rec_type == Record.Type.ACTOR

        # Check to see whether the first_record and second_record exist in the graph
        if first_is_actor:
            first_record_set = self.__actor_records.get(first_record)
            second_record_set = self.__movie_records.get(second_record)
        else:
            first_record_set = self.__movie_records.get(first_record)
            second_record_set = self.__actor_records.get(second_record)

        # The first_record does not exist in the graph. We need to add it to the graph and then connect
        # it to the second record.
        if first_record_set is None:
            new_set = set()
            if first_is_actor:
                self.__actor_records[first_record] = new_set
            else:
                self.__movie_records[first_record] = new_set

            new_set.add(second_record)
        # The first record does exist in the graph. We need to connect it to the second record.
        else:
            first_record_set.add(second_record)

        # The second_record does not exist in the graph. We need to add it to the graph and then connect
        # it to the first record.
        if second_record_set is None:
            new_set = set()
            if first_is_actor:
                self.__movie_records[second_record] = new_set
            else:
                self.__actor_records[second_record] = new_set

            new_set.add(first_record)

        # The second record does exist in the graph. We need to connect it to the first record.
        else:
            second_record_set.add(first_record)

    def remove(self, record):
        pass

    def replace(self, record):
        pass

    def union(self, other_graph):
        pass

    def intersection(self, other_graph):
        pass

    def get_movie_gross(self, record):
        """
        Get the gross earnings for a movie
        :param record: The movie whose gross earnings are sought.
        :return: Gross earnings (a float).
        """
        movie_keys = self.__movie_records.keys()
        for movie in movie_keys:
            if movie.__eq__(record):
                return movie.grossing_amt

    def get_movies_of_actor(self, record):
        """
        Get the movies that an actors has worked in.
        :param record: An ActorRecord
        :return: A list of movies that the actor represented by record has worked in
        """
        movie_set = self.__actor_records[record]
        movie_list = list(movie_set)
        movie_list = sorted(movie_list, key=self.get_name)
        return movie_list

    def get_actors_of_movie(self, record):
        """
        Get the actors that appeared in a movie
        :param record: A MovieRecord
        :return: A list of actors that appeared in the movie represented by the record
        """
        actor_set = self.__movie_records[record]
        actor_list = list(actor_set)
        actor_list = sorted(actor_list, key=self.get_name)
        return actor_list

    def get_top_actors(self, num):
        """
        Get the top 'num' highest earning actors in the graph
        :param num: The number of top actors to cull.
        :return: An array of the names of the top num actors
        """

        all_actors = self.__actor_records.keys()
        for actor in all_actors:
            actor.total_earnings = self.__get_total_earnings(self.__actor_records[actor])

        all_actors_list = sorted(all_actors, key=(lambda an_actor: an_actor.total_earnings))
        return self.__get_top_of_attr(all_actors_list, num)

    @staticmethod
    def __get_total_earnings(movie_set):
        total_earnings = 0
        for movie in movie_set:
            total_earnings += movie.contract
        return total_earnings

    def get_oldest_actors(self, num):
        all_actors = self.__actor_records.keys()
        all_actors_list = sorted(all_actors, key=(lambda an_actor: an_actor.age))
        return self.__get_top_of_attr(all_actors_list, num)

    @staticmethod
    def __get_top_of_attr(all_actors_list, num):
        all_actors_list = list(map((lambda an_actor: an_actor.name), all_actors_list))
        if num == len(all_actors_list):
            return all_actors_list[::-1]
        else:
            first_idx = len(all_actors_list) - 1
            sec_idx = len(all_actors_list) - 1 - num
            return all_actors_list[first_idx:sec_idx:-1]

    def get_movies_year(self, year):
        movies_in_year = list()
        all_movies = self.__movie_records.keys()
        for movie in all_movies:
            if movie.year == year:
                movies_in_year.append(movie.name)
        return movies_in_year

    def get_actors_year(self, year):
        actors_in_year = list()
        all_actors = self.__actor_records.keys()
        for actor in all_actors:
            if actor.age == year:
                actors_in_year.append(actor.name)
        return actors_in_year

