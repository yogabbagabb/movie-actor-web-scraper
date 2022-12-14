from movie_actor_app.graphs.Graph import *
from movie_actor_app.graphs.Record import *
from movie_actor_app.graphs.ParseData import parse_data

from flask import Flask
from flask import request
from flask import abort


def parse_operator(query_string):
    """
    Split a query by the logical operator (if it exists) that exists in it.
    We assume that only one logical operator will exist in a query, and that the
    operator will be AND (&) xor OR (|)
    :param query_string: The complete query string
    :return: An array of strings that have no logical operators in them; each string represents
    an attribute query
    """
    if "&" in query_string:
        return query_string.split("&"), 0
    elif "|" in query_string:
        return query_string.split("|"), 1
    else:
        return [query_string], 2


def parseAttr(definition_string, query_dict):
    """
    Split an attribute query (ie a attribute=value assignment) into
    an array of two strings, the key and value respectively
    :param definition_string: The attribute query
    :param query_dict: A dictionary to add {attribute=value} into
    :return:
    """
    tokens = definition_string.split("=")
    key = tokens[0]
    if is_num(tokens[1]):
        value = int(tokens[1])
    else:
        value = tokens[1]
    if query_dict.__contains__(tokens[0]):
        query_dict[tokens[0]].append(tokens[1])
    else:
        query_dict[tokens[0]] = [tokens[1]]


def is_num(string):
    """
    Check if a string represents a number
    :param string: A string, possibly representing a number
    :return: Whether the string represents a number or not
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def create_app(graph_record=None):
    app = Flask(__name__)
    if graph_record is None:
        graph = Graph()
    else:
        graph = parse_data(graph_record)

    @app.route('/')
    def index():
        return "Hello, World!"

    @app.route('/movies', methods=['POST'])
    @app.route('/actors', methods=['POST'])
    def add_record():
        if not request.is_json:
            abort(400)
        else:
            neighbor_string, query_type = get_identity_params()

            bio_data, neighbor_names = get_bio_data(neighbor_string)

            # Create a suitable vertex for addition into the graph
            record = ActorRecord(bio_data['name'], query_type) if query_type == Type.ACTOR else MovieRecord(
                bio_data['name'], query_type)

            # Add the record and any data that accompanied it
            graph.add(record)
            graph.update_bio(record, bio_data)

            name_of_record = bio_data['name']
            connect_to_neighbors(name_of_record, neighbor_names, query_type)

        return json.dumps({"Message": "Created"}), 201

    def connect_to_neighbors(record_name, neighbor_names, query_type):
        """
        Connect the node corresponding to record_name with all its neighbors, whose names are in
        neighbor_names.
        :param record_name: The name (a string) of the record that we wish to connect to its neighbors.
        :param neighbor_names: A list of strings of neighbor names
        :param query_type: The type of record of the node corresponding to record_name
        :return: None
        """
        # Determine what a neighbor's query type is
        neighbor_query_type = Type.MOVIE if query_type == Type.ACTOR else Type.ACTOR
        if neighbor_names is not None:
            for name in neighbor_names:
                # Connect the posted node with nodes corresponding to its
                # passed in neighbors' names only if a neighbor node corresponding to the name exists
                if graph.contains_by_name(name, neighbor_query_type):
                    if query_type == Type.ACTOR:
                        graph.connect_by_name(record_name, name)
                    else:
                        graph.connect_by_name(name, record_name)

    def get_identity_params():
        """
        Get parameters indicating what type of record is being accessed (a movie or actor) and a string
        describing the category of nodes (actors or movies, respectively) that the record is connected to.
        :return: neighbor_string, query_type
        """
        rule = request.url_rule
        # Determine whether we are posting an actor or a movie
        if 'actors' in rule.rule:
            query_type = Type.ACTOR
            neighbor_string = "movies"
        else:
            query_type = Type.MOVIE
            neighbor_string = "actors"
        return neighbor_string, query_type

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

    @app.route('/actors', methods=['GET'])
    @app.route('/movies', methods=['GET'])
    def query_movie():
        neighbor_string, query_type = get_identity_params()

        queries, the_type = parse_operator(request.query_string.decode('utf-8'))

        and_type = 0
        or_type = 1

        query_dict = dict()
        for query in queries:
            parseAttr(query, query_dict)

        if the_type == and_type:
            return graph.query(query_type, query_dict, and_operator=True), 200

        elif the_type == or_type:
            return graph.query(query_type, query_dict, and_operator=False), 200
        # There was neither an AND (&) nor an OR (|) in the query; thus there is one entry in the query,
        # and we can parse it assuming that either the | or & operator was used -- it does not matter.
        else:
            return graph.query(query_type, query_dict), 200

    @app.route('/actors/<name>', methods=['DELETE'])
    @app.route('/movies/<name>', methods=['DELETE'])
    def delete_record(name):
        if not request.is_json:
            abort(400)
        _, record_type = get_identity_params()
        graph.delete(name, record_type)

        return json.dumps({"Message": "Deleted"}), 200

    @app.route('/actors/a/<name>', methods=['PUT'])
    @app.route('/movies/m/<name>', methods=['PUT'])
    def edit_record(name):
        if not request.is_json:
            abort(400)

        neighbor_string, query_type = get_identity_params()

        bio_data, neighbor_names = get_bio_data(neighbor_string)

        record = Record(name, query_type)

        graph.update_bio(record, bio_data)
        connect_to_neighbors(name, neighbor_names, query_type)

        return json.dumps({"Message": "Updated"}), 200

    def get_bio_data(neighbor_string):
        """
        Get the json that accompanies a post or put request with a Content-Type header set to application/json. :param
        neighbor_string: The string of the category of records that the vertex from the calling function is connected
        to :return: bio_data: The json as a dictionary, a list of neighbor names
        """
        # Get the data that accompanied the post request
        bio_data = request.get_json()
        # Get the list of neighbors to the entry to be posted if it exists
        neighbor_names = bio_data.get(neighbor_string)
        # Remove the list of neighbor names from the dictionary
        if neighbor_names is not None:
            del bio_data[neighbor_string]
        return bio_data, neighbor_names

    return app


if __name__ == '__main__':
    an_app = create_app("data.json")
    an_app.run(debug=True)
