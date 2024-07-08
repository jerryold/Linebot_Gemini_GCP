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
| | |
|:--:|:--:|
| ![Chatbot](https://github.com/jerryold/linebot-gemini-gcp/assets/12774427/7c1650a4-9c82-48db-8b48-8f24c2d306c0) | ![image](https://github.com/jerryold/linebot-gemini-gcp/assets/12774427/9fb8c2a5-9d4a-49f7-933a-b69d800924a3) |

