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
line_bot_api1=LineBotApi(channel_access_token)

parser = WebhookParser(channel_secret)

# Initialize the Gemini Pro API
genai.configure(api_key=gemini_key)

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
    
    # with open('user_info.json', 'r') as json_file:
    #     user_info = json.load(json_file)
        
    # user_id = user_info.get('user_id')
    
    # if user_id:
    #     message = TextSendMessage(text="this is test")
    #     try:
    #         line_bot_api.push_message(user_id, message)
    #         print(f"Success to {user_id}")
    #     except Exception as e:
    #         print(f"Fail to {user_id} {e}")
    # else:
    #     print("Did not find any user")
    # result=generate_gemini_text_complete(f'say good moring, reply in zh-TW:')
    message = TextSendMessage("Hello, this is a test message")
    try:
        
        line_bot_api1.push_message('U0a954d9a98db73941f98259b1f4bfb83', message)
        print(f"Success to U0a954d9a98db73941f98259b1f4bfb83")
    except Exception as e:
        print(f"Fail to U0a954d9a98db73941f98259b1f4bfb83 {e}")
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
        # i also want to make bot return the event user id
        if isinstance(event, FollowEvent):
            profile = line_bot_api.get_profile(event.source.user_id)
            user_info = {
                "user_id": profile.user_id,
                "display_name": profile.display_name
            }

            # file_name = "user_info.json"           
            # with open(file_name, 'w') as json_file:
            #     json.dump(user_info, json_file, ensure_ascii=False, indent=4)
            
            
            continue
        if not isinstance(event, MessageEvent):
            continue        

        if (event.message.type == "text"):
            # Provide a default value for reply_msg
            msg = event.message.text
            ret = generate_gemini_text_complete(f'{msg}, reply in zh-TW:')
            reply_text = ret.text + "\n" + str(event.source.user_id)
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




