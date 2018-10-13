import json
from .Graph import Graph
from .Record import Record
from .Record import Type
from .Record import ActorRecord
from .Record import MovieRecord


def get_type(id_string):
    return Type.ACTOR if id_string.__eq__("Actor") else Type.MOVIE

def parse_data():
    with open("data.json", "r") as file_name:
        data = json.load(file_name)

    graph = Graph.Graph()

    actor_index = 0
    movie_index = 1

    actors = data[actor_index]
    for actor in actors:
        actor_record = ActorRecord(actor['name'], get_type(actor['json_class']), actor['age'], total_earnings=actor['total_gross'], wiki_page=actor['wiki_page'])
        graph.add(actor_record)

    movies = data[movie_index]
    for movie in movies:
        movie_record = MovieRecord(movie['name'], get_type(movie['json_class']), movie['year'], grossing_amt=movie['box_office'], wiki_page=movie['wiki_page'])
        graph.add(movie_record)

    for actor_name in actors:
        movies_of_actor = actor_name['movies']
        for movie_name in movies_of_actor:
            if graph.contains_by_name(movie_name):
                graph.connect_by_name(actor_name, movie_name)


