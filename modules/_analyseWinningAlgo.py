from datetime import datetime, timedelta
from tqdm import tqdm
import json
import time
import re
import pymongo
from modules.tools import *
import json
from modules.config import datas
from modules import common

import sys

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


class AllFixtures:

    ######################################### CONSTRUCTOR ##########################################
    def __init__(self, webdriver_name='firefox', driver=None):
        year = str(sys.argv[1])
        start_date = year + '-04-01'
        end_date = year + '-08-30'

        self.isProd = False

        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        self.all_profit = 0
        self.totalKO = 0
        self.totalKOPicks = 0
        self.totalOK = 0
        self.totalOKPicks = 0
        self.total = 0
        self.totalPicks = 0
        self.totalProfitPicks = 0
        self.percentageWin = 0
        self.percentageWinPicks = 0
        self.lostMax = 0
        self.lostMaximum = 0
        self.picks = []
        current_date = start
        self.start_date_string = start.strftime('%Y-%m-%d')
        self.end_date_string = end.strftime('%Y-%m-%d')
        self.all_fixtures = list(
            mongo_table_matches.find({"date": {"$gte": self.start_date_string, "$lte": self.end_date_string}, "progressive_data": {"$exists": True}}).sort(
                {'dateTime': 1}))
        self.analyseWinning()

        print(self.all_profit)
        self.percentageWin = float("{:.2f}".format(self.totalOK / self.total))
        print('total :' + str(self.total) + ', total KO: ' + str(self.totalKO) + ', total OK: ' + str(
            self.totalOK) + ', pourcentage win:' + str(self.percentageWin))
        print('max lost ' + str(self.lostMaximum))



    def diff_dates(self, date1, date2):
        return abs(datetime.strptime(date2, '%Y-%m-%d') - datetime.strptime(date1, '%Y-%m-%d')).days

    def analyseWinning(self):
        j = 0
        k = 0
        print("Trying to analyse " + str(len(self.all_fixtures)) + ' matches ')
        for fixture in self.all_fixtures:
            #             try:
            id = fixture['id']
            date = fixture['date']
            dateTime = fixture['dateTime']
            league_name = fixture['league_name']
            home_team = fixture['home_team']
            away_team = fixture['away_team']
            progressive_data = fixture['progressive_data']

            profit = 0
            result = ''
            match_data = {
                "id": id,
                "home_team": home_team,
                "away_team": away_team,
                "dateTime": dateTime,
                "date": date,
                "league_name": league_name,
                "progressive_data": progressive_data,
                "goals": fixture['goals']
            }
            #print(match_data)
            if league_name in datas.authorized_leagues and league_name not in datas.excluded_from_stats:
                match_data["elapsed"] = 25

                #########1ST half
                # retourPickLive = common.PickOverFirstHalf(match_data, self.picks, self.all_profit, self.totalOK, self.totalKO, self.total, self.lostMax, self.lostMaximum, self.isProd)
                # self.all_profit = retourPickLive["all_profit"]
                # self.totalOK = retourPickLive["totalOK"]
                # self.totalKO = retourPickLive["totalKO"]
                # self.total = retourPickLive["total"]
                # self.lostMax = retourPickLive["lostMax"]
                # self.lostMaximum = retourPickLive["lostMaximum"]


                ######2ND half
                # match_data["elapsed"] = 70
                # retourPickLive = common.PickOverSecondHalf(match_data, self.picks, self.all_profit, self.totalOK, self.totalKO, self.total, self.lostMax, self.lostMaximum, self.isProd)
                # self.all_profit = retourPickLive["all_profit"]
                # self.totalOK = retourPickLive["totalOK"]
                # self.totalKO = retourPickLive["totalKO"]
                # self.total = retourPickLive["total"]
                # self.lostMax = retourPickLive["lostMax"]
                # self.lostMaximum = retourPickLive["lostMaximum"]

                match_data["elapsed"] = 70
                retourPickLive = common.PickOverSecondHalfTest(match_data, self.picks, self.all_profit, self.totalOK, self.totalKO, self.total, self.lostMax, self.lostMaximum, self.isProd)
                self.all_profit = retourPickLive["all_profit"]
                self.totalOK = retourPickLive["totalOK"]
                self.totalKO = retourPickLive["totalKO"]
                self.total = retourPickLive["total"]
                self.lostMax = retourPickLive["lostMax"]
                self.lostMaximum = retourPickLive["lostMaximum"]




