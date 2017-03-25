#!/home/cori/anaconda3/bin/python
from pymongo import MongoClient
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import re
import pdb
import logging
from logging.config import dictConfig

from race import Race
from stats import Stats
from bet_strategy import bets
from utilities import hook
from utilities import lineno
import utilities
import env_config

SCRIPT_NAME    = 'test_bets.py'
SCRIPT_VERSION = '1.0'

#------------------------------------------------------------------------------
def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d','--date',      dest='date',      default=r'[0-9]+')
  parser.add_argument('-t','--track',     dest='track',     default=r'^[a-z]+')
  parser.add_argument('-r','--race',      dest='race',      default=None)
  parser.add_argument('-v','--verbosity', dest='verbosity', default='OFF')
  args = parser.parse_args()
  utilities.set_verbosity(args.verbosity)
  return args

#------------------------------------------------------------------------------
def plot_bet(bet_list, DIFF, bet_name):
  hook(SCRIPT_NAME, "INFO", "MEDIUM", lineno(), "Running plot_bet(bet_list, DIFF, {})".format(bet_name)) 
  df = pd.DataFrame(np.array(bet_list), index=np.array(DIFF)).T
  plt.plot(df)
  plt.ylabel("Bank Value ($1)")
  plt.xlabel("Races")
  plt.title(bet_name)
  plt.legend(np.array(DIFF),loc='lower left')
  plt.show()
  return

#------------------------------------------------------------------------------
def build_testing_list(track, date):
  hook(SCRIPT_NAME, "INFO", "MEDIUM", lineno(), "Running build_testing_list({}, {})".format(track, date))
  testing_list = []
  track_lower = track.lower()
  track_upper = track.upper()
  for f in glob('./data/*'):
    hook(SCRIPT_NAME, "INFO", "HIGH", lineno(), "Checking csv file: {}".format(f))
    csv_name = f.split('/')[-1]
    if not re.search(date, csv_name) or not re.match(track_lower, csv_name):
      continue
    found_date  = re.search(date, csv_name).group()
    found_track = re.match(track_lower, csv_name).group().upper()
    hook(SCRIPT_NAME, "INFO", "MEDIUM", lineno(), "Appending file to testing list: {}".format(f))
    testing_list.append((found_date, found_track))
  return testing_list

#------------------------------------------------------------------------------
def main():
  args = get_args()
  hook(SCRIPT_NAME, "INFO", "LOW", lineno(), "Running version: {}".format(SCRIPT_VERSION))
  DIFF=[1,1.25,1.5,1.75,2,2.25,2.5]
  testing_list = build_testing_list(args.track, args.date)
  
  stata_list = []
  all_test_list=[]
  first=[1,2,3,4]
  second=[1,2,3,4]
  for diff in DIFF:
    statb = Stats(starting_bank=400)
    bank=[400]
    for day in testing_list:
      races = Race.findRaces(date=day[0],track=day[1], race_number=args.race)
      if not races:
        hook(SCRIPT_NAME, "ERROR", "XXX", lineno(), 'Could not find races: {} {}'.format(day[0], day[1]))
      for race in races:
        race_outcome = bets.exacta_box(race, statb, first, second, diff)
        bank.append(bank[-1] + race_outcome)
    all_test_list.append(bank)

  plot_bet(all_test_list, DIFF, 'Exacta: {} over {}'.format(first,second))
  # statb.printStats()

#------------------------------------------------------------------------------
if __name__ == '__main__':
  main()