from flask import Flask
from threading import Thread
import logging

# ปิด Log ขยะ
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>🤖 Bot is Online!</h1>"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
