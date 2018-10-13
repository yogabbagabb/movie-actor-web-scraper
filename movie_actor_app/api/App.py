from movie_actor_app.graphs.Graph import *
from movie_actor_app.graphs.Record import *
from movie_actor_app.graphs.ParseData import parse_data

from flask import Flask, jsonify
from flask import request
from flask import abort


def create_app(graph_record=None):
    app = Flask(__name__)
    if graph_record is None:
        graph = Graph()
    else:
        graph = parse_data(graph_record)

    @app.route('/')
    def index():
        return "Hello, World!"

    @app.route('/actors', methods=['POST'])
    def add_record():
        if not request.is_json:
            abort(400)
            print("Error")
        else:
            json_data = request.get_json()
            json_data['device'] = 'Aahan'
            return jsonify(json_data)
            # return json_data

    @app.route('/actors/<name>', methods=['GET'])
    def get_whole_actor(name):
        if graph.contains_by_name(name, Type.ACTOR):
            return graph.get_actor_json(name), 200
        else:
            abort(400)

    @app.route('/movies/<name>', methods=['GET'])
    def get_whole_movie(name):
        if graph.contains_by_name(name, Type.MOVIE):
            return graph.get_movie_json(name), 200
        else:
            abort(400)

    return app


if __name__ == '__main__':
    an_app = create_app()
    an_app.run(debug=True)
