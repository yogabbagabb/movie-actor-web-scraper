from unittest import TestCase
from movie_actor_app.graphs.Graph import *
from movie_actor_app.graphs.Record import *


class TestGraph(TestCase):

    # Test the addition of two new nodes
    def test_add_both_new(self):
        graph = Graph()
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        expected_string = "Batman:[['Bruce Wayne', <Type.ACTOR: 2>]]\n" \
                          "Bruce Wayne:[['Batman', <Type.MOVIE: 1>]]"

        actual_string = repr(graph)
        self.assertEqual(expected_string, actual_string)

        graph = Graph()
        graph.add(ActorRecord("Bruce Wayne", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))
        expected_string = "Batman:[['Bruce Wayne', <Type.ACTOR: 2>]]\n" \
                          "Bruce Wayne:[['Batman', <Type.MOVIE: 1>]]"
        actual_string = repr(graph)
        self.assertEqual(expected_string, actual_string)

    # Test the addition of a new node to an existing one
    def test_add_one_new(self):
        graph = Graph()
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Alfred Butler", Type.ACTOR))

        expected_string = "Batman:[['Alfred Butler', <Type.ACTOR: 2>], ['Bruce Wayne', <Type.ACTOR: 2>]]\n" \
                          "Alfred Butler:[['Batman', <Type.MOVIE: 1>]]Bruce Wayne:[['Batman', <Type.MOVIE: 1>]]"

        actual_string = repr(graph)
        self.assertEqual(expected_string, actual_string)

        graph = Graph()
        graph.add(ActorRecord("Bruce Wayne", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))
        graph.add(ActorRecord("Alfred Butler", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))
        expected_string = "Batman:[['Alfred Butler', <Type.ACTOR: 2>], ['Bruce Wayne', <Type.ACTOR: 2>]]\n" \
                          "Alfred Butler:[['Batman', <Type.MOVIE: 1>]]Bruce Wayne:[['Batman', <Type.MOVIE: 1>]]"

        actual_string = repr(graph)
        self.assertEqual(expected_string, actual_string)

    # Test the addition of multiple new nodes to an existing one
    def test_add_multiple_to_one(self):
        graph = Graph()
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Alfred Butler", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("The Penguin", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Cat-woman", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Robin", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Dumb-ass", Type.ACTOR))

        expected_string = "Batman:[['Alfred Butler', <Type.ACTOR: 2>], ['Bruce Wayne', <Type.ACTOR: 2>], " \
                          "['Cat-woman', <Type.ACTOR: 2>], ['Dumb-ass', <Type.ACTOR: 2>], ['Robin', <Type.ACTOR: 2>], " \
                          "['The Penguin', <Type.ACTOR: 2>]]\n" \
                          "Alfred Butler:[['Batman', <Type.MOVIE: 1>]]Bruce Wayne:[['Batman', <Type.MOVIE: " \
                          "1>]]Cat-woman:[['Batman', " \
                          "<Type.MOVIE: 1>]]Dumb-ass:[['Batman', <Type.MOVIE: 1>]]Robin:[['Batman', <Type.MOVIE: " \
                          "1>]]The Penguin:[['Batman', <Type.MOVIE: 1>]]"

        actual_string = repr(graph)
        self.assertEqual(expected_string, actual_string)

    # Test the addition of an isolated node

    # Test that redundant addition of an edge is not problematic
    def test_redundancy(self):
        graph = Graph()
        graph.add(ActorRecord("Bruce Wayne", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))
        graph.add(ActorRecord("Alfred Butler", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))
        graph.add(ActorRecord("The Penguin", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))
        graph.add(ActorRecord("Cat-woman", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))
        graph.add(ActorRecord("Robin", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))
        graph.add(ActorRecord("Dumb-ass", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))
        graph.add(ActorRecord("Dumb-ass", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))
        graph.add(ActorRecord("Dumb-ass", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))
        graph.add(ActorRecord("Dumb-ass", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))
        graph.add(ActorRecord("Dumb-ass", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))

        expected_string = "Batman:[['Alfred Butler', <Type.ACTOR: 2>], ['Bruce Wayne', <Type.ACTOR: 2>], " \
                          "['Cat-woman', <Type.ACTOR: 2>], ['Dumb-ass', <Type.ACTOR: 2>], ['Robin', <Type.ACTOR: 2>], " \
                          "['The Penguin', <Type.ACTOR: 2>]]\n" \
                          "Alfred Butler:[['Batman', <Type.MOVIE: 1>]]Bruce Wayne:[['Batman', <Type.MOVIE: " \
                          "1>]]Cat-woman:[['Batman', " \
                          "<Type.MOVIE: 1>]]Dumb-ass:[['Batman', <Type.MOVIE: 1>]]Robin:[['Batman', <Type.MOVIE: " \
                          "1>]]The Penguin:[['Batman', <Type.MOVIE: 1>]]"

        actual_string = repr(graph)
        self.assertEqual(expected_string, actual_string)

    # Test symmetry
    def test_redundancy_dual(self):
        graph = Graph()
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Alfred Butler", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("The Penguin", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Cat-woman", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Robin", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Dumb-ass", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Dumb-ass", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Dumb-ass", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Dumb-ass", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Dumb-ass", Type.ACTOR))

        expected_string = "Batman:[['Alfred Butler', <Type.ACTOR: 2>], ['Bruce Wayne', <Type.ACTOR: 2>], " \
                          "['Cat-woman', <Type.ACTOR: 2>], ['Dumb-ass', <Type.ACTOR: 2>], ['Robin', <Type.ACTOR: 2>], " \
                          "['The Penguin', <Type.ACTOR: 2>]]\n" \
                          "Alfred Butler:[['Batman', <Type.MOVIE: 1>]]Bruce Wayne:[['Batman', <Type.MOVIE: " \
                          "1>]]Cat-woman:[['Batman', " \
                          "<Type.MOVIE: 1>]]Dumb-ass:[['Batman', <Type.MOVIE: 1>]]Robin:[['Batman', <Type.MOVIE: " \
                          "1>]]The Penguin:[['Batman', <Type.MOVIE: 1>]]"

        actual_string = repr(graph)
        self.assertEqual(expected_string, actual_string)

    # Test that we can encode a graph cycle
    def test_cycle(self):
        graph = Graph()
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("Batman 2", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Alfred Butler", Type.ACTOR))
        graph.add(MovieRecord("Batman 2", Type.MOVIE), ActorRecord("Alfred Butler", Type.ACTOR))

        expected_string = "Batman:[['Alfred Butler', <Type.ACTOR: 2>], ['Bruce Wayne', <Type.ACTOR: 2>]]Batman 2:[[" \
                          "'Alfred Butler', <Type.ACTOR: 2>], ['Bruce Wayne', <Type.ACTOR: 2>]]\n" \
                          "Alfred Butler:[['Batman', <Type.MOVIE: 1>], ['Batman 2', <Type.MOVIE: 1>]]Bruce Wayne:[[" \
                          "'Batman', <Type.MOVIE: 1>], " \
                          "['Batman 2', <Type.MOVIE: 1>]]"

        actual_string = repr(graph)
        self.assertEqual(expected_string, actual_string)

    # Test that we can add two singleton nodes and then connect them
    def test_two_singletons(self):
        graph = Graph()
        graph.add(MovieRecord("Batman", Type.MOVIE))
        graph.add(ActorRecord("Bruce Wayne", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))

        expected_string = "Batman:[['Bruce Wayne', <Type.ACTOR: 2>]]\n" \
                          "Bruce Wayne:[['Batman', <Type.MOVIE: 1>]]"

        actual_string = repr(graph)
        self.assertEqual(expected_string, actual_string)

    # Test that we can add a singleton node and then connect it to another node
    def test_one_singleton(self):
        graph = Graph()
        graph.add(MovieRecord("Batman", Type.MOVIE))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("Bruce Wayne", Type.ACTOR))

        expected_string = "Batman:[['Bruce Wayne', <Type.ACTOR: 2>]]\n" \
                          "Bruce Wayne:[['Batman', <Type.MOVIE: 1>]]"

        actual_string = repr(graph)
        self.assertEqual(expected_string, actual_string)

    def test_apportion_contracts(self):
        graph = Graph()
        graph.add(MovieRecord("Batman", Type.MOVIE, grossing_amt=1000), ActorRecord("1", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("8", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("4", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("3", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("5", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("6", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("7", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("2", Type.ACTOR))
        graph.apportion_contracts(Record("Batman", Type.MOVIE))
        expected_result = ['1', '8', '4', '3', '5', '6', '2', '7']
        self.assertEqual(expected_result, graph.get_top_actors(8))

    def test_contains_by_name(self):
        graph = Graph()
        graph.add(MovieRecord("Batman", Type.MOVIE, grossing_amt=1000), ActorRecord("1", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("8", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("4", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("3", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("5", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("6", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("7", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("2", Type.ACTOR))
        graph.add(MovieRecord("Superman", Type.MOVIE))

        self.assertEqual(True, graph.contains_by_name("8", Type.ACTOR))
        self.assertEqual(True, graph.contains_by_name("Batman", Type.MOVIE))
        self.assertEqual(True, graph.contains_by_name("Superman", Type.MOVIE))
        self.assertEqual(False, graph.contains_by_name("10", Type.ACTOR))
        self.assertEqual(False, graph.contains_by_name("Antman", Type.MOVIE))

    def test_connect_by_name(self):
        graph = Graph()
        graph.add(MovieRecord("Batman", Type.MOVIE))
        graph.add(ActorRecord("2", Type.ACTOR))
        graph.connect_by_name("2", "Batman")
        # Test that we can retrieve the movie that is connected to an actor
        expected_str = "[['Batman', <Type.MOVIE: 1>]]"
        self.assertEquals(expected_str, graph.get_movies_of_actor(ActorRecord("2", Type.ACTOR)).__repr__())
        # Test that we can retrieve the actor that is connected to an movie
        expected_str = "[['2', <Type.ACTOR: 2>]]"
        self.assertEquals(expected_str, graph.get_actors_of_movie(MovieRecord("Batman", Type.MOVIE)).__repr__())
        # Test that by connecting one movie to another actor, an actor connected to
        # the movie's information is not compromised
        graph.add(ActorRecord("3", Type.ACTOR))
        graph.connect_by_name("3", "Batman")
        expected_str = "[['Batman', <Type.MOVIE: 1>]]"
        self.assertEquals(expected_str, graph.get_movies_of_actor(ActorRecord("2", Type.ACTOR)).__repr__())
        # Test that the movie's actors are attributed after we connected it by name
        expected_str = "[['2', <Type.ACTOR: 2>], ['3', <Type.ACTOR: 2>]]"
        self.assertEquals(expected_str, graph.get_actors_of_movie(MovieRecord("Batman", Type.MOVIE)).__repr__())

    # Test that we can get a single actor
    def test_actor_json(self):
        graph = Graph()
        graph.add(ActorRecord("Bruce Wayne", Type.ACTOR, 30, 0, 0, None))
        graph.add(ActorRecord("Bruce Wayne", Type.ACTOR), MovieRecord("Batman", Type.MOVIE))
        expected_str = "{\"json_class\": \"Actor\", \"name\": \"Bruce Wayne\", \"age\": 30, " \
                       "\"total_gross\": 0, \"movies\": [\"Batman\"]}"
        self.assertEquals(expected_str, graph.get_actor_json("Bruce Wayne"))

    # Test that we can get a single movie
    def test_movie_json(self):
        graph = Graph()
        graph.add(ActorRecord("Bruce Wayne", Type.ACTOR, 30, 0, 0, None))
        graph.add(ActorRecord("Bruce Wayne", Type.ACTOR), MovieRecord("Batman", Type.MOVIE, 0, 0, 0, None))
        expected_str = "{\"json_class\": \"Movie\", \"name\": \"Batman\", \"wiki_page\": null, " \
                       "\"box_office\": 0, \"year\": 0, \"actors\": [\"Bruce Wayne\"]}"
        self.assertEquals(expected_str, graph.get_movie_json("Batman"))

    # Test that we can query actors or movies
    def test_query(self):
        graph = Graph()
        graph.add(ActorRecord("Bruce Wayne", Type.ACTOR, 30, 0, 0, None))
        graph.add(ActorRecord("Bruce Doggy", Type.ACTOR, 31, 0, 0, None))
        graph.add(ActorRecord("Bruce Yo", Type.ACTOR, 32, 0, 0, None))
        graph.add(ActorRecord("Bruce Ma", Type.ACTOR, 33, 0, 0, None))
        graph.add(ActorRecord("Bruce dog", Type.ACTOR, 40, 0, 0, None))
        graph.add(ActorRecord("Bruce my", Type.ACTOR, 35, 0, 0, None))

        graph.add(ActorRecord("Bruce Wayne", Type.ACTOR), MovieRecord("Batman", Type.MOVIE, 0, 0, 0, None))

        expected_str = "{\"Bruce Wayne\": {\"json_class\": \"Actor\", \"name\": \"Bruce Wayne\", \"age\": 30, " \
                       "\"total_gross\": 0, \"movies\": [\"Batman\"]}}"
        query_dict = {"age": {30}, "name": ["Wayne"]}
        self.assertEquals(expected_str, graph.query(Type.ACTOR, query_dict))

        expected_str = "{\"Batman\": {\"json_class\": \"Movie\", \"name\": \"Batman\", \"wiki_page\": null, " \
                       "\"box_office\": 0, \"year\": 0, \"actors\": [\"Bruce Wayne\"]}}"
        query_dict = {"year": [0], "name": ["Batman"]}
        self.assertEquals(expected_str, graph.query(Type.MOVIE, query_dict))

        expected_str = "{}"
        query_dict = {"year": [1], "name": ["Batman"]}
        self.assertEquals(expected_str, graph.query(Type.MOVIE, query_dict))

        graph.add(ActorRecord("Bruce Yo", Type.ACTOR), MovieRecord("Batman", Type.MOVIE, 0, 0, 0, None))
        expected_str = "{\"Bruce Wayne\": {\"json_class\": \"Actor\", \"name\": \"Bruce Wayne\", \"age\": 30, " \
                       "\"total_gross\": 0, \"movies\": [\"Batman\"]}, " \
                       "\"Bruce Yo\": {\"json_class\": \"Actor\", \"name\": \"Bruce Yo\", \"age\": 32, " \
                       "\"total_gross\": 0, \"movies\": [\"Batman\"]}}"
        query_dict = {"age": [30, 32]}
        actual_str = graph.query(Type.ACTOR, query_dict, and_operator=False)
        self.assertEquals(expected_str, actual_str)

    def test_match(self):
        self.assertTrue(Graph.match("hitmonlee", ["hi"]))
        self.assertFalse(Graph.match("xitmonlee", ["hi"]))
        self.assertTrue(Graph.match(20, [20]))
        self.assertFalse(Graph.match(21, [20]))

    def test_delete(self):
        graph = Graph()
        graph.add(MovieRecord("Batman", Type.MOVIE, grossing_amt=1000), ActorRecord("1", Type.ACTOR))
        graph.add(MovieRecord("Batman", Type.MOVIE), ActorRecord("8", Type.ACTOR))
        graph.apportion_contracts(MovieRecord("Batman"))
        self.assertEquals(500, graph.get_contract("1","Batman"))
        graph.delete("Batman", Type.MOVIE)
        self.assertEquals(0, graph.get_contract("1","Batman"))
        self.assertFalse(graph.contains_by_name("Batman", Type.MOVIE))
        movies_of_actor = graph.get_movies_of_actor(ActorRecord("8"))
        list_is_empty = not movies_of_actor
        self.assertTrue(list_is_empty)

