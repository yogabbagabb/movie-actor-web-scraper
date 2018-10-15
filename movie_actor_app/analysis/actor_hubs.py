"""
Givenn an actor A, hub_degree(A) is the sum of the degrees of the movies that the actor is connected to
Visualizes which the spread of hub degrees
"""


def get_movie_degrees(graph):
    """
    Get a dictionary; dictionary's first entry is the name of the movie; the dictionary's second entry is the
    movie's degree.
    :param graph: The graph to compute movie degrees for.
    :return: A dictionary.
    """

    list_of_degrees = dict()
    movie_entries = graph.get_movies()
    for movie in movie_entries:
        actors_connected = len(movie_entries[movie])
        list_of_degrees[movie.name] = actors_connected
    return list_of_degrees


def get_hub_degrees(graph, movie_degrees=None):
    """
    Get a dictionary; dictionary's first entry is the name of the actor; the dictionary's second entry is the
    actor's degree.
    :param movie_degrees: A dictionary mapping a movie to its degree
    :param graph: The graph to compute actor degrees for.
    :return: A dictionary.
    """

    if movie_degrees is None:
        movie_degrees = get_movie_degrees(graph)

    list_of_degrees = dict()
    actor_entries = graph.get_actors()
    for actor in actor_entries:
        hub_degree = 0
        for movie in actor_entries[actor]:
            hub_degree += movie_degrees[movie.name]
        list_of_degrees[actor.name] = hub_degree
    return list_of_degrees




def get_top_hubs(num, graph, hub_dict=None):
    """
    Return the num actors with the highest hub_degree, in order from highest hub degree to least.
    :param graph: The graph underlying all computations.
    :param hub_list: A dictionary of mappings actor name -> hub degree
    :param num: How many actors should we find highest hub degree for.
    :return: A list of the top num actors
    """

    if hub_dict is None:
        hub_dict = get_hub_degrees(graph)

    sorted_list = sorted(hub_dict.items(), key=lambda kv: kv[1])
    last_index = len(sorted_list) - num - 1
    if last_index == -1:
        return sorted_list[::-1]
    else:
        return sorted_list[:last_index:-1]
