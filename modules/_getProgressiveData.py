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

        start_date = '2022-04-09'
        end_date = '2022-12-31'

        self.language = "en_US"
        self.headers = config_data['header']
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        self.start_date_string = start.strftime('%Y-%m-%d')
        self.end_date_string = end.strftime('%Y-%m-%d')
        self.all_fixtures = list(mongo_table_matches.find({"date": {"$gte": self.start_date_string, "$lte": self.end_date_string}, "league_name": {"$in": datas.authorized_leagues}}).sort({'dateTime': 1}))
        self.updateMatchesProgressive()

    def updateMatchesProgressive(self):
        j = 0
        print("Trying to update progressive data for " + str(len(self.all_fixtures)) + ' matches ')
        systemDate = ''
        filtered_fixtures = [
            fixture for fixture in self.all_fixtures if fixture['league_name'] in datas.authorized_leagues and fixture['league_name'] not in datas.excluded_from_stats
        ]
        print("Trying to update graphs for filtered " + str(len(filtered_fixtures)) + ' matches ')
        for fixture in filtered_fixtures:
            # try:
            fixture_id = fixture['id']
            date = fixture['date']
            if systemDate != str(date):
                systemDate = str(date)
                print(systemDate)

            self.queryString = {
                "i": str(fixture_id),
                "l": self.language
            }
            print(fixture_id, ';', fixture['home_team'], '-', fixture['away_team'])
            #print('hasDominance')
            print('call graphs api')
            progressive_data_response = common.getJsonResponse(self.url_progressive, self.headers, self.queryString)
            progressive_data = progressive_data_response['result']
            builded_progressive_data = []
            for pd in progressive_data:
                time_float = str(common.getTime(str(pd['timer'])))
                builded_teamA = {}
                builded_teamB = {}
                dataTeamA = pd['teamA']
                dataTeamB = pd['teamB']

                #teamA
                builded_teamA['goal'] = dataTeamA['goal']
                builded_teamA['attacks'] = dataTeamA['attacks']
                builded_teamA['shoots'] = dataTeamA['shoots']
                builded_teamA['dominance'] = dataTeamA['dominance']
                try:
                    builded_teamA['xG'] = dataTeamA['xG']
                except:
                    builded_teamA['xG'] = -1

                #teamB
                builded_teamB['goal'] = dataTeamB['goal']
                builded_teamB['attacks'] = dataTeamB['attacks']
                builded_teamB['shoots'] = dataTeamB['shoots']
                builded_teamB['dominance'] = dataTeamB['dominance']
                try:
                    builded_teamB['xG'] = dataTeamB['xG']
                except:
                    builded_teamB['xG'] = -1
                dt = {"teamA": builded_teamA, "teamB": builded_teamB }

                builded_progressive_data.append({time_float: dt})

            #print(builded_progressive_data)
            fixture["progressive_data"] = builded_progressive_data
            key = {"id": fixture_id}
            x = mongo_table_matches.update_one(key, {"$set": fixture}, upsert=True)
            j = j + 1
            time.sleep(0.2)
        #                 except: pass
        print('updated ' + str(j) + ' matches')
