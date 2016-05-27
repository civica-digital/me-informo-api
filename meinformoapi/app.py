from json import dumps
import pandas as pd
import numpy as np

from flask import Flask, Response, request, send_file

import meinformoapi.calls as calls
import meinformoapi.tools as tools


app = Flask(__name__)
current_entities = calls.entities()
df_current_entities = pd.DataFrame(current_entities)
states_list = list(np.unique(df_current_entities["estado"]))


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


@app.route('/search', methods=['GET'])
def get_search():
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
def get_entities():
    output = current_entities
    return Response(dumps(output), mimetype='application/json')


@app.route('/entities/<entity_id>')
def get_entity(entity_id):
    entity_id = str(entity_id)
    output = tools.filter_dict(current_entities,"id", [entity_id])
    return Response(dumps(output), mimetype='application/json')


@app.route('/entities/states/')
def get_state_entities():
    output = states_list
    return Response(dumps(output), mimetype='application/json')


@app.route('/entities/states/<state_id>')
def get_state(state_id):
    state_id = str(state_id)
    output = tools.filter_dict(current_entities,"estado", [state_id])
    return Response(dumps(output), mimetype='application/json')


@app.route('/entities/states/<state_id>/sectors')
def get_sectors(state_id):
    state_id = str(state_id)
    filter_state = tools.filter_dict(current_entities,"estado", [state_id])
    df_filter_state = pd.DataFrame(filter_state)
    output = list(np.unique(df_filter_state["sector"]))
    return Response(dumps(output), mimetype='application/json')


@app.route('/entities/states/<state_id>/sectors/<sector_id>')
def get_sector(state_id,sector_id):
    state_id = str(state_id)
    sector_id = str(sector_id)
    filter_state = tools.filter_dict(current_entities,"estado", [state_id])
    output = tools.filter_dict(filter_state,"sector",[sector_id])
    return Response(dumps(output), mimetype='application/json')
