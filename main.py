import os
import asyncio
import pyrogram
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Environment variables
app_id = int(os.environ.get("app_id"))
api_hash = os.environ.get("api_hash")
bot_token = os.environ.get("bot_token")
custom_caption = os.environ.get("custom_caption", "`{file_name}`")

# Pyrogram Client
AutoCaptionBot = pyrogram.Client(
    name="AutoCaptionBot", api_id=app_id, api_hash=api_hash, bot_token=bot_token
)

start_message = """
<b>👋Hello {}</b>
<b>I am an AutoCaption bot</b>
<b>All you have to do is add me to your channel and I will show you my power</b>
<b>@TonyStark_Botz</b>"""

about_message = """
<b>• Name : [AutoCaption V1](t.me/{username})</b>
<b>• Developer : [TonyStark](https://t.me/Tony_Stark_75)</b>
<b>• Language : Python3</b>
<b>• Library : Pyrogram v{version}</b>
<b>• Updates : <a href=https://t.me/TonyStark_Botz>Click Here</a></b>
<b>• Source Code : <a href=https://github.com/PR0FESS0R-99/AutoCaption-Bot>Click Here</a></b>"""

@AutoCaptionBot.on_message(pyrogram.filters.private & pyrogram.filters.command(["start"]))
def start_command(bot, update):
    update.reply(
        start_message.format(update.from_user.mention),
        reply_markup=start_buttons(bot, update),
        parse_mode=pyrogram.enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

@AutoCaptionBot.on_callback_query(pyrogram.filters.regex("start"))
def start_callback(bot, update):
    update.message.edit(
        start_message.format(update.from_user.mention),
        reply_markup=start_buttons(bot, update.message),
        parse_mode=pyrogram.enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

@AutoCaptionBot.on_callback_query(pyrogram.filters.regex("about"))
def about_callback(bot, update):
    bot = bot.get_me()
    update.message.edit(
        about_message.format(version=pyrogram.__version__, username=bot.username),
        reply_markup=about_buttons(bot, update.message),
        parse_mode=pyrogram.enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

@AutoCaptionBot.on_message(pyrogram.filters.channel)
def edit_caption(bot, update: pyrogram.types.Message):
    if custom_caption:
        motech, _ = get_file_details(update)
        try:
            update.edit(custom_caption.format(file_name=motech.file_name))
        except pyrogram.errors.FloodWait as e:
            asyncio.sleep(e.value)
            update.edit(custom_caption.format(file_name=motech.file_name))
        except pyrogram.errors.MessageNotModified:
            pass

def get_file_details(update: pyrogram.types.Message):
    if update.media:
        for message_type in (
            "photo", "animation", "audio", "document",
            "video", "video_note", "voice", "sticker"
        ):
            obj = getattr(update, message_type)
            if obj:
                return obj, obj.file_id

def start_buttons(bot, update):
    bot = bot.get_me()
    buttons = [[
        pyrogram.types.InlineKeyboardButton("Updates", url="t.me/TonyStark_Botz"),
        pyrogram.types.InlineKeyboardButton("About 🤠", callback_data="about")
    ], [
        pyrogram.types.InlineKeyboardButton("➕️ Add To Your Channel ➕️", url=f"http://t.me/{bot.username}?startchannel=true")
    ]]
    return pyrogram.types.InlineKeyboardMarkup(buttons)

def about_buttons(bot, update):
    buttons = [[
        pyrogram.types.InlineKeyboardButton("🏠 Back To Home 🏠", callback_data="start")
    ]]
    return pyrogram.types.InlineKeyboardMarkup(buttons)

# Dummy web server
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"AutoCaptionBot is running!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, DummyServer)
    httpd.serve_forever()

if __name__ == "__main__":
    # Start dummy server in a new thread
    threading.Thread(target=run_dummy_server).start()
    # Run the bot
    AutoCaptionBot.run()

print("Telegram AutoCaption V1 Bot Start")
print("Bot Created By https://github.com/PR0FESS0R-99")