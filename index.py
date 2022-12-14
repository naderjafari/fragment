import re
from flask import Flask, request
import telegram
import logging
from telebot.credentials import bot_token, bot_user_name, URL

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    print('Request:', request.get_json(force=True))
    print('Bot: ', bot)
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    print('Update: ', update)
    print('Update Message: ', update.message)

    # Telegram understands UTF-8, so encode text for unicode compatibility

    if (update.message is not None and update.message.text is not None):
        chat_id = update.message.chat.id
        msg_id = update.message.message_id
        text = update.message.text.encode('utf-8').decode()
        print("Chat ID: ",chat_id)
        print("Message Id: ",msg_id)

        # for debugging purposes only
        print("got text message :", text)
        # the first time you chat with the bot AKA the welcoming message
        if text == "/start":
            # print the welcoming message
            bot_welcome = """
        Welcome to coolAvatar bot, the bot is using the service from http://avatars.adorable.io/ to generate cool looking avatars based on the name you enter so please enter a name and the bot will reply with an avatar for your name.
        """
            # send the welcoming message
            bot.sendMessage(chat_id=chat_id, text=bot_welcome)

        else:
            try:
                # clear the message we got from any non alphabets
                text = re.sub(r"\W", "_", text)
                # create the api link for the avatar based on http://avatars.adorable.io/
                url = "https://api.adorable.io/avatars/285/{}.png".format(
                    text.strip())
                # reply with a photo to the name the user sent,
                # note that you can send photos by url and telegram will fetch it for you
                bot.sendPhoto(chat_id=chat_id, photo=url)
            except Exception:
                # if things went wrong
                bot.sendMessage(
                    chat_id=chat_id, text="There was a problem in the name you used, please enter different name")
    else:
        print('Bad Message')
    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'
