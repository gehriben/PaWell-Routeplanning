import os
from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

"""@app.route('/road')
def snapToRoad():
    return render_template('roadSnapTest.html')

@app.route('/geojson')
def geoJSON():
    return render_template('geoJSONTest.html')"""