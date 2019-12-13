'''
@Author: your name
@Date: 2019-12-11 10:19:16
@LastEditTime: 2019-12-11 10:19:46
@LastEditors: Please set LastEditors
@Description: In User Settings Edit  
@FilePath: \watchlist\wsgi.py
'''
import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.venv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from watchlist import app