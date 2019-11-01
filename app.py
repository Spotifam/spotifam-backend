# app.py
#https://stackabuse.com/deploying-a-flask-application-to-heroku/
import requests
from flask import Flask, request, jsonify
app = Flask(__name__)

TEST_TOK = ""
room_tokens = {
    "test_room": TEST_TOK,
}

@app.route('/createroom/', methods=['GET'])
def createroom():
    # Retrieve the name from url parameter
    room_id = request.args.get("room_id", None)

    # For debugging
    print(f"got room_id: {room_id}")

    response = {}

    # Check if user sent a name at all
    if not room_id:
        response["ERROR"] = "no id found, please send a name."
    # todo return if invalid songid
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Successfully recieved room_id"

    # Return the response in json format
    return jsonify(response)

@app.route('/getqueue/', methods=['GET'])
def getqueue():
    

    response = {}

    #TODO retrieve queue and insert 
    response["List"] = f"todo: actually return queue"

    # Return the response in json format
    return jsonify(response)

@app.route('/addsong/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    song_id = request.args.get("song_id", None)

    # For debugging
    print(f"got name {song_id}")

    response = {}

    # Check if user sent a name at all
    if not song_id:
        response["ERROR"] = "no id found, please send a name."
    #todo return if invalid songid
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Successfully recieved song_id"

    # Return the response in json format
    return jsonify(response)

@app.route('/search/', methods=['GET'])
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

    search_response = requests.get(
        "https://api.spotify.com/v1/search",
        params = {
            'q'    :   query,
            'type' : 'track',
        },
        headers = {
            'Accept'        :            'application/json',
            'Content-Type'  :            'application/json',
            'Authorization' : 'Bearer ' + room_tokens[room],
        }
    )

    if search_response.status_code == 200:
        return search_response.content
    else:
        return jsonify({
            "ERROR"    :     search_response.status_code,
            "MESSAGE:" : f"No results found for {query}",
        })

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
    app.run(threaded=True, port=5000)