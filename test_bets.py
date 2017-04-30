#!/home/cori/anaconda3/bin/python
from pymongo import MongoClient
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import re
import pdb
import datetime

from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

from race import Race
from stats import Stats
from bet_strategy import bets
from utilities import hook
from utilities import lineno
import utilities

SCRIPT_NAME    = 'test_bets.py'
SCRIPT_VERSION = '1.0'

#------------------------------------------------------------------------------
def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d','--date',      action='store',      dest='date',      default=r'[0-9]+')
  parser.add_argument('-t','--track',     action='store',      dest='track',     default=r'^[a-z]+')
  parser.add_argument('-r','--race',      action='store',      dest='race',      default=None)
  parser.add_argument('-v','--verbosity', action='store',      dest='verbosity', default='OFF')
  parser.add_argument('-s','--save',      action='store_true')
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
  plt.grid()
  plt.show()
  return

#------------------------------------------------------------------------------
def save_to_csv(bet_list, DIFF, csv_path):
  hook(SCRIPT_NAME, "INFO", "MEDIUM", lineno(), "Running save_bet_to_csv(bet_list, DIFF, {})".format(csv_path)) 
  df = pd.DataFrame(np.array(bet_list), index=np.array(DIFF)).T
  df.to_csv(csv_path)
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
  start_time = datetime.datetime.now()
  args = get_args()
  hook(SCRIPT_NAME, "INFO", "LOW", lineno(), "Running version: {}".format(SCRIPT_VERSION))
  testing_list = build_testing_list(args.track, args.date)

  # Bet info
  DIFF      = [1,2,4,7,10]
  #DIFF      = [1]
  purse_min = 000
  first     = [1]
  second    = [1]
  third     = [1]
  fourth    = 'All'
  horse     = 6
  finish    = 'SHOW'
  bet_name  = 'GaussianNB: Prob > 0.8, Odds > 2.0'
  csv_path  = './results/{}/nb_prob0.8_odds2.0_{}.csv'.format('ml', args.date)
  #csv_path = './results/{}/exacta_{}_{}_{}.csv'.format('ALL',first, second, args.date)

  stata_list = []
  all_test_list=[]

  clf_obj,x,sc_dict = get_svc_clf()
  for diff in DIFF:
    statb = Stats(starting_bank=400)
    bank=[1000]
    for day in testing_list:
      races = Race.findRaces(date=day[0],track=day[1], race_number=args.race)
      if not races:
        hook(SCRIPT_NAME, "ERROR", "XXX", lineno(), 'Could not find races: {} {}'.format(day[0], day[1]))
      for race in races:
        #race_outcome = bets.exacta(race, statb, bet_name, first, second, diff)
        #race_outcome = bets.trifecta(race, statb, bet_name, first, second, third, diff, purse_min)
        race_outcome = bets.clf_wps(race, statb, bet_name, clf_obj, x, sc_dict, 0.8, diff, purse_min)
        bank.append(bank[-1] + race_outcome)
    all_test_list.append(bank)

  
  if args.save:
    save_to_csv(all_test_list, DIFF, csv_path)
  hook(SCRIPT_NAME, "INFO", "LOW", lineno(), "Execution time: {}".format(str(datetime.datetime.now() - start_time)))
  plot_bet(all_test_list, DIFF, bet_name)
  # statb.printStats()

#------------------------------------------------------------------------------
def get_nb_clf():

  df = pd.read_csv('results/singleHorse_2017-04-21.csv')

  x = df.iloc[:,:-1]
  y = df.iloc[:,-1]

  columns = list(x.columns)

  sc_dict = sc_fit(x,columns)

  for col in columns:
    x = scale_col(x, col, sc_dict)

  #x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
  
  clf = GaussianNB()
  nb_filter = SelectKBest(f_regression, k=5)
  nb_pipe = Pipeline([('anova',nb_filter), ('nb',clf)])
  nb_pipe.fit(x,y)
  score = nb_pipe.score(x,y)  
  return nb_pipe,x,sc_dict

#------------------------------------------------------------------------------
def get_svc_clf():

  df = pd.read_csv('results/singleHorse_2017-04-21.csv')

  x = df.iloc[:,:-1]
  y = df.iloc[:,-1]

  columns = list(x.columns)

  sc_dict = sc_fit(x,columns)

  for col in columns:
    x = scale_col(x, col, sc_dict)

  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
  
  clf = SVC(probability=True)
  svc_filter = SelectKBest(f_regression, k=5)
  svc_pipe = Pipeline([('anova',svc_filter), ('svc',clf)])
  svc_pipe.fit(x_train, y_train)
  scores = cross_val_score(svc_pipe, x, y, cv=5)
  obj = {'clf':svc_pipe,'type':'SVC'}
  hook(SCRIPT_NAME, "INFO", "LOW", lineno(), "SVC score: {0:.3f}".format(scores.mean()))
  return obj,x,sc_dict

#------------------------------------------------------------------------------
def sc_fit(df, labels):
  sc_dict = {}
  for label in labels:
    sc = StandardScaler()
    col = np.array(df[label]).T
    sc.fit(col.reshape(-1,1))
    sc_dict[label] = sc
  return sc_dict

#------------------------------------------------------------------------------
def scale_col(df, label, sc_dict):
  col = np.array(df[label]).T
  try:
    df[label] = sc_dict[label].transform(col.reshape(-1,1))
  except:
    pdb.set_trace()
  return df



#------------------------------------------------------------------------------
if __name__ == '__main__':
  main()
