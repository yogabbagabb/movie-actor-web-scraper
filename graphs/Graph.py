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
    def get_first(some_tuple):
        return some_tuple[0]

    def __repr__(self):

        the_rep = ""

        # Get the keys for the movie dictionary and sort them by their name
        movie_record_keys = self.__movie_records.keys()
        movie_record_keys = sorted(movie_record_keys, key=self.get_first)

        # For each movie, sort its actors and add them to the set
        for movie in movie_record_keys:
            actor_set = self.__movie_records[movie]
            actor_list = sorted(actor_set, key=self.get_name)

            the_rep += self.get_first(movie) + ":"
            the_rep += repr(actor_list)

        the_rep += "\n"

        actor_record_keys = self.__actor_records.keys()
        actor_record_keys = sorted(actor_record_keys, key=self.get_first)
        for actor in actor_record_keys:
            movie_set = self.__actor_records[actor]
            movie_list = sorted(movie_set, key=self.get_name)

            the_rep += self.get_first(actor) + ":"
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
        :return: Nothing
        """
        if second_record is None:
            self.__add_node(first_record)
        else:
            self.__add_edge(first_record, second_record)

    def __add_node(self, first_record):
        pass

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
            first_record_set = self.__actor_records.get(first_record.get_key())
            second_record_set = self.__movie_records.get(second_record.get_key())
        else:
            first_record_set = self.__movie_records.get(first_record.get_key())
            second_record_set = self.__actor_records.get(second_record.get_key())

        # The first_record does not exist in the graph. We need to add it to the graph and then connect
        # it to the second record.
        if first_record_set is None:
            new_set = set()
            if first_is_actor:
                self.__actor_records[first_record.get_key()] = new_set
            else:
                self.__movie_records[first_record.get_key()] = new_set

            new_set.add(second_record)
        # The first record does exist in the graph. We need to connect it to the second record.
        else:
            first_record_set.add(second_record)

        # The second_record does not exist in the graph. We need to add it to the graph and then connect
        # it to the first record.
        if second_record_set is None:
            new_set = set()
            if first_is_actor:
                self.__movie_records[second_record.get_key()] = new_set
            else:
                self.__actor_records[second_record.get_key()] = new_set

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
        pass

    def get_movies(self, record):
        pass

    def get_actors(self, record):
        pass

    def get_top_actors(self, num):
        pass

    def get_oldest_actors(self, num):
        pass

    def get_movies_year(self, num):
        pass

    def get_actors_year(self, year):
        pass
