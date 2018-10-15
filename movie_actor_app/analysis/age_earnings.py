from enum import Enum
from movie_actor_app.graphs.Graph import Graph


class AgeCategory(Enum):
    A = lambda x: 10 <= x < 20
    B = lambda x: 20 <= x < 30
    C = lambda x: 30 <= x < 40
    D = lambda x: 40 <= x < 50
    E = lambda x: 50 <= x < 60
    F = lambda x: 60 <= x < 70
    G = lambda x: 70 <= x < 80
    H = lambda x: 80 <= x < 90
    I = lambda x: 90 <= x < 100
    J = lambda x: 100 <= x < 110


def add_to_dict(the_dict, key, value):
    """
    Append an entry to a list in the_dict
    :param the_dict: The dictionary to add to.
    :param key: An object that serves as an index
    :param value: An entry to append to to_dict at key
    :return: None
    """

    if key in the_dict:
        the_dict[key].append(value)
    else:
        the_dict[key] = [value]


def average(list):
    n = len(list)
    sum = 0
    for x in list:
        sum += x
    return sum/n

def get_age_distribution(graph):
    actor_dict = graph.get_actors()
    age_dict = dict()

    age_categories = [AgeCategory.A, AgeCategory.B, AgeCategory.C, AgeCategory.D, AgeCategory.E,AgeCategory.F,
                      AgeCategory.G, AgeCategory.H, AgeCategory.I, AgeCategory.J]
    for actor in actor_dict:
        for age_category in age_categories:
            age_matches = age_category(actor.age)
            if age_matches:
                add_to_dict(age_dict, age_category, actor.total_earnings)
                break

    category_dict = {AgeCategory.A: 10, AgeCategory.B: 20, AgeCategory.C :30, AgeCategory.D : 40, AgeCategory.E : 50, AgeCategory.F :60, AgeCategory.G : 70, AgeCategory.H:80, AgeCategory.I:90, AgeCategory.J:100}

    final_dict = dict()
    for age_category in age_dict:
        final_dict[category_dict[age_category]] = average(age_dict[age_category])

    return final_dict
