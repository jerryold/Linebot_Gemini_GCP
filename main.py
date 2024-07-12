from linebot.models import FlexSendMessage
from linebot.models import (
    FollowEvent, MessageEvent, TextSendMessage
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot import (
    AsyncLineBotApi, WebhookParser
)

from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from fastapi import Request, FastAPI, HTTPException
import google.generativeai as genai
import os
import sys
from io import BytesIO
# import aioschedule as schedule

from datetime import datetime
import pytz

import aiohttp
import PIL.Image
from firebase import firebase
import json
from pydantic import BaseModel
import requests

# # get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('ChannelSecret', None)
channel_access_token = os.getenv('ChannelAccessToken', None)
gemini_key = os.getenv('GEMINI_API_KEY')
firebase_url = os.getenv('FIREBASE_URL')






imgage_prompt = '''
Describe this image with scientific detail, reply in zh-TW:
'''



if channel_secret is None:
    print('Specify ChannelSecret as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify ChannelAccessToken as environment variable.')
    sys.exit(1)
if gemini_key is None:
    print('Specify GEMINI_API_KEY as environment variable.')
    sys.exit(1)
if firebase_url is None:
    print('Specify FIREBASE_URL as environment variable.')
    sys.exit(1)

# Initialize the FastAPI app for LINEBot
app = FastAPI()
session = aiohttp.ClientSession()
async_http_client = AiohttpAsyncHttpClient(session)
line_bot_api = AsyncLineBotApi(channel_access_token, async_http_client)
line_bot_api1 = LineBotApi(channel_access_token)

parser = WebhookParser(channel_secret)

# Initialize the Gemini Pro API
genai.configure(api_key=gemini_key)


global_user_ids=set()
global_group_ids = set()


def generate_gemini_text_complete(prompt):
    """
    Generate a text completion using the generative model.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response


def generate_result_from_image(img, prompt):
    """
    Generate a image vision result using the generative model.
    """

    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, img], stream=True)
    response.resolve()
    return response




@app.post("/usermessage")
async def send_user_message():
    
    result=generate_gemini_text_complete('https://goodinfo.tw/tw/StockAnnounceList.asp?START_DT=2024%2F7%2F6&END_DT=2024%2F7%2F12 \n,爬取這個網址並回傳股市訊息一覽和新聞')
    message = TextSendMessage(text=result.text)
    #create user_id list
    # user_id_list = ['Uf7bc16da786923d10a1a8f6110a8b947','U0a954d9a98db73941f98259b1f4bfb83',
    #                 'Ue821ac226937a52b9f1770c20bc7cc35','U6545179fe8bf5e9cf2cf260203447770', #friends
    #                 'U4debac703fd0890a031592ef7cd476c7','Ucdefd05a3c2bc3f5bedea00f191f1ace','U2f098e537327fc080ebd79b2ac485740'#family
    #                 ]
    for user_id in global_user_ids:
        try:
            line_bot_api1.push_message(user_id, message)
            print(f"Success to {user_id}")
        except LineBotApiError as e:
            print(f"Fail to {user_id} {e}")

    for group_id in global_group_ids:
        try:
            line_bot_api1.push_message(group_id, message)
            print(f"Success to {group_id}")
        except LineBotApiError as e:
            print(f"Fail to {group_id} {e}")
    
    return {"message": "Success to send message to user"}


@app.post("/afterworkmessage")
async def send_afterwork_message():
    
    result=generate_gemini_text_complete('please say some interesting word after work, and recommend type of dinner after work,please reply in zh-TW:')
    message = TextSendMessage(text=result.text)
    #create user_id list
    # user_id_list = ['Uf7bc16da786923d10a1a8f6110a8b947','U0a954d9a98db73941f98259b1f4bfb83',
    #                 'Ue821ac226937a52b9f1770c20bc7cc35','U6545179fe8bf5e9cf2cf260203447770', #friends
    #                 'U4debac703fd0890a031592ef7cd476c7','Ucdefd05a3c2bc3f5bedea00f191f1ace','U2f098e537327fc080ebd79b2ac485740'#family
    #                ]
    for user_id in global_user_ids:
        try:
            line_bot_api1.push_message(user_id, message)
            print(f"Success to {user_id}")
        except LineBotApiError as e:
            print(f"Fail to {user_id} {e}")

    for group_id in global_group_ids:
        try:
            line_bot_api1.push_message(group_id, message)
            print(f"Success to {group_id}")
        except LineBotApiError as e:
            print(f"Fail to {group_id} {e}")
    
    return {"message": "Success to send message to user"}



@app.post("/")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    for event in events: 
        if hasattr(event.source, 'group_id') and event.source.group_id not in global_group_ids:
            global_group_ids.add(event.source.group_id)
        if hasattr(event.source, 'user_id')  and event.source.user_id not in global_user_ids:
            global_user_ids.add(event.source.user_id)       
        

        
        if not isinstance(event, MessageEvent):
            continue        

        if (event.message.type == "text"):
            
            # Provide a default value for reply_msg
            msg = event.message.text
            ret = generate_gemini_text_complete(f'{msg}, reply in zh-TW:')
            # reply_text = ret.text + "\n" + str(event.source.user_id)
            reply_text = ret.text
            reply_msg = TextSendMessage(text=reply_text)
            await line_bot_api.reply_message(
                event.reply_token,                
                [reply_msg]  
            )
                        
        elif (event.message.type == "image"):
            message_content = await line_bot_api.get_message_content(
                event.message.id)
            image_content = b''
            async for s in message_content.iter_content():
                image_content += s
            img = PIL.Image.open(BytesIO(image_content))

            result = generate_result_from_image(img, imgage_prompt)
            reply_msg = TextSendMessage(text=result.text)
            await line_bot_api.reply_message(
                event.reply_token,
                reply_msg
            )
            return 'OK'
        else:
            continue

    return 'OK'


# @app.post("/")
# async def handle_callback(request: Request):
#     signature = request.headers['X-Line-Signature']

#     # get request body as text
#     body = await request.body()
#     body = body.decode()

#     try:
#         events = parser.parse(body, signature)
#     except InvalidSignatureError:
#         raise HTTPException(status_code=400, detail="Invalid signature")
    
#     for event in events:
#         if not isinstance(event, MessageEvent):
#             continue        

#         if (event.message.type == "text"):
#             # Provide a default value for reply_msg
#             msg = event.message.text
#             ret = generate_gemini_text_complete(f'{msg}, reply in zh-TW:')
#             reply_msg = TextSendMessage(text=ret.text)
#             await line_bot_api.reply_message(
#                 event.reply_token,
#                 reply_msg
#             )
#         elif (event.message.type == "image"):
#             message_content = await line_bot_api.get_message_content(
#                 event.message.id)
#             image_content = b''
#             async for s in message_content.iter_content():
#                 image_content += s
#             img = PIL.Image.open(BytesIO(image_content))

#             result = generate_result_from_image(img, imgage_prompt)
#             reply_msg = TextSendMessage(text=result.text)
#             await line_bot_api.reply_message(
#                 event.reply_token,
#                 reply_msg
#             )
#             return 'OK'
#         else:
#             continue

#     return 'OK'




