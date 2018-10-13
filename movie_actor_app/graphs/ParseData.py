import json
from movie_actor_app.graphs.Graph import Graph
from movie_actor_app.graphs.Record import Type
from movie_actor_app.graphs.Record import ActorRecord
from movie_actor_app.graphs.Record import MovieRecord


def get_type(id_string):
    return Type.ACTOR if id_string.__eq__("Actor") else Type.MOVIE


def parse_data(file_name):
    with open(file_name, "r") as file_name:
        data = json.load(file_name)

    graph = Graph()

    actor_index = 0
    movie_index = 1

    actors = data[actor_index]
    for actor in actors:
        actor_record = ActorRecord(actors[actor]['name'], get_type(actors[actor]['json_class']), actors[actor]['age'],
                                   total_earnings=actors[actor]['total_gross'])
        graph.add(actor_record)

    movies = data[movie_index]
    for movie in movies:
        movie_record = MovieRecord(movies[movie]['name'], get_type(movies[movie]['json_class']), movies[movie]['year'],
                                   grossing_amt=movies[movie]['box_office'], wiki_page=movies[movie]['wiki_page'])
        graph.add(movie_record)

    for actor_name in actors:
        movies_of_actor = actors[actor_name]['movies']
        for movie_name in movies_of_actor:
            if graph.contains_by_name(movie_name, Type.MOVIE):
                graph.connect_by_name(actor_name, movie_name)

    for movie_name in movies:
        actors_in_movie = movies[movie_name]['actors']
        for actor_name in actors_in_movie:
            if graph.contains_by_name(actor_name, Type.ACTOR):
                graph.connect_by_name(actor_name, movie_name)

    return graph


if __name__ == "__main__":
    print(parse_data("data.json"))
