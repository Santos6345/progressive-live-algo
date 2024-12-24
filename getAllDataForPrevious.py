from modules import _getAllDataForPrevious
import datetime


print(str(datetime.datetime.now()) + '  STARTING PROCESS : getting all games from sofascore')
_getAllDataForPrevious.AllFixtures()
print(str(datetime.datetime.now()) + '  ENDING PROCESS')