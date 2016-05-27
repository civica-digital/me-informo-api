from json import dumps
import pandas as pd
import numpy as np

from flask import Flask, Response, request, send_file
from flask.ext.autodoc import Autodoc

import meinformoapi.calls as calls
import meinformoapi.tools as tools


app = Flask(__name__)
auto = Autodoc(app)

current_entities = calls.entities()
df_current_entities = pd.DataFrame(current_entities)
states_list = list(np.unique(df_current_entities["estado"]))
sectors_list = list(np.unique(df_current_entities["sector"]))


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


@app.route('/')
def documentation():
    return auto.html()


@app.route('/requests/search', methods=['GET'])
@auto.doc()
def get_search():
    """
    GET: Searches the Portal de Transparencia
    [params]
    query: Text to search <non escaped/string>
    page: results page <non escaped/string>
    resultspage: results to show per page <non escaped/string>
    https://meinformoapi.herokuapp.com/requests/search?query=Estado&page=2&resultspage=25
    """
    query = request.args.get('query')
    page = request.args.get('page')
    resultspage = request.args.get('resultspage')
    if query is None:
        query = "a"
    if page is None:
        page = "1"
    if resultspage == None:
        resultspage = "25"
    output = calls.foi_search(query,page,resultspage)
    return Response(dumps(output), mimetype='application/json')


@app.route('/entities/')
@auto.doc()
def get_entities():
    """
    GET: Gets all Entities on record
    https://meinformoapi.herokuapp.com/entities
    """
    output = current_entities
    return Response(dumps(output), mimetype='application/json')


@app.route('/entities/<entity_id>')
@auto.doc()
def get_entity(entity_id):
    """
    GET: Gets entities marked with such id
    Note: ids come from original site, may be duplicated.
    https://meinformoapi.herokuapp.com/entities/130
    """
    entity_id = str(entity_id)
    output = tools.filter_dict(current_entities,"id", [entity_id])
    return Response(dumps(output), mimetype='application/json')


@app.route('/entities/sectors/')
@auto.doc()
def get_sectors():
    """
    GET: Gets the sectors on the database
    https://meinformoapi.herokuapp.com/entities/sectors/
    """
    output = sectors_list
    return Response(dumps(output), mimetype='application/json')


@app.route('/entities/sectors/<sector_id>')
@auto.doc()
def get_sector(sector_id):
    """
    GET: Gets all Entities on the required sector.
    https://meinformoapi.herokuapp.com/entities/sectors/
    """
    sector_id = str(sector_id)
    output = tools.filter_dict(current_entities,"sector", [sector_id])
    return Response(dumps(output), mimetype='application/json')


@app.route('/entities/states/')
@auto.doc()
def get_state_entities():
    """
    GET: Gets all States on record
    https://meinformoapi.herokuapp.com/entities/states/
    """
    output = states_list
    return Response(dumps(output), mimetype='application/json')


@app.route('/entities/states/<state_id>')
@auto.doc()
def get_state(state_id):
    """
    GET: Gets all Entities on the selected state
    https://meinformoapi.herokuapp.com/entities/states/AGUASCALIENTES
    """
    state_id = str(state_id)
    output = tools.filter_dict(current_entities,"estado", [state_id])
    return Response(dumps(output), mimetype='application/json')


@app.route('/entities/states/<state_id>/sectors')
@auto.doc()
def get_state_sectors(state_id):
    """
    GET: Gets all Sectors on state
    https://meinformoapi.herokuapp.com/entities/states/AGUASCALIENTES/sectors
    """
    state_id = str(state_id)
    filter_state = tools.filter_dict(current_entities,"estado", [state_id])
    df_filter_state = pd.DataFrame(filter_state)
    output = list(np.unique(df_filter_state["sector"]))
    return Response(dumps(output), mimetype='application/json')


@app.route('/entities/states/<state_id>/sectors/<sector_id>')
@auto.doc()
def get_state_sector(state_id,sector_id):
    """
    GET: Gets all Entities on the selected sector and state
    https://meinformoapi.herokuapp.com/entities/states/AGUASCALIENTES/sectors/Judicial
    """
    state_id = str(state_id)
    sector_id = str(sector_id)
    filter_state = tools.filter_dict(current_entities,"estado", [state_id])
    output = tools.filter_dict(filter_state,"sector",[sector_id])
    return Response(dumps(output), mimetype='application/json')
