import sys
import hydrogram
import hydrogram.types
import hydrogram.enums
import hydrogram.errors
import hydrogram.raw
import hydrogram.raw.types
import hydrogram.raw.base
import hydrogram.filters
import hydrogram.handlers

sys.modules["pyrogram"] = hydrogram
for name, module in list(sys.modules.items()):
    if name == "hydrogram" or name.startswith("hydrogram."):
        pyrogram_name = name.replace("hydrogram", "pyrogram", 1)
        sys.modules[pyrogram_name] = module

from hydrogram.raw import types as raw_types

original_init = hydrogram.types.InlineKeyboardButton.__init__

def patched_init(self, *args, style=None, **kwargs):
    original_init(self, *args, **kwargs)
    self.style = style

hydrogram.types.InlineKeyboardButton.__init__ = patched_init

original_write = hydrogram.types.InlineKeyboardButton.write

async def patched_write(self, client):
    style_type = getattr(self, "style", None)
    text = self.text
    if text and "#" in text:
        for keyword, s_type in [("#primary", "primary"), ("#danger", "danger"), ("#success", "success"), ("#succes", "success")]:
            if keyword in text.lower():
                style_type = s_type
                self.text = text.replace(keyword, "").replace(keyword.upper(), "").strip()
                break

    res_btn = await original_write(self, client)

    if style_type and hasattr(res_btn, "style"):
        bg_primary = style_type == "primary"
        bg_danger = style_type == "danger"
        bg_success = style_type == "success"
        res_btn.style = raw_types.KeyboardButtonStyle(
            bg_primary=bg_primary or None,
            bg_danger=bg_danger or None,
            bg_success=bg_success or None
        )
    return res_btn

hydrogram.types.InlineKeyboardButton.write = patched_write

from hydrogram.parser.html import Parser

original_handle_starttag = Parser.handle_starttag

def patched_handle_starttag(self, tag, attrs):
    original_handle_starttag(self, tag, attrs)
    if tag == "blockquote" and "expandable" in dict(attrs):
        if tag in self.tag_entities and self.tag_entities[tag]:
            self.tag_entities[tag][-1].collapsed = True

Parser.handle_starttag = patched_handle_starttag

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
