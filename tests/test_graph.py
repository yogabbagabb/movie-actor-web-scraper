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

    # Test the addition of an isolated node

    # Test that redundant addition of programming
