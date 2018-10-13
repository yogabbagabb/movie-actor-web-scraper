# from unittest import TestCase

import pytest
import json
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
    print(actor_json)
    print(small_data[0]['Bruce Willis'])
    assert actor_json.__eq__(small_data[0]['Bruce Willis'])


# Test getting all the attributes of a single movie
def test_get_whole_actor(loaded_client):
    movie_details = loaded_client.get('/movies/The First Deadly Sin')
    movie_json = json.loads(movie_details.get_data().decode(sys.getdefaultencoding()))

    with open("small_data.json", "r") as fd:
        small_data = json.load(fd)
    print(movie_json)
    print(small_data[1]['The First Deadly Sin'])
    assert movie_json.__eq__(small_data[1]['The First Deadly Sin'])
