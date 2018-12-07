import re
import requests
import flask
from flask import request
import json
from pathlib import Path
from datetime import datetime as dt
from ..lib.parse_hubitat_log import parse_log_line
from ..config import MANUAL_LOG_ENTRIES_PATH, FLASK_ROOT_PATH
from ..app import app



def get_mock_data():
    with open(Path(__file__).parent / 'data' / 'past.html', 'r') as fp:
        past_page = fp.read()
    return past_page


def get_manual_logs():
    try:
        with MANUAL_LOG_ENTRIES_PATH.open() as fp:
            logs_text = fp.readlines()
    except Exception as err:
        print(f'Error reading from Manual Log Entry file. ({MANUAL_LOG_ENTRIES_PATH}). Error: {err}')
        return []

    logs = [json.loads(log) for log in logs_text]
    return logs


@app.route('/api/logs/past')
def logs_past():
    mock_data = flask.request.args.get('mock_data', False)
    max_log_lines =  int(flask.request.args.get('max_log_lines', 0))

    if mock_data and mock_data.lower() == 'true':
        print('Using MOCK data')
        content = get_mock_data()
    else:
        ipaddress = flask.request.args.get('hubitat_ip')
        ipaddressre1 = re.compile(r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(:[0-9]+)?')
        ipaddressre2 = re.compile(r'^(localhost)(:[0-9]+)?')

        if not ipaddress or (not ipaddressre1.match(ipaddress) and not ipaddressre2.match(ipaddress)):
            return f'Improper ip address received: |{ipaddress}|', 400

        url = f'http://{ipaddress}/logs/past'
        try:
            r = requests.get(url)
        except Exception as err:
            return f'Could not retrieve url ({url}). Err: {err}', 500
        if not r.ok:
            return f'Error retrieving url ({url}). Err: {r.status_code} -- {r.reason}', 500
        content = r.content.decode('utf-8')

    logline_text = re.search(r'^\s*var logs = (\[.*\])$', content, flags=re.MULTILINE)
    if not logline_text:
        return f'Error unexpected format of past page', 500
    loglines = json.loads(logline_text.group(1))
    logdata = [parse_log_line(line) for line in loglines]

    manual_logs = get_manual_logs()
    def get_date(rec):
        time = rec['time'].upper()
        if re.search('(AM)|(PM)', time):
            return dt.strptime(time, '%Y-%m-%d %H:%M:%S.%f %p')
        else:
            return dt.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    combined_logs = sorted(manual_logs+logdata, key=get_date, reverse=True)


    if max_log_lines:
        combined_logs = combined_logs[0:max_log_lines]  # Inefficient to do after parse, but easier

    return flask.jsonify(combined_logs)


@app.route('/api/logs/add_manual_entry', methods={'POST'})
def logs_add_manual_entry():
    try:
        with MANUAL_LOG_ENTRIES_PATH.open(mode='a') as fp:
            fp.write(request.data.decode('UTF-8')+'\n')
    except Exception as err:
        print(f'Error writing to Manual Log Entry file. ({MANUAL_LOG_ENTRIES_PATH}). Error: {err}')
        return "Error writing to file", 500
    return "Success", 200

@app.route('/api/ping', methods={'GET'})
def ping():
    return flask.jsonify({'ping': 'success'})

