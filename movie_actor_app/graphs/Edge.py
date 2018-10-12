class Edge(object):

    def __init__(self, actor_name, movie_name):
        self.actor_name = actor_name
        self.movie_name = movie_name

    def __hash__(self):
        return hash((self.actor_name, self.movie_name))

    def __eq__(self, other):
        return self.actor_name == other.actor_name and self.movie_name == other.movie_name
