from flask import Flask
from threading import Thread
import logging

# ปิด Log ขยะของ Flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask('')

@app.route('/')
def home():
    return "<h1>🤖 SYSTEM STATUS: ONLINE</h1><p>Bot is running...</p>"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()