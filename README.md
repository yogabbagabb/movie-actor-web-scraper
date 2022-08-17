# Movie-Actor Scraper


## Description

This is a web scraper that parses movie-actor data from Wikipedia pages. For example, given an actor, we might identify all movies involving that actor and, then, for each movie, all the actors in each movie.

After having finished scraping, one can execute queries on a REPL to answer questions like:

- What are all the movies for a given actor?
- What are the names of all the actors who were scraped?
- Who are the `n` highest paid actors?
- What are the pay distributions for different actors?
- What movies earned the greatest amount?

The scraper was built using beautiful soup.

## Usage

Please run `scraper/UserInterface.py` to run the scraper.

After it scrapes some starting entry (a movie or actor's name),
and finishes scraping a parametrized number of actors and a parametrized number movies, you can then
write queries to it using the console.

These are the methods that you can thereafter run.

To run them, note that you will have to execute methods on an instance of `Scraper` like so

```bash
>>> scraper.get_top_actors(1)
['JoBeth Williams']
```


\
The methods available are shown below:

```python
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
```


## Roadmap

- The scraper requires up to 20 minutes to finish scraping 250 movies and 125 actors. Some optimizations are needed to speed this up.
- The `analysis` and `api` modules need to be bug-patched. The former produces charts to show relationships in parsed data; the latter opened a web server to perform queries.

## License

The MIT License (MIT)

Copyright © 2022

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.