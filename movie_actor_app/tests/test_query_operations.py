from unittest import TestCase
from movie_actor_app.graphs.Graph import *
from movie_actor_app.graphs.Record import *


class TestGraph(TestCase):

    # See if we can get a movie's grossing amount using the same record we added to the graph
    def test_get_movie_gross_easy(self):
        graph = Graph()
        expected_amount = 1000
        graph.add(MovieRecord("Batman", Type.MOVIE, 0, grossing_amt=expected_amount),
                  ActorRecord("Bruce Wayne", Type.ACTOR))
        self.assertEqual(expected_amount, graph.get_movie_gross(MovieRecord("Batman", Type.MOVIE)))

    # See if we can get a movie's grossing amount using a different record than what we added to the graph This
    # record is, however, technically equal to the one in the graph since it equals the movie in the graph under __eq__
    def test_get_movie_gross_deceptive(self):
        graph = Graph()
        expected_amount = 1000
        graph.add(MovieRecord("Batman", Type.MOVIE, 0, grossing_amt=expected_amount),
                  ActorRecord("Bruce Wayne", Type.ACTOR))
        self.assertEqual(expected_amount,
                         graph.get_movie_gross(MovieRecord("Batman", Type.MOVIE, 0, grossing_amt=2000)))

    # Add another actor and some movies (noise) and test if the noise obstructs
    # the use of get_movie_of_actor and get_actors_of_movie
    def test_get_movies_of_actor_and_movie(self):
        graph = Graph()
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("FILM1", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("FILM2", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("FILM3", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("FILM4", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("FILM5", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("FILM6", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("FILM7", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("FILM8", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))

        graph.add(MovieRecord("FILM", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("FILM", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("FILM", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("FILM", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))

        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Mom", Type.ACTOR))
        graph.add(MovieRecord("FILM1", Type.MOVIE), ActorRecord("Mom", Type.ACTOR))
        graph.add(MovieRecord("FILM2", Type.MOVIE), ActorRecord("Mom", Type.ACTOR))
        graph.add(MovieRecord("FILM3", Type.MOVIE), ActorRecord("Mom", Type.ACTOR))
        graph.add(MovieRecord("FILM4", Type.MOVIE), ActorRecord("Mom", Type.ACTOR))
        graph.add(MovieRecord("FILM5", Type.MOVIE), ActorRecord("Mom", Type.ACTOR))
        graph.add(MovieRecord("FILM6", Type.MOVIE), ActorRecord("Mom", Type.ACTOR))
        graph.add(MovieRecord("FILM7", Type.MOVIE), ActorRecord("Mom", Type.ACTOR))
        graph.add(MovieRecord("FILM8", Type.MOVIE), ActorRecord("Mom", Type.ACTOR))

        # Test get_movies_of_actor
        expected_output = "[['Batman', <Type.MOVIE: 1>], ['FILM', <Type.MOVIE: 1>], ['FILM1', <Type.MOVIE: 1>], " \
                          "['FILM2', <Type.MOVIE: 1>], ['FILM3', <Type.MOVIE: 1>], ['FILM4', <Type.MOVIE: 1>], " \
                          "['FILM5', <Type.MOVIE: 1>], ['FILM6', <Type.MOVIE: 1>], ['FILM7', <Type.MOVIE: 1>], " \
                          "['FILM8', <Type.MOVIE: 1>]]"
        actual_output = graph.get_movies_of_actor(ActorRecord("Bruce Wayne", Type.ACTOR))
        self.assertEqual(expected_output, repr(actual_output))

        # Test get_actors_of_movie
        expected_output = "[['Bruce Wayne', <Type.ACTOR: 2>], ['Mom', <Type.ACTOR: 2>]]"
        actual_output = graph.get_actors_of_movie(MovieRecord("Batman", Type.MOVIE))
        self.assertEqual(expected_output, repr(actual_output))

    # Give custom salaries that each of 5 actors earned from each of 5 movies. Make sure that the calculations
    # are done correctly
    def test_get_top_actors(self):
        graph = Graph()

        graph.add(MovieRecord("A", Type.MOVIE))
        graph.add(MovieRecord("B", Type.MOVIE))
        graph.add(MovieRecord("C", Type.MOVIE))
        graph.add(MovieRecord("D", Type.MOVIE))
        graph.add(MovieRecord("E", Type.MOVIE))

        graph.add(ActorRecord("1", Type.ACTOR))
        graph.add(ActorRecord("2", Type.ACTOR))
        graph.add(ActorRecord("3", Type.ACTOR))
        graph.add(ActorRecord("4", Type.ACTOR))
        graph.add(ActorRecord("5", Type.ACTOR))

        graph.add(MovieRecord("A", Type.MOVIE, contract=5000), ActorRecord("1", Type.ACTOR, contract=5000))
        graph.add(MovieRecord("A", Type.MOVIE, contract=0), ActorRecord("2", Type.ACTOR, contract=0))
        graph.add(MovieRecord("A", Type.MOVIE, contract=80), ActorRecord("3", Type.ACTOR, contract=80))
        graph.add(MovieRecord("A", Type.MOVIE, contract=0), ActorRecord("4", Type.ACTOR, contract=0))
        graph.add(MovieRecord("A", Type.MOVIE, contract=0), ActorRecord("5", Type.ACTOR, contract=0))

        graph.add(MovieRecord("B", Type.MOVIE, contract=1000), ActorRecord("1", Type.ACTOR, contract=1000))
        graph.add(MovieRecord("B", Type.MOVIE, contract=1000), ActorRecord("1", Type.ACTOR, contract=1000))
        graph.add(MovieRecord("B", Type.MOVIE, contract=0), ActorRecord("2", Type.ACTOR, contract=0))
        graph.add(MovieRecord("B", Type.MOVIE, contract=90), ActorRecord("3", Type.ACTOR, contract=90))
        graph.add(MovieRecord("B", Type.MOVIE, contract=0), ActorRecord("4", Type.ACTOR, contract=0))
        graph.add(MovieRecord("B", Type.MOVIE, contract=-4), ActorRecord("5", Type.ACTOR, contract=-4))

        graph.add(MovieRecord("C", Type.MOVIE, contract=60), ActorRecord("1", Type.ACTOR, contract=60))
        graph.add(MovieRecord("C", Type.MOVIE, contract=10000), ActorRecord("2", Type.ACTOR, contract=10000))
        graph.add(MovieRecord("C", Type.MOVIE, contract=21000), ActorRecord("3", Type.ACTOR, contract=21000))
        graph.add(MovieRecord("C", Type.MOVIE, contract=0), ActorRecord("4", Type.ACTOR, contract=0))
        graph.add(MovieRecord("C", Type.MOVIE, contract=-5), ActorRecord("5", Type.ACTOR, contract=-5))

        graph.add(MovieRecord("D", Type.MOVIE, contract=0), ActorRecord("1", Type.ACTOR, contract=0))
        graph.add(MovieRecord("D", Type.MOVIE, contract=0), ActorRecord("2", Type.ACTOR, contract=0))
        graph.add(MovieRecord("D", Type.MOVIE, contract=0), ActorRecord("3", Type.ACTOR, contract=0))
        graph.add(MovieRecord("D", Type.MOVIE, contract=0), ActorRecord("4", Type.ACTOR, contract=0))
        graph.add(MovieRecord("D", Type.MOVIE, contract=1), ActorRecord("5", Type.ACTOR, contract=1))

        graph.add(MovieRecord("E", Type.MOVIE, contract=0), ActorRecord("1", Type.ACTOR, contract=0))
        graph.add(MovieRecord("E", Type.MOVIE, contract=0), ActorRecord("2", Type.ACTOR, contract=0))
        graph.add(MovieRecord("E", Type.MOVIE, contract=0), ActorRecord("3", Type.ACTOR, contract=0))
        graph.add(MovieRecord("E", Type.MOVIE, contract=0), ActorRecord("4", Type.ACTOR, contract=0))
        graph.add(MovieRecord("E", Type.MOVIE, contract=1), ActorRecord("5", Type.ACTOR, contract=1))

        expected_output = ["3", "2", "1", "4", "5"]
        self.assertEqual(expected_output, graph.get_top_actors(5))
        expected_output = ["3", "2", "1", "4"]
        self.assertEqual(expected_output, graph.get_top_actors(4))
        expected_output = ["3", "2", "1"]
        self.assertEqual(expected_output, graph.get_top_actors(3))
        expected_output = ["3", "2"]
        self.assertEqual(expected_output, graph.get_top_actors(2))
        expected_output = ["3"]
        self.assertEqual(expected_output, graph.get_top_actors(1))

    # Self Explanatory
    def test_get_movies_year(self):
        graph = Graph()
        graph.add(MovieRecord("A", Type.MOVIE, year=2000))
        graph.add(MovieRecord("B", Type.MOVIE, year=2001))
        graph.add(MovieRecord("C", Type.MOVIE, year=2000))
        graph.add(MovieRecord("D", Type.MOVIE, year=2002))
        graph.add(MovieRecord("E", Type.MOVIE, year=2000))
        expected_output = ["A", "C", "E"]
        self.assertEqual(expected_output, graph.get_movies_year(2000))

    # Self Explanatory
    def test_get_actors_year(self):
        graph = Graph()
        graph.add(ActorRecord("A", Type.ACTOR, age=20))
        graph.add(ActorRecord("B", Type.ACTOR, age=20))
        graph.add(ActorRecord("C", Type.ACTOR, age=20))
        graph.add(ActorRecord("D", Type.ACTOR, age=21))
        graph.add(ActorRecord("E", Type.ACTOR, age=20))
        expected_output = ["A", "B", "C", "E"]
        self.assertEqual(expected_output, graph.get_actors_year(20))

    # Self Explanatory
    def test_update_bio(self):
        graph = Graph()
        graph.add(MovieRecord("A", Type.MOVIE, year=20), Record("Actor 1", Type.ACTOR, 0))
        graph.update_bio(MovieRecord("A", Type.MOVIE), {"year": 30})
        expected_output = []
        self.assertEqual(expected_output, graph.get_movies_year(20))
        expected_output = ["A"]
        self.assertEqual(expected_output, graph.get_movies_year(30))
        expected_output = []
        self.assertEqual(expected_output, graph.get_movies_year(20))

    # Self Explanatory
    def test_update_contract(self):
        graph = Graph()
        graph.add(MovieRecord("A", Type.MOVIE, year=20,contract=50), Record("1", Type.ACTOR, contract=50))
        graph.add(MovieRecord("A", Type.MOVIE, year=20,contract=50), Record("2", Type.ACTOR, contract=50))
        graph.add(MovieRecord("A", Type.MOVIE, year=20,contract=50), Record("3", Type.ACTOR, contract=50))
        graph.add(MovieRecord("A", Type.MOVIE, year=20,contract=50), Record("4", Type.ACTOR, contract=50))

        graph.update_contract(MovieRecord("A", Type.MOVIE), Record("1", Type.ACTOR), new_contract=100)
        graph.update_contract(MovieRecord("A", Type.MOVIE), Record("2", Type.ACTOR), new_contract=-50)
        graph.update_contract(MovieRecord("A", Type.MOVIE), Record("3", Type.ACTOR), new_contract=60)

        expected_output = ["1", "3", "4", "2"]
        self.assertEqual(expected_output, graph.get_top_actors(4))

        expected_output = ["1", "3", "4"]
        self.assertEqual(expected_output, graph.get_top_actors(3))

        expected_output = ["1", "3"]
        self.assertEqual(expected_output, graph.get_top_actors(2))

        expected_output = ["1"]
        self.assertEqual(expected_output, graph.get_top_actors(1))
