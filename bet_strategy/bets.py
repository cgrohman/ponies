from stats import Stats
from race import Race
from horse import Horse
import pdb

from utilities import hook
from utilities import lineno

SCRIPT_NAME = 'bets.py'
SCRIPT_VERSION = '1.0'

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
          logger.debug('WON- Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number,exacta_payout-cost_of_bet))
        else:
          logger.warning('LOST- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
          stat.appendBet([cost_of_bet, exacta_payout, WON])
          return()        

#------------------------------------------------------------------------------
def exacta(race, stat, first, second='All', DIFF=1):
  '''
  Exactas ex; first = [1,2] second='All'
  '''
  stat.name = 'Exacta: {} over {}'.format(first,second)
  exacta_payout = float(race.exacta['payout'])
  exacta_bet= int(race.exacta['bet_amount'])
  ordered_horses_odds = race.sortedHorseOdds()
  if not ordered_horses_odds:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'No odds for any horses- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)
  elif len(ordered_horses_odds)<4:
    hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), 'Not enough horses for this bet- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
    return(0)

  first_horse_list = []
  for i in first:
    first_horse_list.append(ordered_horses_odds[i-1])
    second_horse_list = []
    if second != 'All':
      second_horse_list=second
    else:
      for i in ordered_horses_odds:
        if i in first_horse_list:
          continue
        second_horse_list.append(i)
  outcome=0
  if float(ordered_horses_odds[max(first)-1].odds)*DIFF <= float(ordered_horses_odds[max(first)].odds):
    cost_of_bet = (len(ordered_horses_odds)-1)*2*exacta_bet
    outcome-=cost_of_bet
    WON=False
    for h in first_horse_list:
      if h.finish_position['position'] == '1':
        WON=True
        stat.races_bet.append((race,WON))
        outcome+=exacta_payout
        hook(SCRIPT_NAME, "INFO", "LOW", lineno(), 'WON- Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number,exacta_payout-cost_of_bet)) 
    if not WON:
      hook(SCRIPT_NAME, "INFO", "MEDIUM", lineno(), 'LOST- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
      stat.appendBet([cost_of_bet, exacta_payout, WON])
  return(outcome)

#------------------------------------------------------------------------------
def exacta_box(race, stat, first, second='All', DIFF=1):
  '''
  Exactas ex; first = [1,2] second='All'
  '''
  stat.name = 'Exacta: {} over {}'.format(first, second)
  exacta_payout = float(race.exacta['payout'])
  exacta_bet= int(race.exacta['bet_amount'])
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
      stat.races_bet.append((race,WON))
      outcome += exacta_payout
      hook(SCRIPT_NAME, "INFO", "LOW", lineno(), 'WON- Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number,exacta_payout-cost_of_bet))
    else:
      hook(SCRIPT_NAME, "INFO", "MEDIUM", lineno(), 'LOST- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number)) 
      stat.appendBet([cost_of_bet, exacta_payout, WON])
  return(outcome)

##############################################################

##############################################################
# Exactas ex; first = [1,2] second='All'
##############################################################