from unittest import TestCase
from movie_actor_app.graphs.Graph import *
from movie_actor_app.graphs.Record import *
from movie_actor_app.analysis.age_earnings import get_age_distribution


class TestGet_age_distribution(TestCase):

    def setUp(self):
        self.graph = Graph()
        batman = MovieRecord("Batman")
        superman = MovieRecord("Superman")

        bruce = ActorRecord("Bruce", total_earnings=400, age=10)
        bruce1 = ActorRecord("Bruce1", total_earnings=300, age=20)
        bruce2 = ActorRecord("Bruce2", total_earnings=20, age=30)
        clark = ActorRecord("Clark", total_earnings=1, age=50)
        clark1 = ActorRecord("Clark1", total_earnings=9, age=54)
        clark2 = ActorRecord("Clark2", total_earnings=3, age=99)

        self.graph.add(batman, bruce)
        self.graph.add(batman, bruce1)
        self.graph.add(batman, bruce2)
        self.graph.add(batman, clark)
        self.graph.add(superman, clark)
        self.graph.add(superman, clark1)
        self.graph.add(superman, clark2)

    def test_get_age_distribution(self):
        expected_output = {10: 400.0, 20: 300.0, 30: 20.0, 50: 5.0, 90: 3.0}
        assert(expected_output.__eq__(get_age_distribution(self.graph)))

