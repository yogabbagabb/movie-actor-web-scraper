# from unittest import TestCase

import pytest
import sys
from movie_actor_app.api.App import *


# class TestCreate_app(TestCase):

@pytest.fixture
def sample_client():
    app_instance = create_app()
    app_instance.config['TESTING'] = True
    client = app_instance.test_client()
    yield client


@pytest.fixture
def loaded_client():
    file_name = "small_data.json"
    app_instance = create_app(file_name)
    app_instance.config['TESTING'] = True
    client = app_instance.test_client()
    yield client


# Test our ability to get the correct string from the root url
def test_initialize(sample_client):
    hello_world = sample_client.get('/')
    assert hello_world.__eq__("Hello World")


# Test getting all the attributes of a single actor
def test_get_whole_actor(loaded_client):
    actor_details = loaded_client.get('/actors/Bruce Willis')
    actor_json = json.loads(actor_details.get_data().decode(sys.getdefaultencoding()))

    with open("small_data.json", "r") as fd:
        small_data = json.load(fd)
    # print(actor_json)
    # print(small_data[0]['Bruce Willis'])
    assert actor_json.__eq__(small_data[0]['Bruce Willis'])


# Test getting all the attributes of a single movie
def test_get_whole_movie(loaded_client):
    movie_details = loaded_client.get('/movies/The First Deadly Sin')
    movie_json = json.loads(movie_details.get_data().decode(sys.getdefaultencoding()))

    with open("small_data.json", "r") as fd:
        small_data = json.load(fd)
    # print(movie_json)
    # print(small_data[1]['The First Deadly Sin'])
    assert movie_json.__eq__(small_data[1]['The First Deadly Sin'])


def test_perform_simple_query(loaded_client):
    movie_details = loaded_client.get('/movies?name=Deadly')
    movie_json = json.loads(movie_details.get_data().decode(sys.getdefaultencoding()))

    with open("small_data.json", "r") as fd:
        small_data = json.load(fd)

    assert (small_data[1]['The First Deadly Sin']).__eq__(movie_json['The First Deadly Sin'])


def test_perform_complex_query(loaded_client):
    # Test for orring that results in two matches
    movie_details = loaded_client.get('/movies?name=Deadly|name=Verdict')
    movie_json = json.loads(movie_details.get_data().decode(sys.getdefaultencoding()))

    with open("small_data.json", "r") as fd:
        small_data = json.load(fd)

    assert (small_data[1]['The First Deadly Sin']).__eq__(movie_json['The First Deadly Sin'])

    expected_dict = {'actors': ['Bruce Willis'], 'box_office': 53977250, 'json_class': 'Movie', 'name': 'The Verdict',
                     'year': 1982, "wiki_page": "https://en.wikipedia.org/wiki/The_Verdict"}
    assert expected_dict.__eq__(movie_json['The Verdict'])

    # Test for orring that results in one match
    movie_details = loaded_client.get('/movies?name=Deadly|name=Poop')
    movie_json = json.loads(movie_details.get_data().decode(sys.getdefaultencoding()))
    assert (small_data[1]['The First Deadly Sin']).__eq__(movie_json['The First Deadly Sin'])

    # Test for anding that results in one match
    movie_details = loaded_client.get('/movies?name=Deadly&name=The')
    movie_json = json.loads(movie_details.get_data().decode(sys.getdefaultencoding()))
    assert (small_data[1]['The First Deadly Sin']).__eq__(movie_json['The First Deadly Sin'])

    # Test for redundant anding that results in two matches
    movie_details = loaded_client.get('/movies?name=The&name=The')
    movie_json = json.loads(movie_details.get_data().decode(sys.getdefaultencoding()))
    assert (small_data[1]['The First Deadly Sin']).__eq__(movie_json['The First Deadly Sin'])

    expected_dict = {'actors': ['Bruce Willis'], 'box_office': 53977250, 'json_class': 'Movie', 'name': 'The Verdict',
                     'year': 1982, "wiki_page": "https://en.wikipedia.org/wiki/The_Verdict"}
    assert expected_dict.__eq__(movie_json['The Verdict'])


