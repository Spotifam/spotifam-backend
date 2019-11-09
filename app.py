# app.py
#https://stackabuse.com/deploying-a-flask-application-to-heroku/
import requests
import random
import string
import json
import os
from room import Room
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources= {
        r"/createroom":     {"origins": "*"},
        r"/getqueue":       {"origins": "*"},
        r"/search":         {"origins": "*"},
        r"/updatequeue":    {"origins": "*"},
        r"/addsong":        {"origins": "*"},
        r"/checkroom":      {"origins": "*"},
    })
app.config['CORS_HEADERS'] = 'Content-Type'

TEST_TOK = ""
rooms = {}

def generateRoomId():
    return ''.join(random.choices(string.ascii_uppercase, k=4))

@app.route('/createroom/', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def createroom():
    # Retrieve the name from url parameter
    auth_tok = request.args.get("auth_tok", None)
    print(auth_tok)

    # Make sure the RoomID doesnt exist.
    room_id = generateRoomId()
    while room_id in rooms:
        room_id = generateRoomId()

    # Insert the new room into the list of rooms
    room = Room(room_id, auth_tok)
    rooms[room_id] = room

    response = {}

    # Check if user sent a name at all
    if not auth_tok:
        response["ERROR"] = "Failed to create a room."
    # todo return if invalid songid
    # Now the user entered a valid name
    else:
        response["room"] = room_id
    
    print(rooms)
    # Return the response in json format
    return jsonify(response)

@app.route('/getqueue/', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getqueue():
    
    room_code = request.args.get("room_code", None)

    response = {}

    response["list"] = rooms[room_code].getQueue()

    return jsonify(response)

@app.route('/updatequeue/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def updatequeue():
    # Retrieve the name from url parameter
    queue = json.loads(request.form.get("queue", None))
    room = request.form.get("room", None)

    rooms[room].updateQueue(queue)

    response = {}

    # Check if user sent a name at all
    if not queue:
        response["ERROR"] = "no id found."
    #todo return if invalid songid
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Successfully updated queue."

    # Return the response in json format
    return jsonify(response)

@app.route('/addsong/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def addsong():
    # Retrieve the name from url parameter
    song = json.loads(request.form.get("song", None))
    room = request.form.get("room", None)

    rooms[room].addToQueue(song)

    response = {}

    # Check if user sent a name at all
    if not song:
        response["ERROR"] = "no id found."
    #todo return if invalid songid
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Successfully added song."

    # Return the response in json format
    return jsonify(response)

@app.route('/search/', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def search():
    ### For testing
    # (i) Get a spotify Oauth token from,
    #     https://developer.spotify.com/console/get-search-item/
    #     then copy and paste in TEST_TOK.
    # 
    # (ii) Send a get curl request with the parameters 
    #      - [str] query: the song name to search for
    #      - [str] auth: the users authorization token from spotify

    print(request)
    query = request.args.get('query', None)
    room  = request.args.get('room',  None)

    print(query + "\n" + room +'\n')

    search_response = requests.get(
        "https://api.spotify.com/v1/search",
        params = {
            'q'    :   query,
            'type' : 'track',
        },
        headers = {
            'Accept'        :            'application/json',
            'Content-Type'  :            'application/json',
            'Authorization' : 'Bearer ' + rooms[room].token,
        }
    )

    if search_response.status_code == 200:
        return search_response.content
    else:
        return jsonify({
            "ERROR"    :     search_response.status_code,
            "MESSAGE:" : f"No results found for {query}",
        })

@app.route('/checkroom/', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def checkroom():

    room = request.args.get('room', None)

    response = {}

    if room in rooms:
        response['exists'] = True
    else:
        response['exists'] = False

    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    print(request)
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to the Spotifam server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    port = int(os.environ.get("PORT", 5000))
    print("PORT: "+ port)
    app.run(threaded=True, port=port)