from flask import Flask,request,render_template
from .core.server import Server
from .core.client import Client

app = Flask(__name__)
server, server_address = Server.get_server_instance()
print(f"Request Accepted. Socket server started at port {server_address}")

client_sockets = {}


@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "GET":
        print("request received.")
        return render_template("index.html")

    elif request.method == "POST":
        username = request.form['username']
        print("username::",username)

        if username in client_sockets.keys():
            return "Username already taken. Please use another username."
        client = Client.get_client_instance()
        client_sockets[username] = client
        client.connect()

        return client.receive_message()


@app.route('/send',methods=["POST"])
def send():
    if request.method == "POST":
        message = request.form['message']
        username = request.form['username']

        if username in client_sockets.keys():
            return client_sockets[username].send_message(message.encode('utf-8'))
        else:
            return "Username error.! No user with the given username found."
    else:
        return


@app.route('/receive',methods=["POST"])
def receive():
    if request.method == "POST":
        username = request.form['username']

        if username in client_sockets.keys():
            message = client_sockets[username].receive_message()
            return message
        else:
            return "Username error.! No user with the given username found."
    else:
        return