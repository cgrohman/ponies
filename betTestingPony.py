from pymongo import MongoClient
from race import Race
from stats import Stats
from bet_strategy import bets
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
        bets.one_two_overall(races, statc, DIFF)
        bets.two_three_overall(races, statd, DIFF)

    statc.printStats()
    statd.printStats()
    

if __name__ == '__main__':
    main()