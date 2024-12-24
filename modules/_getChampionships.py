from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from tqdm import tqdm
import json
import time
import re
import pymongo
from modules.tools import *
import json
from modules.config import datas
import sys
import urllib.request
import ssl
import zlib
from modules import common
import requests

ssl._create_default_https_context = ssl._create_stdlib_context
# end Init Database
config_data = read_json('modules/config/config.json')
mongo_client = pymongo.MongoClient(config_data['mongo_host'] + ':' + config_data['mongo_port'])
mydb = mongo_client[config_data['mongo_db']]
mongo_table_matches = mydb[config_data['mongo_table_matches']]
DATETIME_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"
URL_DATETIME_FORMAT = "%Y-%m-%d"
UPDATETIME_FORMAT = "%d-%m-%YT%H:%M:%S"
DATETIME_FORMAT_MONGO = "%d-%m-%Y"

# a executer toutes les heures
# 24 appels + 24 appels = 48 appels
class AllFixtures:

    ######################################### CONSTRUCTOR ##########################################
    def __init__(self, webdriver_name='firefox', driver=None):
        self.url_progressive = 'https://soccer-football-info.p.rapidapi.com/matches/view/progressive/'

        start_date = '2024-01-01'
        end_date = '2024-03-31'

        self.language = "en_US"
        self.headers = config_data['header']
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        self.start_date_string = start.strftime('%Y-%m-%d')
        self.end_date_string = end.strftime('%Y-%m-%d')
        self.all_fixtures = list(mongo_table_matches.find({"date": {"$gte": self.start_date_string, "$lte": self.end_date_string}}).sort({'dateTime': 1}))
        self.league_names = set()
        self.j = 0
        self.k = 0
        self.updateMatchesProgressive()
        sorted_leagues = sorted(self.league_names)
        print('with dominance', self.j)
        print('without dominance', self.k)

    def updateMatchesProgressive(self):
        print("Trying to update data for " + str(len(self.all_fixtures)) + ' matches ')
        filtered_fixtures = [
            fixture for fixture in self.all_fixtures if fixture['league_name'] in datas.authorized_leagues
        ]
        print("Trying to update progressive data for " + str(len(filtered_fixtures)) + ' matches ')
        for fixture in filtered_fixtures:
            fixture_id = fixture['id']
            goals = common.extract_goals(fixture['events'], 'goal')
            fixture['goals'] = goals
            fixture['events'] = []
            fixture['dominance_index'] = []
            #update goals
            # Si league_name existe, on l'ajoute au set
            #self.league_names.add(league_name)
            # if (len(fixture['dominance_index']) > 0):
            #     self.j = self.j + 1
            # else:
            #     self.k = self.k + 1
            #     key = {"id": fixture['id']}
            #     print(fixture['league_name'], fixture['home_team'], fixture['away_team'])
            #     mongo_table_matches.delete_one(key)
            # key = {"id": fixture['id']}
            # mongo_table_matches.delete_one(key)
            self.j = self.j + 1
            key = {"id": fixture_id}
            x = mongo_table_matches.update_one(key, {"$set": fixture}, upsert=True)
            # key = {"id": fixture['id']}
            # mongo_table_matches.delete_one(key)

