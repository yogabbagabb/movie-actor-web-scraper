from enum import Enum


class Record(object):

    def __init__(self, name, rec_type, contract=None, wiki_page=None):
        self.name = name
        self.rec_type = rec_type
        self.contract = contract
        self.wiki_page = wiki_page

    def get_key(self):
        """
        Return a dictionary key
        :return: A key for use in a dictionary.
        """
        rec_key = (self.name, self.rec_type)
        return rec_key

    def __repr__(self):
        return "[" + repr(self.name) + ", " + repr(self.rec_type) + "]"

    def __hash__(self):
        return hash((self.name, self.rec_type))

    def __eq__(self, other):
        return self.name == other.name and self.rec_type == other.rec_type


class Type(Enum):
    MOVIE = 1
    ACTOR = 2


class MovieRecord(Record):
    def __init__(self, name, rec_type, year=0, grossing_amt=0, contract=0, wiki_page=None):
        super(MovieRecord, self).__init__(name, rec_type, contract, wiki_page)
        self.year = year
        self.grossing_amt = grossing_amt


class ActorRecord(Record):
    def __init__(self, name, rec_type, age=0, contract=0, total_earnings=0, wiki_page = None):
        super(ActorRecord, self).__init__(name, rec_type, contract, wiki_page)
        self.age = age
        self.total_earnings = total_earnings

"""
Note:
We could make it a policy that each movie in the movie dictionary maps to Records (and not ActorRecords) whose types are set to actors.
Then if we want to look up information about the actors in a movie, we just iterate over these Record objects and check out their fields
in the actor dictionary
"""
