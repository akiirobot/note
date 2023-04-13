import os
import datetime
import re
import json
import string
import random
import requests
from datetime import datetime, timezone, timedelta

from bs4 import BeautifulSoup
from flask import Flask, request
from google.cloud import firestore
import functions_framework
import jsonpickle

if __debug__:
    project_id = "note-376412"
else:
    project_id = os.environ['GCP_PROJECT']

app = Flask(__name__)
db = firestore.Client(project=project_id)

# Register an HTTP function with the Functions Framework
# Your function is passed a single parameter, (request), which is a Flask Request object.
# https://flask.palletsprojects.com/en/1.0.x/api/#flask.Request
@functions_framework.http
def entrypoint(request):
    # Create a new app context for the app
    internal_ctx = app.test_request_context(
        path=request.full_path, method=request.method
    )
    # Copy the request headers to the app context
    internal_ctx.request = request
    # Activate the context
    internal_ctx.push()
    # Dispatch the request to the internal app and get the result
    return_value = app.full_dispatch_request()
    # Offload the context
    internal_ctx.pop()
    # Return the result of the internal app routing and processing
    return return_value

@app.route("/", methods=["GET"])
def home():
    tz_string = str(datetime.now())

    return "<h1>" + tz_string + "</h1>" + \
    """
    <form>
    <label for="timestamp">Timestamp:</label><br>
    <input type="text" id="timestamp" name="timestamp"><br>
    <input type="submit" value="Submit">
    </form>
    """, 200

    return "<h1>" + tz_string + "</h1>", 200

@app.route("/notes", methods=["GET"])
def notes():
    return """
    <form action="/notes" method="post">
    <label for="key">Key:</label><br>
    <input type="text" id="key" name="key"><br>
    <label for="title">Title:</label><br>
    <input type="text" id="title" name="title"><br>
    <label for="text">Text:</label><br>
    <textarea name="text" rows="30" cols="120"></textarea>
    <input type="submit" value="Submit">
    </form>
    """, 200

def check_collision(key):
    doc_ref = db.collection(u'note').document(key)
    doc = doc_ref.get()
    return doc.exists

@app.route("/notes/<string:key>", methods=["GET"])
def get_note(key):
    doc_ref = db.collection(u'note').document(key)

    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
        obj = doc.to_dict()

        return """
        <h1>{}</h1><br>
        <pre>{}</pre>
        """.format(obj['Title'], obj['Text']), 200
    else:
        return "404", 404


@app.route("/notes", methods=["POST"])
def create_note():

    print("POST")
    print(request.form.get('title', default="bbb"))

    key = request.form.get('key', default="", type = str)
    title = request.form.get('title', default="", type = str)
    text = request.form.get('text', default="", type = str)

    if key:
        if check_collision(key):
            return "Key Exists", 400
    else: # not key
        key = id_generator(6)
        while check_collision(key):
            key = id_generator(6)

    time = get_current_time()

    doc_ref = db.collection(u'note').document(key)

    doc_ref.set({
        u'Timestamp': time,
        u'Key': key,
        u'Title': title,
        u'Text': text,
    })

    return "OK", 200

