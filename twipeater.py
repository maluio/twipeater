import json
import os
from datetime import datetime, timedelta

import twint
from flask import Flask, request

app = Flask(__name__)


@app.route('/tweets')
def get_feeds():
    temp_output_file = "output.json"
    if os.path.isfile(temp_output_file):
        os.remove(temp_output_file)

    username = request.args.get('username', None)
    if not username:
        return {"message": "Parameter 'username' is required"}, 400

    # https://github.com/twintproject/twint#more-examples
    c = twint.Config()
    c.Username = username
    c.Store_json = True
    c.Output = temp_output_file
    since_days = int(request.args.get('since-days', 7))
    since = datetime.now() - timedelta(days=since_days)
    c.Since = since.strftime("%Y-%m-%d %H:%M:%S")
    twint.run.Search(c)

    data = []
    with open(temp_output_file, 'r') as file:
        rows = file.readlines()
        for row in rows:
            data.append(json.loads(row))

    if os.path.isfile(temp_output_file):
        os.remove(temp_output_file)

    return {'data': data}