def test_perform_null_query(loaded_client):
    # Test for anding that results in zero matches
    movie_details = loaded_client.get('/movies?name=Deadly&name=Poop')
    movie_json = json.loads(movie_details.get_data().decode(sys.getdefaultencoding()))
    movie_json_is_not_empty = bool(movie_json)
    assert movie_json_is_not_empty == False


def test_perform_simple_query_actors(loaded_client):
    actor_details = loaded_client.get('/actors?age=61')
    actor_json = json.loads(actor_details.get_data().decode(sys.getdefaultencoding()))
    expected_dict = {
        'Bruce Willis': {'json_class': 'Actor', 'name': 'Bruce Willis', 'age': 61, 'total_gross': 562709189,
                         'movies': ['The First Deadly Sin', 'The Verdict']}}
    assert expected_dict.__eq__(actor_json)

    actor_details = loaded_client.get('/actors?age=61&age=71')
    actor_json = json.loads(actor_details.get_data().decode(sys.getdefaultencoding()))
    actor_json_is_not_empty = bool(actor_json)
    assert actor_json_is_not_empty == False


def test_perform_complex_query_actors(loaded_client):
    actor_details = loaded_client.get('/actors?age=61|age=76')
    actor_json = json.loads(actor_details.get_data().decode(sys.getdefaultencoding()))
    expected_dict = {
        'Bruce Willis': {'json_class': 'Actor', 'name': 'Bruce Willis', 'age': 61, 'total_gross': 562709189,
                         'movies': ['The First Deadly Sin', 'The Verdict']},
        'Faye Dunaway': {'json_class': 'Actor', 'name': 'Faye Dunaway', 'age': 76, 'total_gross': 515893034,
                         'movies': ['The First Deadly Sin']}}
    assert expected_dict.__eq__(actor_json)


def test_simple_post(sample_client):
    # Test that we can add an actor
    sample_client.post('/actors', data=json.dumps({"name": "Bruce Wayne"}),
                       headers={"Content-Type": "application/json"})
    actor_details = sample_client.get('/actors/Bruce Wayne')
    actor_dict = json.loads(actor_details.get_data().decode(sys.getdefaultencoding()))
    expected_dict = {'json_class': 'Actor', 'name': 'Bruce Wayne', 'age': 0, 'total_gross': 0, 'movies': []}
    assert expected_dict.__eq__(actor_dict)

    # Test that if we mis-spell a field, then we don't crash
    sample_client.post('/actors', data=json.dumps({"name": "Bruce Wayne", "aged": 40, "total_earnings": 50}),
                       headers={"Content-Type": "application/json"})
    actor_details = sample_client.get('/actors/Bruce Wayne')
    actor_dict = json.loads(actor_details.get_data().decode(sys.getdefaultencoding()))
    expected_dict = {'json_class': 'Actor', 'name': 'Bruce Wayne', 'age': 0, 'total_gross': 50, 'movies': []}
    assert expected_dict.__eq__(actor_dict)

    # Test that we can specify multiple fields
    sample_client.post('/actors', data=json.dumps({"name": "Bruce Wayne", "age": 40, "total_earnings": 50}),
                       headers={"Content-Type": "application/json"})
    actor_details = sample_client.get('/actors/Bruce Wayne')
    actor_dict = json.loads(actor_details.get_data().decode(sys.getdefaultencoding()))
    expected_dict = {'json_class': 'Actor', 'name': 'Bruce Wayne', 'age': 40, 'total_gross': 50, 'movies': []}
    assert expected_dict.__eq__(actor_dict)


def test_complex_post(sample_client):
    sample_client.post('/movies', data=json.dumps({"name": "Batman"}), headers={"Content-Type": "application/json"})
    sample_client.post('/movies', data=json.dumps({"name": "Robin"}), headers={"Content-Type": "application/json"})
    sample_client.post('/actors', data=json.dumps(
        {"name": "Bruce Wayne", "age": 40, "total_earnings": 50, "movies": ["Batman", "Robin"]}),
                       headers={"Content-Type": "application/json"})

    actor_details = sample_client.get('/actors/Bruce Wayne')
    actor_dict = json.loads(actor_details.get_data().decode(sys.getdefaultencoding()))
    expected_dict = {'json_class': 'Actor', 'name': 'Bruce Wayne', 'age': 40, 'total_gross': 50,
                     'movies': ["Batman", "Robin"]}
    assert expected_dict.__eq__(actor_dict)

    movie_details = sample_client.get('/movies/Batman')
    movie_dict = json.loads(movie_details.get_data().decode(sys.getdefaultencoding()))
    expected_dict = {'json_class': 'Movie', 'name': 'Batman', 'wiki_page': None, 'box_office': 0, 'year': 0,
                     'actors': ['Bruce Wayne']}
    assert expected_dict.__eq__(movie_dict)


