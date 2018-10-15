from . import Record
from .Record import Type
from .Contract import Contract
import json
import orderedset


class Graph(object):
    contract_string = "contract"

    def __init__(self):
        # A dictionary that maps the key associated with a particular movie to a set of actors connected to the movie
        self.__movie_records = dict()
        # A dictionary that maps the key associated with a particular actor to a set of movies connected to the actor
        self.__actor_records = dict()
        # A dictionary that maps a Contract (an actor's name, a movie's name) to a float (the actual contract between
        #  the corresponding actor and movie)
        self.__contracts = dict()
        # A dictionary that looks up an ActorRecord or MovieRecord using the name of the object and its type
        self.__lookup_table = dict()

    def get_movies(self):
        return self.__movie_records

    def get_actors(self):
        return self.__actor_records

    def get_contract(self, actor_name, movie_name):
        """
        Get the contract between actor_name and movie_name.
        :param actor_name: The name of an actor.
        :param movie_name: The name of a movie.
        :return: The contract amount, a float.
        """
        contract_amt = self.__contracts.get(Contract(actor_name, movie_name))
        if contract_amt is None:
            return 0
        else:
            return contract_amt['contract']

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

    def connect_by_name(self, actor_name, movie_name):
        """
        We assume that actor_name and movie_name correspond
        to an actor and movie that already exist in the graph.
        :param actor_name: The name of an actor whose record
        exists in the graph
        :param movie_name: The name of an movie whose record
        exists in the graph
        :return: Nothing
        """

        actor_record = self.__lookup_table.get((actor_name, Type.ACTOR))
        movie_record = self.__lookup_table.get((movie_name, Type.MOVIE))

        movies_of_actor = self.__actor_records[actor_record]
        actors_in_movie = self.__movie_records[movie_record]

        movies_of_actor.add(movie_record)
        actors_in_movie.add(actor_record)

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
            self.__add_two_nodes(first_record, second_record)

    def __add_node(self, first_record):
        """
        Add a single node to the graph.
        :param first_record: The node to add, either an actor or movie.
        :return: None
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
            new_set = orderedset.OrderedSet()
            if first_is_actor:
                self.__actor_records[first_record] = new_set
            else:
                self.__movie_records[first_record] = new_set
            self.__lookup_table[(first_record.name, first_record.rec_type)] = first_record

    def __add_two_nodes(self, first_record, second_record):

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
            new_set = orderedset.OrderedSet()
            if first_is_actor:
                self.__actor_records[first_record] = new_set
            else:
                self.__movie_records[first_record] = new_set

            new_set.add(second_record)
            self.__lookup_table[(first_record.name, first_record.rec_type)] = first_record
        # The first record does exist in the graph. We need to connect it to the second record.
        else:
            first_record_set.add(second_record)

        # The second_record does not exist in the graph. We need to add it to the graph and then connect
        # it to the first record.
        if second_record_set is None:
            new_set = orderedset.OrderedSet()
            if first_is_actor:
                self.__movie_records[second_record] = new_set
            else:
                self.__actor_records[second_record] = new_set

            new_set.add(first_record)
            self.__lookup_table[(second_record.name, second_record.rec_type)] = second_record

        # The second record does exist in the graph. We need to connect it to the first record.
        else:
            second_record_set.add(first_record)

        # Now update the edges if the passed in records have a contract
        if first_record.contract is not None and second_record.contract is not None:
            if first_record.contract == second_record.contract:
                edge = Contract(first_record.name, second_record.name) if first_is_actor else Contract(
                    second_record.name, first_record.name)
                self.__contracts[edge] = {Graph.contract_string: first_record.contract}

    # def remove(self, record):
    #     pass
    #
    # def replace(self, record):
    #     pass
    #
    # def union(self, other_graph):
    #     pass
    #
    # def intersection(self, other_graph):
    #     pass

    def get_movie_gross(self, record):
        """
        Get the gross earnings for a movie
        :param record: The movie whose gross earnings are sought.
        :return: Gross earnings (a float).
        """
        movie_record = self.__lookup_table.get((record.name, Type.MOVIE))
        return movie_record.grossing_amt

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
            actor.total_earnings = self.__get_total_earnings(actor, self.__actor_records[actor])

        all_actors_list = sorted(all_actors, key=(lambda an_actor: an_actor.total_earnings))
        return self.__get_top_of_attr(all_actors_list, num)

    def __get_total_earnings(self, actor, movie_set):
        total_earnings = 0
        for movie in movie_set:
            edge = Contract(actor.name, movie.name)
            edge_dict = self.__contracts[edge]
            total_earnings += 0 if edge_dict.get(Graph.contract_string) is None else edge_dict.get(
                Graph.contract_string)
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

    def update_bio(self, record, update_attr):
        """
        Update a MovieRecord or ActorRecord's fields to have those field values
        in update_attr
        :param record: A record whose fields we wish to update inside the graph. Note that
        record does not have to be in the graph, and this method will update the copy of record in the graph.
        :param update_attr: The dictionary with new fields and values. We assume that contract is not a field in this dict.
        :return: Nothing
        """
        key = self.__lookup_table[(record.name, record.rec_type)]
        for attr in update_attr:
            setattr(key, attr, update_attr[attr])

    def update_contract(self, first_record, second_record, new_contract):
        """
        Update the contract between the first record and second record. We assume that first record is a movie
        and second record an actor or vice versa. We assume that there is already a connection between first_record and
        second_record. Note that first_record and second_record will be modified to have their contract fields
        set to new_contract as a result of this call.
        :param new_contract: The amount that the first record paid or earned from the second record
        :param first_record: Either a MovieRecord or ActorRecord
        :param second_record: Whatever first_record is not
        :return: Nothing
        """

        first_is_actor = first_record.rec_type == Record.Type.ACTOR
        if first_is_actor:
            edge = Contract(first_record.name, second_record.name)
        else:
            edge = Contract(second_record.name, first_record.name)
        self.__contracts[edge][Graph.contract_string] = new_contract

    def contains(self, record):
        """
        Checks whether record is already part of the graph
        :param record: A record referring to either an actor or movie
        :return: Whether record is part of the graph or not
        """

        if record.rec_type == Record.Type.ACTOR:
            return record in self.__actor_records
        else:
            return record in self.__movie_records

    def contains_by_name(self, name, the_type):
        """
        Checks whether the name of an actor or movie maps to record that exists in the graph.
        :param the_type: The record type of the entry corresponding to name
        :param name: The name of the actor or movie to check
        :return: A boolean (true indicates that an actor or movie does exist in the graph; false otherwise)
        """
        return self.__lookup_table.get((name, the_type)) is not None

    def apportion_contracts(self, movie_record):

        # Get the movie within the graph that equals movie_record
        # Recall that two records are equal iff they have the same name and type
        movie_keys = self.__movie_records.keys()
        for key in movie_keys:
            if key.__eq__(movie_record):
                movie_record = key
                break

        # Get the number of actors connected to the movie and the movie's grossing amount
        actors_in_movie = self.__movie_records[movie_record]
        number_actors = len(actors_in_movie)
        contract_amounts = [None] * number_actors
        grossing_amt = movie_record.grossing_amt
        original_grossing_amt = grossing_amt

        # Split the grossing amount over the actors
        ratio = 0.5
        total_apportioned = 0
        for i in range(0, number_actors - 1, 1):
            grossing_amt *= ratio
            total_apportioned += grossing_amt
            contract_amounts[i] = grossing_amt

        # Give whatever remains to the last actor
        contract_amounts[number_actors - 1] = original_grossing_amt - total_apportioned

        # Update the records in the graph to have correct contract amounts
        actors_in_movie_list = list(actors_in_movie)
        for i in range(0, number_actors):
            edge = Contract(actors_in_movie_list[i].name, movie_record.name)
            self.__contracts[edge] = {Graph.contract_string: contract_amounts[i]}

    def get_actor_json(self, name, actor=None):
        """
        Gets the attributes of actor `name`; these attributes are returned as a json.
        :param name: The name of an actor
        :return: A json with the attributes of the actor
        """

        if actor is None:
            actor = self.__lookup_table[(name, Type.ACTOR)]

        movies_of_actor = [movie.name for movie in self.__actor_records[actor]]
        actor_dict = {
            "json_class": "Actor",
            "name": name,
            "age": actor.age,
            "total_gross": actor.total_earnings,
            "movies": movies_of_actor
        }

        return json.dumps(actor_dict)

    def get_movie_json(self, name, movie=None):
        """
        Gets the attributes of movie `name`; these attributes are returned as a json.
        :param name: The name of an movie
        :return: A json with the attributes of the movie
        """
        if movie is None:
            movie = self.__lookup_table[(name, Type.MOVIE)]

        actors_in_movie = [actor.name for actor in self.__movie_records[movie]]

        movie_dict = {
            "json_class": "Movie",
            "name": name,
            "wiki_page": movie.wiki_page,
            "box_office": movie.grossing_amt,
            "year": movie.year,
            "actors": actors_in_movie
        }

        return json.dumps(movie_dict)

    def query(self, record_type, query_dict, and_operator=True):
        """
        Get all the records with attributes that match those in query_dict.

        :param and_operator: A boolean that indicates whether we and
         (take the intersection of) the queries in query_dictionary. If false,
         we or them
        :param record_type: The category of record (ActorRecord or MovieRecord) that we are trying to find matches in
        :param query_dict: The dictionary of attributes to match against.
        :return: A json satisfying the query
        """
        if record_type == Type.ACTOR:
            return self.query_portion(self.__actor_records, self.get_actor_json, query_dict, and_operator)
        else:
            return self.query_portion(self.__movie_records, self.get_movie_json, query_dict, and_operator)

    @staticmethod
    def query_portion(record_list, lookup_function, query_dict, and_operator=True):
        """
        Return a json object containing those entries in record-list whose attributes match those in query_dict.
        :param record_list: A list of actor records or movie records
        :param lookup_function: A function to obtain a json for any entry in record_list
        :param query_dict: The dictionary with attributes to match against
        :param and_operator: A boolean that indicates whether we and
         (take the intersection of) the queries in query_dictionary. If false,
         we or them
        :return: A json satisfying the query
        """

        match_dict = dict()

        # We are taking the intersection of all queries
        if and_operator:
            for record in record_list:
                attr_match = True
                for key in query_dict:
                    attr_match = Graph.match(getattr(record, key), query_dict[key], and_operator=True)
                    if not attr_match:
                        break
                if attr_match:
                    # Add to the dictionary the matching actor or movie along with its attributes
                    match_dict.update({record.name: json.loads(lookup_function(record.name, record))})

        # We are taking the union of all queries
        else:
            for record in record_list:
                for key in query_dict:
                    attr_match = Graph.match(getattr(record, key), query_dict[key], and_operator=False)
                    if attr_match:
                        # Add to the dictionary the matching actor or movie along with its attributes
                        match_dict.update({record.name: json.loads(lookup_function(record.name, record))})
                        break

        return json.dumps(match_dict)

    @staticmethod
    def match(candidate, standards, and_operator=False):
        """
        Determine if an object (candidate) matches any object in standards,
        or if it matches all objects in standards
        Matching tests, in this function, for string containment of any
        object in standards in candidate or for integer equality between
        candidate and any member of standards.
        :param and_operator: Whether we wish to match candidate against every element in standards or at least one.
        :param candidate: An integer or string to match.
        :param standards: Objects the candidate can match against.
        :return: Whether candidate matches against any standard in standards.
        """
        if and_operator:
            for standard in standards:
                match = Graph.match_two_values(candidate, standard)

                if not match:
                    return False
            return True

        else:
            for standard in standards:
                match = Graph.match_two_values(candidate, standard)

                if match:
                    return True
            return False

    @staticmethod
    def match_two_values(candidate, standard):
        if type(candidate) == str:
            match = standard in candidate
        else:
            # Make sure that standard is an integer
            integer_standard = int(standard)
            match = candidate == integer_standard
        return match

    def delete(self, name, record_type):
        """
        Delete the vertex corresponding to name and record_type from the graph
        This function first checks to see that the record does exist before deleting it; if it does not exist,
        then this function does nothing.
        :param name: The name of the entry.
        :param record_type: The type of entry (actor or movie)
        :return: Whether the record was deleted. If the record did not exist, then return False.
        """

        if not self.contains_by_name(name, record_type):
            return False

        record = self.__lookup_table[(name, record_type)]
        # Remove the record from the look up table
        del self.__lookup_table[(name, record_type)]

        # Get the dictionary that maps record to its neighbors, among other records of the same type
        our_group = self.__movie_records if record_type == Type.MOVIE else self.__actor_records

        opposing_group = self.__actor_records if record_type == Type.MOVIE else self.__movie_records

        neighbors_of_record = our_group[record]
        # Remove the record from the appropriate neighbor dictionary
        del our_group[record]

        for neighbor in neighbors_of_record:
            # Remove any contract between record and a neighbor
            if record_type == Type.ACTOR:
                contract = Contract(record.name, neighbor.name)
            else:
                contract = Contract(neighbor.name, record.name)

            if contract in self.__contracts:
                del self.__contracts[contract]

            # Remove record from the list of neighbors that each of record's neighbors has
            neighbors_of_neighbor = opposing_group[neighbor]
            neighbors_of_neighbor.remove(record)
        return True

    # def to_json(self, filename):
    #     """
    #     Convert the graph to a json
    #     :type filename: A file to write the json to
    #     :return: None
    #     """
    #
    #     with open(filename, "w") as fd:
    #         json.dump(self.__dict__, fd)
    #
    #     return filename
    #
    #
    # @staticmethod
    # def from_json(filename):
    #     """
    #     Construct from a json file that was serialized
    #     :param filename:
    #     :return: None
    #     """
    #
    #     graph = Graph()
    #     graph.__dict__ = json.load(filename)
    #     return graph
