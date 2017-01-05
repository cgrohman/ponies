from pymongo import MongoClient
from race import Race
from horse import HorseInstance
from stats import Stats
from glob import glob
import re
import pdb
import logging
from logging.config import dictConfig
import env_config

dictConfig(env_config.logging_config)
logger = logging.getLogger()

def main():
    DIFF=2.5
    testing_list = []
    for f in glob('./data/*'):
        csv_name = f.split('/')[2]
        date = re.search(r'[0-9]+', csv_name).group()
        track = re.match(r'[a-z]+[0-9]',csv_name).group()[:-1]
        testing_list.append((date,track.upper()))

    statc = Stats(starting_bank=400)
    statd = Stats(starting_bank=400)
    for day in testing_list:
        races = Race.findRaces(date=day[0],track=day[1])
        if not races:
            logger.error('Could not find races: {} {}'.format(day[0], day[1]))
        one_two_overall(races, statc, DIFF)
        two_three_overall(races, statd, DIFF)

    statc.printStats()
    statd.printStats()
    

def one_two_overall(races,stat,DIFF=1):
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

def one_two_overall_conditions(horses, DIFF):
    flag = False
    if float(horses[1].odds)*DIFF <= float(horses[2].odds):
        flag = True
    return(flag)

def two_three_overall(races,stat,DIFF=1):
    stat.name = "Two/Three Overall"
    for race in races:
        exacta_payout = float(race.exacta['payout'])
        exacta_bet= int(race.exacta['bet_amount'])
        horses = race.sortedHorseOdds()
        if not horses:
            logger.warning('No odds for any horses- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
            continue
        elif len(horses)<4:
            logger.warning('Not enough hourse for this bet- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
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


if __name__ == '__main__':
    main()