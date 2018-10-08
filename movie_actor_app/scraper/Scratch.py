import time

from bs4 import BeautifulSoup
import urllib.request
import logging
import code

from movie_actor_app.scraper.Scraper import Scraper


def is_movie(tag):
    return tag.name == "a" and tag.parent.name == "i" and tag.has_attr("href") and tag.has_attr("title")


def is_filmography_section_strict(tag):
    return tag.has_attr("href") and "filmography" in tag["href"].lower() and "wiki" in tag["href"].lower() \
           and tag.has_attr("rel") and "https" in tag["href"]


def is_filmography_section(tag):
    return tag.has_attr("href") and "filmography" in tag["href"].lower() and "wiki" in tag["href"].lower()


def has_starring_tag(tag):
    return tag.string == "Starring"


def is_age_tag_lax2(tag):
    return tag.has_attr("class") and tag.name == "span" and "noprint" in tag["class"]




def get_movies_of_actor(num, actor_name):
    """
    Get num movies for the actor
    :param num:
    :return:
    """
    page = "https://en.wikipedia.org/wiki/"
    actor_name = actor_name.replace(" ", "_")
    final_string = "_filmography"

    page += (actor_name + final_string)
    with urllib.request.urlopen(page) as url:
        html = url.read()
    soup = BeautifulSoup(html, 'lxml')
    movies = soup.find_all(is_movie)
    return movies[0:num:1]


def get_stars_of_movie(num, movie_name):
    page = "https://en.wikipedia.org/wiki/"
    actor_name = movie_name.replace(" ", "_")

    page += movie_name
    with urllib.request.urlopen(page) as url:
        html = url.read()
    soup = BeautifulSoup(html, 'lxml')
    starring_tag = soup.find(has_starring_tag)
    starring_parent_tag = starring_tag.parent
    stars = starring_parent_tag.findChildren("a")
    if len(stars) < num:
        num = len(stars)
    return stars[0:num:1]


if __name__ == "__main__":
    logging.basicConfig(filename='scraper.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info("\n\n\nStarting\n\n\n")

    # page = "https://en.wikipedia.org/wiki/Matt_Damon_filmography"
    # page = "https://en.wikipedia.org/wiki/Matt_Damon"
    # page = "https://en.wikipedia.org/wiki/Morgan_Freeman"
    # page = "https://en.wikipedia.org/wiki/Ryan_Reynolds"
    # with urllib.request.urlopen(page) as url:
    #     html = url.read()
    # soup = BeautifulSoup(html, 'lxml')
    # print(soup.find_all(is_movie))
    # code.interact(local=locals())

    # scraper = Scraper()
    # print(scraper.get_stars_of_movie(3, "Mulan"))
    # print(scraper.get_movies_of_actor(3, "Matt Damon"))

    t0 = time.time()
    scraper = Scraper(degree=10)
    scraper.query("Matt Damon", is_actor=True, actor_limit=251, movie_limit=126)
    print(time.time() - t0)


