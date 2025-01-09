from flask import Flask, request, send_file
import secrets

app = Flask(__name__)
FLAG = "irisctf{testflag}"
ADMIN = "redacted"

valid_tokens = {}

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/giveflag")
def hello_world():
    if "token" not in request.args or "admin" not in request.cookies:
        return "Who are you?"

    token = request.args["token"]
    admin = request.cookies["admin"]
    if token not in valid_tokens or admin != ADMIN:
        return "Why are you?"

    valid_tokens[token] = True
    return "GG"

@app.route("/token")
def tok():
    token = secrets.token_hex(16)
    valid_tokens[token] = False
    return token

@app.route("/redeem", methods=["POST"])
def redeem():
    if "token" not in request.form:
        return "Give me token"

    token = request.form["token"]
    if token not in valid_tokens or valid_tokens[token] != True:
        return "Nice try."

    return FLAG

