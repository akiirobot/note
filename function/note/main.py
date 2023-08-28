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
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
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
def notes():
    return """
    <script>
        var formSubmitting = false;
        var setFormSubmitting = function() { formSubmitting = true; };
        window.onload = function() {
            window.addEventListener("beforeunload", function (e) {
                if (formSubmitting) {
                    return undefined;
                }

                var confirmationMessage = 'It looks like you have been editing something. '
                                        + 'If you leave before saving, your changes will be lost.';
                
                (e || window.event).returnValue = confirmationMessage; //Gecko + IE
                return confirmationMessage; //Gecko + Webkit, Safari, Chrome etc.
            });
        };
    </script>
    <form action="/notes" method="post" onsubmit="setFormSubmitting()">
    <label for="text">Text:</label><br>
    <textarea name="text" rows="30" cols="120" required></textarea>
    <input type="submit" value="Submit">
    </form>
    """, 200

def check_collision(key):
    doc_ref = db.collection(u'note').document(key)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.delete()
    return doc.exists

def random_key(length):
   letters = "0123456789abcdefghjkmnopqrstuvwxyzABCDEFGHJKMNOPQRSTUVWXYZ"
   return ''.join(random.choice(letters) for i in range(length))

@app.route("/notes/<string:key>", methods=["GET"])
def get_note(key):
    doc_ref = db.collection(u'note').document(key)

    doc = doc_ref.get()
    if doc.exists:
        obj = doc.to_dict()

        return """
        <pre>{}</pre>
        """.format(obj['Text']), 200
    else:
        return "404", 404


@app.route("/notes", methods=["POST"])
def create_note():

    text = request.form.get('text', default="", type = str)

    if not text.strip():
        return "not text", 400

    key = random_key(3)
    while check_collision(key):
        key = random_key(3)

    doc_ref = db.collection(u'note').document(key)

    doc_ref.set({
        u'Timestamp': firestore.SERVER_TIMESTAMP,  # datetime.datetime.now()
        u'Key': key,
        u'Text': text,
    })

    return "OK "+key, 200

