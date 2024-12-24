from modules import _analyseWinningAlgo
from datetime import datetime as timer
import schedule
import time as tme
import datetime
import sys

print(str(datetime.datetime.now()) + '  STARTING PROCESS : getting all games from sofascore')
_analyseWinningAlgo.AllFixtures()
print(str(datetime.datetime.now()) + '  ENDING PROCESS')
