import os
import json
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('fiK5JVpGVGIM2CGc4+1CSTLeVupHBdGFW+/Iddix9zusohj4Wxnpb3KmyANuFvW3FHxcaWyitcwqdl+xnaWAfaHGbZGS60CjG9KIrMAGvnRClRBNjJsWQYHLWyD57lPzFJ+g+G3HKGMaadWf3iJnXwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('351967b479cda699b4bc98225a253054')

with open('messages.json', 'rb') as f:
    reply_msgs = json.load(f)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.lower().strip()
    reply = reply_msgs.get(text, reply_msgs['help'])

    if text == 'work funpodium':
        message = [
            TextSendMessage(text=reply),
            TemplateSendMessage(
                alt_text=reply,
                template=ButtonsTemplate(
                    title='sw-project',
                    thumbnail_image_url='https://www.hcytlog.com/upload/GitHub-logo_202011055020_.png',
                    actions=[URIAction(label='view repo', uri='https://github.com/andy94077/sw-project')]
                )
            )
        ]
    else:
        message = TextSendMessage(text=reply)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
