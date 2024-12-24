from modules import _getProgressiveData
import datetime


print(str(datetime.datetime.now()) + '  STARTING PROCESS : getting all games from sofascore')
_getProgressiveData.AllFixtures()
print(str(datetime.datetime.now()) + '  ENDING PROCESS')