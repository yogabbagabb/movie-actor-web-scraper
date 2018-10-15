"""
Make plots
"""
from movie_actor_app.analysis.actor_hubs import *
from movie_actor_app.graphs.ParseData import parse_data
from movie_actor_app.analysis.age_earnings import *
from matplotlib import pyplot as plt
import os



def make_box_whisker(distribution):
    """
    Make a box and whisker plot using a distribution.
    :param distribution: A an array of floats.
    :return: None
    """

    plt.boxplot(distribution)
    plt.ylabel("Hub Degree")
    plt.title("Distribution of Hub Degrees in The Graph")
    plt.show()

def make_scatter_plot(x_vals, y_vals):
    """
    Make a scatter plot with dots (no lines)
    :param x_vals: Some x coordinates.
    :param y_vals: Some y coordinates
    :return:
    """
    plt.plot(x_vals, y_vals, 'rx')
    plt.xlabel("Age Bracket [x, x+10)")
    plt.ylabel("Average Total Gross")
    plt.title("Correlation Between Total Gross Amount and Age Bracket")
    plt.show()


if __name__ == "__main__":

    file_path = os.path.join(os.getcwd(), "../api/data.json")
    graph = parse_data(file_path)
    hub_degree_dict = get_hub_degrees(graph)

    print(get_top_hubs(50, graph, hub_degree_dict))

    all_values = list(hub_degree_dict.values())
    make_box_whisker(all_values)
    values_less_40 = list(filter(lambda x: x <= 40, all_values))
    make_box_whisker(values_less_40)
    age_dict = get_age_distribution(graph)
    make_scatter_plot(list(age_dict.keys()), list(age_dict.values()))
