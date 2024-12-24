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
        self.url = "https://soccer-football-info.p.rapidapi.com/matches/day/full/"
        self.urlChampionShips = 'https://soccer-football-info.p.rapidapi.com/championships/list/'
        self.url_all_odds = 'https://footapi7.p.rapidapi.com/api/matches/odds/'
        self.event_url = 'https://footapi7.p.rapidapi.com/api/match/'

        year = str(sys.argv[1])
        #2022
        start_date = year + '-09-25'
        end_date = year + '-12-31'

        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        self.language = "en_US"
        self.headers = config_data['header']


        current_date = start
        self.list = []
        self.listID = []


        while current_date <= end:
            self.date_string = current_date.strftime('%Y%m%d')
            self.page_number = 1
            current_date += timedelta(days=1)
            builded_url = self.url

            #first call
            self.params = {
                "d": self.date_string,
                "p": str(self.page_number),
                "l": self.language
            }
            print(self.date_string)
            response_fixtures = common.getJsonResponse(builded_url, self.headers, self.params)

            #params
            try:
                pagination = response_fixtures['pagination']
                self.per_page = pagination['per_page']
                self.number_items = pagination['number_items']
                self.number_pages = int(self.number_items / self.per_page)
                self.page_number = pagination['page_number'] + 1
            except:
                self.page_number = 1
                self.number_pages = 1

            #traitement first page
            self.all_fixtures = response_fixtures['result']
            self.updateMatches()

            #call for every page
            if self.number_pages > 1:
                for pn in range(self.page_number, self.number_pages):
                    self.params = {
                        "d": self.date_string,
                        "p": str(pn),
                        "l": self.language
                    }
                    response_fixtures = common.getJsonResponse(builded_url, self.headers, self.params)
                    #traitement des autres pages
                    self.all_fixtures = response_fixtures['result']
                    self.updateMatches()

    def updateMatches(self):
        j = 0
        print("Trying to update ", len(self.all_fixtures), ' matches for date ', self.date_string, ', and page:', self.page_number, ', page numbers: ', self.number_pages)
        for fixture in self.all_fixtures:
            id = fixture['id']
            dateTime = fixture['date']
            datetime_obj = datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
            date_only = datetime_obj.date()
            championship = fixture['championship']
            status = fixture['status']
            teamA = fixture['teamA']
            teamB = fixture['teamB']
            scoreTeamA_final = teamA['score']['f']
            scoreTeamA_half = teamA['score']['1h']
            scoreTeamB_final = teamB['score']['f']
            scoreTeamB_half = teamB['score']['1h']
            home_team = teamA["name"]
            away_team = teamB["name"]
            league_name = championship['name']
            league_id = championship['id']

            try:
                odds = fixture['odds']
            except:
                continue

            try:
                events = fixture['events']
            except:
                continue

            #get goals from events
            if (status == 'ENDED') and len(events) > 0 and league_name in datas.authorized_leagues:
                #get goals from events
                goals = common.extract_goals(events)
                red_cards = common.extract_event(events, 'red_card')

                matchDate = {
                    "id": id,
                    "dateTime": dateTime,
                    "date": str(date_only),
                    "dateTime": str(dateTime),
                    "championship": championship,
                    "league_name": league_name,
                    "league_id": league_id,
                    "status": status,
                    "teamA": teamA,
                    "teamB": teamB,
                    "FT_score": str(scoreTeamA_final) + '-' + str(scoreTeamB_final),
                    "HT_score": str(scoreTeamA_half) + '-' + str(scoreTeamB_half),
                    "FT_goals_teamA": scoreTeamA_final,
                    "FT_goals_teamB": scoreTeamB_final,
                    "HT_goals_teamA": scoreTeamA_half,
                    "HT_goals_teamB": scoreTeamB_half,
                    "home_team": home_team,
                    "away_team": away_team,
                    "odds": odds,
                    "goals": goals,
                    "red_cards": red_cards
                }
                key = {"id": id}
                x = mongo_table_matches.update_one(key, {"$set": matchDate}, upsert=True)
                j = j + 1
        print('updated ' + str(j) + ' matches')

