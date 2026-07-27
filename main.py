from bot import Bot
import pyrogram.utils
from flask import Flask
from threading import Thread
import os

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'UNRATED CODER FileStore'

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

import traceback
import time
from pyrogram.errors import FloodWait

if __name__ == "__main__":
    Thread(target=run, daemon=True).start()
    while True:
        try:
            Bot().run()
        except FloodWait as e:
            print(f"FloodWait: {e.x} seconds")
            time.sleep(e.x)
        except Exception:
            print(f"FATAL: Bot crashed at startup")
            traceback.print_exc()
            time.sleep(10)
