from unittest import TestCase
from graphs.Graph import *
from graphs.Record import *


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

        expected_string = "Batman:[['Bruce Wayne', <Type.ACTOR: 2>]]\n"\
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
