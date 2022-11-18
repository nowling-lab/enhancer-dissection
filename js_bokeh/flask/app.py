import os
import sys 
import webbrowser
from helpers import read_csv
from vis.table import get_table
from flask import Flask, request, render_template, session, redirect
from flask_cors import CORS
from bokeh.embed import json_item
import json
    
abs_path = os.path.abspath(sys.argv[1])

data = read_csv(abs_path)
data.set_index(['report_file_path'])

app = Flask(__name__)
CORS(app)

@app.route('/')
def gen_table():
    table = get_table(abs_path, data, {})
    return json.dumps(json_item(table))

if __name__ == '__main__':
    app.run()