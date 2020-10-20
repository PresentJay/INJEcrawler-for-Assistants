import dotenv
import os
import json

# get environment variables from .env file
dotenv.load_dotenv(verbose=True, encoding='UTF8')
# get config variables from config.json file
with open("config.json") as file:
    config = json.load(file)

HOME = os.getenv('HOME')
TARGET = os.getenv('TARGET')
PAGE = os.getenv('PAGE')
CATEGORY = os.getenv('CATEGORY')
CATEGORY_TARGET = os.getenv('CATEGORY_TARGET')
MOD = os.getenv('MOD')
ID = os.getenv('ID')
PW = os.getenv('PW')

URL_PREV = HOME + TARGET + PAGE
URL_NEXT = CATEGORY + CATEGORY_TARGET

DETAIL_MOD =os.getenv('DETAIL_MOD')

DOWNLOAD_UID_PREV = os.getenv('DOWNLOAD_UID_PREV')
DOWNLOAD_ACTION = os.getenv('DOWNLOAD_ACTION')
DOWNLOAD_UID_NEXT = os.getenv('DOWNLOAD_UID_NEXT')
DOWNLOAD_NONCE = os.getenv('DOWNLOAD_NONCE')

DOWNLOAD_PREV = HOME + DOWNLOAD_ACTION + DOWNLOAD_UID_PREV
DOWNLOAD_NEXT = DOWNLOAD_UID_NEXT + DOWNLOAD_NONCE

SUBJECT = os.getenv('SUBJECT')
LOGIN_URL = os.getenv('LOGIN_URL')


def unzip__projectfiles(obj):
    for _ in config['PROJECTFILES']:
        obj.append(_)
