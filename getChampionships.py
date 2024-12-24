from modules import _getChampionships
import datetime


print(str(datetime.datetime.now()) + '  STARTING PROCESS : getting all games from sofascore')
_getChampionships.AllFixtures()
print(str(datetime.datetime.now()) + '  ENDING PROCESS')