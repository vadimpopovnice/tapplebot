import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram import executor
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "credentials.json")

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = '1LNJAvnjotJiDnO3Rs4SaMbnQ8ZC7LVXrSuFewxSuAH0'
SAMPLE_RANGE_NAME = 'Лист1'

service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()

result = service.get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                     range=SAMPLE_RANGE_NAME).execute()
date_from_sheet = result.get('values', [])

cell = 1


@dp.message_handler(content_types=['text'])
async def updatelist(message: types.Message):
    global cell
    range_ = f"Лист1!A{cell}:C{cell}"
    array = {'values': [[message.from_user.id, message.from_user.first_name, message.text]]}
    response = service.update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                              range=range_,
                              valueInputOption="USER_ENTERED",
                              body=array).execute()
    cell = cell + 1
    await message.answer("Заполнено!")


if __name__ == "__main__":
    executor.start_polling(dp)
