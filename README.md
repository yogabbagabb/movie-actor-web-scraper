# fa18-cs242-assignment2
Please run scraper/UserInterface.py to run the scraper

After it scrapes some starting entry (a movie or actor's name),
and finishes scraping 251 actors and 151 movies, you can then
write queries to it using the console that will open below.

These are the methods that a scraper object can use:

    def get_actors_in_movie_ui(self, movie_name):
        """
        Get the actors in the movie whose title is movie_name
        :param movie_name: A movie name
        :return:
        """

    def get_movies_of_actor_ui(self, actor_name):
        """
        Get the movies that an actor played in.
        :param actor_name: The actor for whom we wish to query movies.
        :return:
        """

    def get_top_actors(self, num):
        """
        Get the num highest paid actors
        :param num: an integer.
        :return: A list of the higest paid actors. The first actor is the highest paid one.
        """

    def get_grossing_amount(self, movie_name):
        """
        Get the amount that the movie earned
        :param movie_name: The movie to query
        :return:
        """

    def get_actors_in_year(self, year):

    def get_movies_in_year(self, year):

    def get_oldest_actors(self, num):
        """
        Get num oldest actors
        :param num: How many actors to get
        :return: A list of the oldest actors; the first actor in the list is the oldest
        """

    def get_all_movies(self):

    def get_all_actors(self):

    def get_billing_distribution(self, movie_name):
        """
        Get the distribution of salaries for the actors that worked in a movie
        :param movie_name: The movie actors worked in
        :return: Notne
        """
