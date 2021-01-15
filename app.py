import os
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
    text = event.message.text.lower()
    if text == 'work history':
        reply = '''CMLab, National Taiwan University. Special Research Undergraduate, Jan. 2020 – Present.
Funpodium. Web Developer Intern, July 2020 – Aug. 2020.
AICS, ASUSTek COMPUTER INC. Software Engineering Intern, July 2019 – Aug. 2019.
'''
    elif text == 'skills':
        reply = 'C, C++, Python, Machine Learning, Deep Learning, React, Javascript'
    elif text == 'awards':
        reply = '''Honorable Mention, Special Research Exhibition – Department of Computer Science, National Taiwan University, June 2020.
Student Group Leaderboards Honorable Mention, Ministry of Education Intercollegiate AI CUP 2019 – Ministry of Education, Jan. 2020.
'''
    else:
        reply = u'''I am Yi-Rong Chen.
I'm a senior student at the Department of Computer Science, National Taiwan University. I specialize in frontend, backend, and deep learning. Type 
• "Work History" to show my working experience.
• "Skills" to show my programming skills.
• "Awards" to show awards I got.
Or, type "Help" to show this helping message.'''

    message = TextSendMessage(text=reply)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
