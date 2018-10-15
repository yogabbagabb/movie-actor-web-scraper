from unittest import TestCase
from movie_actor_app.graphs.Graph import *
from movie_actor_app.graphs.Record import *
from movie_actor_app.analysis.actor_hubs import *


class Test_Actor_Hubs(TestCase):
    def setUp(self):
        self.graph = Graph()
        batman = MovieRecord("Batman")
        superman = MovieRecord("Superman")

        bruce = ActorRecord("Bruce")
        bruce1 = ActorRecord("Bruce1")
        bruce2 = ActorRecord("Bruce2")
        clark = ActorRecord("Clark")
        clark1 = ActorRecord("Clark1")
        clark2 = ActorRecord("Clark2")

        self.graph.add(batman, bruce)
        self.graph.add(batman, bruce1)
        self.graph.add(batman, bruce2)
        self.graph.add(batman, clark)
        self.graph.add(superman, clark)
        self.graph.add(superman, clark1)
        self.graph.add(superman, clark2)

    def test_get_movie_degrees(self):
        expected_output = {'Batman': 4, 'Superman': 3}
        self.assertEquals(get_movie_degrees(self.graph), expected_output)

    def test_get_hub_degrees(self):
        expected_output = {'Bruce': 4, 'Bruce1': 4, 'Bruce2': 4, 'Clark': 7, 'Clark1': 3, 'Clark2': 3}
        actual_output = get_hub_degrees(self.graph, get_movie_degrees(self.graph))
        self.assertEquals(expected_output, actual_output)

    def test_get_top_hubs(self):
        expected_output = [('Clark', 7), ('Bruce2', 4), ('Bruce1', 4), ('Bruce', 4), ('Clark2', 3), ('Clark1', 3)]
        self.assertEquals(expected_output, get_top_hubs(6, self.graph))

