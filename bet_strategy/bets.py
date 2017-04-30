from stats import Stats
from race import Race
from horse import Horse

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

import sys
import pdb
import itertools

from utilities import hook
from utilities import lineno
import utilities

SCRIPT_NAME = 'bets.py'
SCRIPT_VERSION = '1.0'

BREAKAGE   = 1   # 1 = one digit after period (rounds down to nearest tenth)
MIN_PAYOUT = 0.4 # $2.40 is the minimum payout

#------------------------------------------------------------------------------
def one_two_overall(races,stat,DIFF=1):
  '''
  exactas: 1/2, All
  DEPRICATED - use exactas()
  '''
  stat.name = "One/Two Overall"
  for race in races:
    logger.info('Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
    exacta_payout = float(race.exacta['payout'])
    exacta_bet= int(race.exacta['bet_amount'])
    horses = race.sortedHorseOdds()
    if not horses:
      logger.warning('No odds for any horses- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
      continue

      if one_two_overall_conditions(horses,DIFF):
        cost_of_bet = (len(horses)-1)*2*exacta_bet
        WON=False
        if (horses[0].finish_position['position'] == '1' or horses[1].finish_position['position'] == '1'):
          WON=True
          stat.races_bet.append((race,WON))
          logger.debug('WON- Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number,exacta_payout-cost_of_bet))
        else:
          stat.races_bet.append((race,WON))
          logger.warning('LOST- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
          stat.appendBet([cost_of_bet, exacta_payout, WON])
          return()

#------------------------------------------------------------------------------
def one_two_overall_conditions(horses, DIFF):
  flag = False
  if float(horses[1].odds)*DIFF <= float(horses[2].odds):
    flag = True
    return(flag)

#------------------------------------------------------------------------------
def two_three_overall(races,stat,DIFF=1):
  '''
  Exactas: 2/3, All
  DEPRICATED - use exactas()
  '''
  stat.name = "Two/Three Overall"
  for race in races:
    exacta_payout = float(race.exacta['payout'])
    exacta_bet= int(race.exacta['bet_amount'])
    horses = race.sortedHorseOdds()
    if not horses:
      logger.warning('No odds for any horses- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
      continue
    elif len(horses)<4:
      logger.warning('Not enough horses for this bet- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
      continue

      if float(horses[2].odds)*DIFF <= float(horses[3].odds):
        cost_of_bet = (len(horses)-1)*2*exacta_bet
        WON=False
        if (horses[1].finish_position['position'] == '1' or horses[2].finish_position['position'] == '1'):
          WON=True
          stat.races_bet.append((race,WON))
          logger.debug('WON - Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number,exacta_payout-cost_of_bet))
        else:
          logger.warning('LOST- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
          stat.appendBet([cost_of_bet, exacta_payout, WON])
          return()        

#------------------------------------------------------------------------------
def exacta(race, stat, bet_name, first, second='All', DIFF=1):
  '''
  Exactas ex; first = [1,2] second='All'
  '''
  stat.name = bet_name
  exacta_payout = float(race.exacta['payout'])
  exacta_bet= int(race.exacta['bet_amount'])
  ordered_horses_odds = race.sortedHorseOdds()
  if not ordered_horses_odds:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'No odds for any horses- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)
  elif len(ordered_horses_odds)<4:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'Not enough horses for this bet- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)

  first_horse_list, first   = build_horse_list(first,  ordered_horses_odds)
  second_horse_list, second = build_horse_list(second, ordered_horses_odds)

  outcome=0
  if float(ordered_horses_odds[max(first + second)-1].odds)*DIFF <= float(ordered_horses_odds[max(first + second)].odds):
    cost_of_bet = calculate_bet_cost([first_horse_list, second_horse_list], exacta_bet, True)
    outcome-=cost_of_bet
    WON=False

    first_flag  = did_horse_hit(first_horse_list,  '1')
    second_flag = did_horse_hit(second_horse_list, '2')
    
    if first_flag and second_flag:
      WON=True
      outcome += exacta_payout
      hook(SCRIPT_NAME, "INFO", "LOW", lineno(), 'WON - Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number,exacta_payout-cost_of_bet)) 
    else:
      hook(SCRIPT_NAME, "INFO", "MEDIUM", lineno(), 'LOST- Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number, -cost_of_bet)) 
    stat.races_bet.append((race, WON))
    stat.appendBet([cost_of_bet, exacta_payout, WON])
  return(outcome)

#------------------------------------------------------------------------------
def exacta_box(race, stat, first, second='All', DIFF=1):
  '''
  Exactas ex; first = [1,2] second='All'
  '''
  stat.name = 'Exacta: {} over {}'.format(first, second)
  exacta_payout = float(race.exacta['payout'])
  exacta_bet    = int(race.exacta['bet_amount'])
  ordered_horses_odds = race.sortedHorseOdds()
  if not ordered_horses_odds:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'No odds for any horses- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)
  if len(ordered_horses_odds)<5:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'Not enough horses for this bet- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)

  first_horse_list = []
  for i in first:
    first_horse_list.append(ordered_horses_odds[i-1])
  
  outcome = 0
  if float(ordered_horses_odds[max(first)-1].odds)*DIFF <= float(ordered_horses_odds[max(first)].odds):
    cost_of_bet = len(first)*(len(first)-1)*exacta_bet
    calc = calculate_bet_cost([first_horse_list, first_horse_list], exacta_bet, True)
    if cost_of_bet != calc:
      hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'Bet costs are not equal: {} calced: {}'.format(cost_of_bet, calc)) 
    outcome -= cost_of_bet
    WON = False
    first_flag,second_flag = False,False
    for h in first_horse_list:
      if h.finish_position['position'] == '1':
        first_flag = True
      elif h.finish_position['position'] == '2':
        second_flag = True
    if first_flag and second_flag:
      WON = True
      outcome += exacta_payout
      hook(SCRIPT_NAME, "INFO", "LOW", lineno(), 'WON- Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number,exacta_payout-cost_of_bet))
    else:
      hook(SCRIPT_NAME, "INFO", "MEDIUM", lineno(), 'LOST- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    stat.races_bet.append((race,WON))
    stat.appendBet([cost_of_bet, exacta_payout, WON])
  return(outcome)

#------------------------------------------------------------------------------
def trifecta(race, stat, bet_name, first, second='All', third='All', DIFF=1, purse_min=0):
  '''
  Trifectas ex; first = [1,2,3] second = [1,2,3] third = [1,2,3]
  '''
  stat.name = bet_name
  try:
    trifecta_payout = float(race.trifecta['payout'])
    trifecta_bet    = float(race.trifecta['bet_amount'])
  except:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'Race did not contain trifecta data- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)
  ordered_horses_odds = race.sortedHorseOdds()
  if not ordered_horses_odds:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'No odds for any horses- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)
  if len(ordered_horses_odds)<5:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'Not enough horses for this bet- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)

  # List of horses based on odds
  first_horse_list, first   = build_horse_list(first,  ordered_horses_odds)
  second_horse_list, second = build_horse_list(second, ordered_horses_odds)
  third_horse_list, third   = build_horse_list(third,  ordered_horses_odds)
  
  outcome = 0
  all_positions = first + second + third
  if float(ordered_horses_odds[max(all_positions)-1].odds)*DIFF <= float(ordered_horses_odds[max(all_positions)].odds) and float(race.trifecta['pool']) >= purse_min:
    hook(SCRIPT_NAME, "INFO", "HIGH", lineno(), 'Position/odds: {}/{} {}/{}'.format(max(all_positions), ordered_horses_odds[max(all_positions)].odds, max(all_positions)+1, ordered_horses_odds[max(all_positions)+1].odds))
    cost_of_bet = calculate_bet_cost([first_horse_list, second_horse_list, third_horse_list], trifecta_bet, True)
    outcome -= cost_of_bet
    WON = False
    
    first_flag  = did_horse_hit(first_horse_list,  '1')
    second_flag = did_horse_hit(second_horse_list, '2')
    third_flag  = did_horse_hit(third_horse_list,  '3')
    
    if first_flag and second_flag and third_flag:
      WON = True
      outcome += trifecta_payout
      hook(SCRIPT_NAME, "INFO", "LOW", lineno(), 'WON - Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number, trifecta_payout-cost_of_bet))
    else:
      hook(SCRIPT_NAME, "INFO", "MEDIUM", lineno(), 'LOST- Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number, -cost_of_bet)) 
    stat.races_bet.append((race,WON))
    stat.appendBet([cost_of_bet, trifecta_payout, WON])
  return(outcome)

#------------------------------------------------------------------------------
def superfecta(race, stat, bet_name, first, second='All', third='All', fourth='All', DIFF=1, purse_min = 0):
  '''
  Trifectas ex; first = [1,2,3] second = [1,2,3] third = [1,2,3]
  '''
  stat.name = bet_name
  try:
    superfecta_payout = float(race.superfecta['payout'])
    superfecta_bet    = float(race.superfecta['bet_amount'])
  except:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'Race did not contain superfecta data- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)
  if superfecta_bet == 0:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'Race did not contain superfecta data- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)

  ordered_horses_odds = race.sortedHorseOdds()
  if not ordered_horses_odds:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'No odds for any horses- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)
  if len(ordered_horses_odds)<6:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'Not enough horses for this bet- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)

  # List of horses based on odds
  first_horse_list, first   = build_horse_list(first,  ordered_horses_odds)
  second_horse_list, second = build_horse_list(second, ordered_horses_odds)
  third_horse_list, third   = build_horse_list(third,  ordered_horses_odds)
  fourth_horse_list, fourth = build_horse_list(fourth,  ordered_horses_odds)
  
  outcome = 0
  all_positions = first + second + third + fourth
  if float(ordered_horses_odds[max(all_positions)-1].odds)*DIFF <= float(ordered_horses_odds[max(all_positions)].odds):
    hook(SCRIPT_NAME, "INFO", "HIGH", lineno(), 'Position/odds: {}/{} {}/{}'.format(max(all_positions), ordered_horses_odds[max(all_positions)-1].odds, max(all_positions)+1, ordered_horses_odds[max(all_positions)].odds))
    cost_of_bet = calculate_bet_cost([first_horse_list, second_horse_list, third_horse_list, fourth_horse_list], superfecta_bet, True)
    outcome -= cost_of_bet
    WON = False
    
    first_flag  = did_horse_hit(first_horse_list,  '1')
    second_flag = did_horse_hit(second_horse_list, '2')
    third_flag  = did_horse_hit(third_horse_list,  '3')
    fourth_flag = did_horse_hit(fourth_horse_list, '4')
    
    if first_flag and second_flag and third_flag and fourth_flag:
      WON = True
      outcome += superfecta_payout
      hook(SCRIPT_NAME, "INFO", "LOW", lineno(), 'WON - Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number, superfecta_payout-cost_of_bet))
    else:
      hook(SCRIPT_NAME, "INFO", "MEDIUM", lineno(), 'LOST- Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number, -cost_of_bet)) 
    stat.races_bet.append((race,WON))
    stat.appendBet([cost_of_bet, superfecta_payout, WON])
  return(outcome)

#------------------------------------------------------------------------------
def straight(race, stat, bet_name, horse_num, finish_wps, DIFF=1, purse_min = 0):
  """
  horse: is the odds ordered horse ('1' = horse with best odds to win)
  finish: list of positions that 'horse' can finish in
  """
  if finish_wps not in ['WIN', 'PLACE', 'SHOW']:
    hook(SCRIPT_NAME, "FATAL", "XXX", lineno(), "Finish input incorrect, expected ['WIN', 'PLACE', 'SHOW'], got:{} ".format(finish_wps))
    sys.exit()

  stat.name = bet_name
  ordered_horses_odds = race.sortedHorseOdds()
  if not ordered_horses_odds:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'No odds for any horses- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)
  if len(ordered_horses_odds)<horse_num+1:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'Not enough horses for this bet- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)

  outcome = 0
  horse = ordered_horses_odds[horse_num - 1]
  if float(horse.odds)*DIFF <= float(ordered_horses_odds[horse_num].odds):
    hook(SCRIPT_NAME, "INFO", "HIGH", lineno(), 'Position/odds: {}/{}'.format(horse_num, horse.odds))
    finish = []
    payout = 0
    if finish_wps == 'WIN':
      finish = [1]
      payout = float(horse.wps[0])
    elif finish_wps == 'PLACE':
      finish = [1, 2]
      payout = float(horse.wps[1])
    elif finish_wps == 'SHOW':
      finish = [1, 2, 3]
      payout = float(horse.wps[2])
    
    if payout-2 < MIN_PAYOUT:
      payout = MIN_PAYOUT + 2
    
    cost_of_bet = 2
    outcome -= cost_of_bet
    WON = False

    for f in finish:
      if did_horse_hit([horse], str(f)):
        WON = True
        outcome += payout
        hook(SCRIPT_NAME, "INFO", "LOW", lineno(), 'WON - Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number, payout-cost_of_bet))
    if not WON:
      hook(SCRIPT_NAME, "INFO", "LOW", lineno(), 'LOST- Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number, -cost_of_bet))

    stat.races_bet.append((race,WON))
    stat.appendBet([cost_of_bet, payout, WON])
  return(outcome)

#------------------------------------------------------------------------------
def clf_wps(race, stat, bet_name, clf_obj, x, sc_dict, min_prob=0.8, DIFF=1, purse_min = 0):
  stat.name = bet_name
  low_to_high_odds = race.sortedHorseOdds()[::-1]
  outcome = 0
  labels = ['race_number', 'purse', 'distance', 'class_rating', 'num_in_field', 'h_odds', 'h_age', 'h_weight', 'h_gate_position', 'h_claim_value', 'h_odds_index']

  horse = None
  for i,horse in enumerate(low_to_high_odds):
    h_index = len(low_to_high_odds)-1-i
    new = pd.DataFrame([[race.race_number, race.purse, race.distance, race.class_rating, len(low_to_high_odds), horse.odds, horse.age, horse.weight, horse.gate_position, horse.claim_value, h_index]])
    new.columns = labels
    for col in labels:
      new = scale_col(new, col, sc_dict)
    
    clf = clf_obj['clf']
    pred = clf.predict(new)
    probs = clf.predict_proba(new)
    if probs[0][1] > .8 and float(horse.odds)>DIFF:
      hook(SCRIPT_NAME, "INFO", "HIGH", lineno(), 'Prob/odds: {0:.2f}/{1}'.format(probs[0][1], horse.odds))
      cost_of_bet = 2
      outcome -= cost_of_bet
      WON = False
      
      #SHOW
      finish = [1, 2, 3]
      payout = float(horse.wps[2])
      if payout-2 < MIN_PAYOUT:
        payout = MIN_PAYOUT + 2

      for f in finish:
        if did_horse_hit([horse], str(f)):
          WON = True
          outcome += payout
          hook(SCRIPT_NAME, "INFO", "LOW", lineno(), 'WON - Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number, payout-cost_of_bet))
      if not WON:
        hook(SCRIPT_NAME, "INFO", "LOW", lineno(), 'LOST- Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number, -cost_of_bet))
      
      stat.races_bet.append((race,WON))
      stat.appendBet([cost_of_bet, payout, WON])
  return(outcome)


#------------------------------------------------------------------------------
def get_clf():

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
  obj = {''}  
  return nb_pipe,x,sc_dict

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
def odds_to_horses(abs_place, ordered_horses, **params):
  horse_list = []
  exclude_list = []
  if params:
    for k,v in params.items():
      exclude_list += v
    exclude_list = set(exclude_list)
  
  if abs_place != 'All':
    for i in range(1, len(ordered_horses)):
      if i in exclude_list:
        continue
      horse_list.append(ordered_horses[i-1])
  else:
    for i in abs_place:
      horse_list.append(ordered_horses[i-1])
  return horse_list

#------------------------------------------------------------------------------
def build_horse_list(abs_place, ordered_horses):
  horse_list = []
  pos_list   = []
  if abs_place == 'All':
    horse_list = ordered_horses
    pos_list = [0]
  else:
    for i in abs_place:
      horse_list.append(ordered_horses[i-1])
    pos_list = abs_place
  return horse_list, pos_list

#------------------------------------------------------------------------------
def did_horse_hit(horses, position):
  for h in horses:
      if h.finish_position['position'] == position:
        return True
  return False

#------------------------------------------------------------------------------
def calculate_bet_cost(legs, amount, unique):
  num_bets = 0
  if unique:
    num_bets = len([ tuple(ea) for ea in itertools.product(*legs) if len(ea) == len(set(ea)) ])
  else:
    num_bets = len([ tuple(ea) for ea in itertools.product(*legs) ])
  return num_bets*amount
