# Gemini Linebot GCP

## Project Background

## Screenshot_Image Replay
![image](https://github.com/jerryold/linebot-gemini-gcp/assets/12774427/22e9ccf7-ebdb-44a6-b58d-419bbc70ae50)

![image](https://github.com/jerryold/linebot-gemini-gcp/assets/12774427/465d2caf-d91c-45f4-b3ce-c217660f1aa0)




## Features

## Technologies Used
- Python 3
- FastAPI
- LINE Messaging API
- Google Generative AI
- Aiohttp
- PIL (Python Imaging Library)

## Setup

1. Set the following environment variables:
   - `ChannelSecret`: Your LINE channel secret.
   - `ChannelAccessToken`: Your LINE channel access token.
   - `GEMINI_API_KEY`: Your Gemini API key for AI processing.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Start the FastAPI server with `uvicorn main:app --reload`.

## Usage

To use the Receipt Helper, send a picture of your receipt to the LINE bot. The bot will process the image, extract the data, and provide a JSON representation of the receipt. For text-based commands or queries, simply send the command or query as a message to the bot.

## Commands

- `!清空`: Clears all the scanned receipt history for the user.

## Qrcode
If you'd like to use the chatbot, please feel free to scan qrcode to add friend.
|:--:|:--:|
| ![Chatbot_new](https://github.com/jerryold/linebot-gemini-gcp/assets/12774427/839dae13-2d64-4ca5-bbde-02958b44881e) | ![qrcode](https://github.com/jerryold/linebot-gemini-gcp/assets/12774427/a9d32b33-cd32-4bdf-b035-21349b170ba8) |


