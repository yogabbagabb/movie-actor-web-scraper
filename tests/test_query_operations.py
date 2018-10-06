from unittest import TestCase
from graphs.Graph import *
from graphs.Record import *


class TestGraph(TestCase):

    def test_get_movie_gross(self):
        graph = Graph()
        expected_amount = 1000
        graph.add(MovieRecord("Batman", Type.MOVIE,0,grossing_amt=expected_amount), ActorRecord("Bruce Wayne", Type.ACTOR))
        self.assertEqual(expected_amount, graph.get_movie_gross(MovieRecord("Batman", Type.MOVIE)))


