import thread

from data import *
from flask import Flask
app = Flask(__name__)

def run():
    print "starting web server..."
    app.run(host='0.0.0.0')

toggle_cb = None
brightness_cb = None

def setup(t, b):
    global toggle_cb
    global brightness_cb
    toggle_cb = t
    brightness_cb = b
    thread.start_new_thread(run, ())

@app.route("/toggle/<state>")
def toggle(state):
    return str(toggle_cb(state)).lower()

@app.route("/brightness/<level>")
def brightness(level):
    return str(brightness_cb(level)).lower()

