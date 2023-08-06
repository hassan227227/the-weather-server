import collections
from typing import Collection, OrderedDict
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request
from flask_restful import Api
from datetime import datetime, timedelta
from numpy import record
import pandas as pd
import pyodbc
import constants
import json
import sqlite3
from flask import Flask, render_template   
# from pandas.io.json import json_normalize
# from werkzeug.exceptions import HTTPException
app = Flask(__name__)
cors = CORS(app)
api = Api(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
#dbConn = pyodbc.connect(constants.DB_CONNECT_CRED)



@app.route('/api', methods=['POST'])
@cross_origin()
def page():
    conn = get_db_connection()
    city = request.args.get('city')
    temp = request.args.get('temp')
    weatherDescription = request.args.get('weatherDescription')
    weatherMain = request.args.get('weatherMain')
    city = request.args.get('city')
    conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('lahore', '200')
            )
    conn.close()
    
    response = "<h1>This Api is for the weather app</p>"
    print(city, temp, weatherDescription, weatherMain)
    return jsonify({'response': response, 'status' : "SuccessFul"})


@app.route('/data', methods=['GET'])
@cross_origin()
def data():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    
    response = "<h1>This Api is for the weather app</p>"
    print(posts)
    return  posts




@app.route('/update-missing-PlCoords/', methods=['POST'])
@cross_origin()
def update_missing_plcoords():
    content = request.get_json(silent=True)
    z = jsonify(content["body"])
    data = json.loads(z.json)
    vSSLat = data['vSSLat']
    vSSLng = data['vSSLng']
    vESLat = data['vESLat']
    vESLng = data['vESLng']
    vPLCoords = data['vPLCoords']
 
    cursor = dbConn.cursor()
   
    query = "Exec usp_InsertUpdatePolylineCoordinates @iMode = ?, @vSSLat = ?, @vSSLng = ?, @vESLat = ?, @vESLng = ?, @vPLCoords = ?"
    values = (2, str(vSSLat), str(vSSLng), str(vESLat), str(vESLng), str(vPLCoords))
    cursor.execute(query, values)
    cursor.commit()
    cursor.close()
    return jsonify({'Success': 'Data is updated Successfully'})


@app.route('/save-od-reservation/', methods=['POST'])
@cross_origin()
def save_od_reservation():
    content = request.get_json(silent=True)
    z = jsonify(content["body"])
    data = json.dumps(z.json, separators=(',', ':'))
    data = json.loads(data)
    PassengerPhoneNo = data['PassengerPhoneNo']
    PassengerName = data['PassengerName']
    iStationID = data['iStationID']
    vStationAddress = data['vStationAddress']
    vStationCity = data['vStationCity']
    vStationState = data['vStationState']
    vStationZip = data['vStationZip']
    dtArrival = data['dtArrival']
    iRouteID = data['iRouteID']
    iDestStationID = data['iDestStationID']
    vCreatedBy = data['vCreatedBy']
    NearByStationMinTimeInMin = data['NearByStationMinTimeInMin']
    iStatusID = 0
    TripCount = 0
    cursor = dbConn.cursor()
   
    query = "Exec usp_SaveCancelODReservationForStation @vPhoneNo = ?, @vPersonName = ?, @iStationID = ?, @vStationAddress = ?, @vStationCity = ?, @vStationState = ?, @vStationZip = ?, @dtArrival = ?, @iRouteID = ?, @iDestStationID = ?, @vCreatedBy = ?, @iStatusID = ?, @NearByStationMinTimeInMin = ?"
    values = (str(PassengerPhoneNo), str(PassengerName), str(iStationID), str(vStationAddress), str(vStationCity), str(vStationState), str(vStationZip), str(dtArrival), str(iRouteID), str(iDestStationID), str(vCreatedBy), str(iStatusID), str(NearByStationMinTimeInMin))
    iResult = cursor.execute(query, values).fetchone()
    TripCount = iResult[0]
    cursor.commit()
    cursor.close()

    if TripCount == 0:
        return jsonify({'Result': 'This reservation already exists.'})
    elif TripCount == -1:
        return jsonify({'Result': 'Reservation time for selected station has expired. \nPlease choose the next available timeslot.'})
    elif TripCount > 0:
        return jsonify({'Result': 'Reservation saved successfully.'})
 


#define main and add the API endpoints
def __main__():
    api.add_resource(page, '/api')
    api.add_resource(data, '/data')
    api.add_resource(get_missing_pl_coords, '/get-missing-pl-coords')
    api.add_resource(update_missing_plcoords, '/update-missing-PlCoords')

if __name__ == "__main__":
    app.run(host='localhost', port='1222', debug=True, threaded=True)
