from enum import Enum


class Record(object):

    def __init__(self, name, rec_type):
        self.name = name
        self.rec_type = rec_type

    def get_key(self):
        """
        Return a dictionary key
        :return: A key for use in a dictionary.
        """
        rec_key = (self.name, self.rec_type)
        return rec_key

    def __repr__(self):
        return "[" + repr(self.name) + ", " + repr(self.rec_type) + "]"



class Type(Enum):
    MOVIE = 1
    ACTOR = 2



class MovieRecord(Record):
    def __init__(self, name, rec_type, year=0, grossing_amt=0, contract=0):
        super(MovieRecord, self).__init__(name, rec_type)
        self.year = year
        self.grossing_amt = grossing_amt
        self.contract = contract


class ActorRecord(Record):
    def __init__(self, name, rec_type, age=0, contract=0):
        super(ActorRecord, self).__init__(name, rec_type)
        self.age = age
        self.contract = contract