def test_simple_post_movie(sample_client):
    sample_client.post('/movies', data=json.dumps({"name": "Batman"}), headers={"Content-Type": "application/json"})
    actor_details = sample_client.get('/movies/Batman')
    actor_dict = json.loads(actor_details.get_data().decode(sys.getdefaultencoding()))
    expected_dict = {'json_class': 'Movie', 'name': 'Batman', 'wiki_page': None, 'box_office': 0, 'year': 0,
                     'actors': []}
    assert expected_dict.__eq__(actor_dict)

def test_simple_put_movie(sample_client):
    sample_client.post('/movies', data=json.dumps({"name": "Batman"}), headers={"Content-Type": "application/json"})
    actor_details = sample_client.get('/movies/Batman')
    actor_dict = json.loads(actor_details.get_data().decode(sys.getdefaultencoding()))
    expected_dict = {'json_class': 'Movie', 'name': 'Batman', 'wiki_page': None, 'box_office': 0, 'year': 0,
                     'actors': []}
    assert expected_dict.__eq__(actor_dict)

    sample_client.post('/actors', data=json.dumps({"name": "Bruce Wayne"}), headers={"Content-Type": "application/json"})
    sample_client.put('/movies/m/Batman', data=json.dumps({"actors": ["Bruce Wayne"]}),
                      headers={"Content-Type": "application/json"})

# def test_delete(loaded_client):
#     loaded_client.delete('/actors/Bruce Willis', headers={"Content-Type": "application/json"})
#     actor_details = loaded_client.get('/actors/Bruce Willis')
#     actor_dict = json.loads(actor_details.get_data().decode(sys.getdefaultencoding()))
#
#     actor_dict_is_not_empty = bool(actor_dict)
#     assert actor_dict_is_not_empty == False
#
#     movie_details = loaded_client.get('/movies/The First Deadly Sin')
#     movie_dict = json.loads(movie_details.get_data().decode(sys.getdefaultencoding()))
#
#     print(movie_dict)


def test_parse_operator():
    query = "name=Aahan&age=21"
    output_array = ['name=Aahan', 'age=21']
    assert output_array.__eq__(parse_operator(query))


def test_parseAttr():
    query = "name=Aahan"
    output_dict = {'name': ['Aahan']}
    query_dict = dict()
    parseAttr(query, query_dict)
    assert query_dict.__eq__(output_dict)

    query = "name=Aahan"
    query_dict = dict()
    parseAttr(query, query_dict)
    query = "name=Bob"
    parseAttr(query, query_dict)
    output_dict = {'name': ['Aahan', 'Bob']}
    assert query_dict.__eq__(output_dict)


def test_is_num():
    true_string = "9"
    false_string = "hi"

    assert (is_num(true_string) == True)
    assert (is_num(false_string) == False)

# def test_perform_and_query(loaded_client):
#     movie_details = loaded_client.get('/actors?name=Bruce&name=Faye')
#     movie_json = json.loads(movie_details.get_data().decode(sys.getdefaultencoding()))
#
#     with open("small_data.json", "r") as fd:
#         small_data = json.load(fd)
#     # print(movie_json)
#     # print(small_data[1]['The First Deadly Sin'])
#     assert movie_json.__eq__(small_data[1]['The First Deadly Sin'])
#
# def test_perform_or_query(loaded_client):
#     movie_details = loaded_client.get('/actors?name=Bruce&name=joe')
#     movie_json = json.loads(movie_details.get_data().decode(sys.getdefaultencoding()))
#
#     with open("small_data.json", "r") as fd:
#         small_data = json.load(fd)
#     # print(movie_json)
#     # print(small_data[1]['The First Deadly Sin'])
#     assert movie_json.__eq__(small_data[1]['The First Deadly Sin'])
