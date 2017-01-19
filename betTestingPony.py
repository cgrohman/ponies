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
import argparse

dictConfig(env_config.logging_config)
logger = logging.getLogger()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-date', dest='date', default=r'[0-9]+')
    parser.add_argument('-track', dest='track', default=r'^[a-z]+')
    parser.add_argument('-race', dest='race', default=None)
    args = parser.parse_args()
    
    DIFF=[1,1.25,1.5, 1.75,2,2.25,2.5]
    testing_list = []
    for f in glob('./data/*'):
        csv_name = f.split('/')[2]
        if not re.search(args.date, csv_name) or not re.match(args.track,csv_name): continue
        date = re.search(args.date, csv_name).group()
        track = re.match(args.track,csv_name).group()
        testing_list.append((date,track.upper()))
 

    stata_list = []
    statb_list = []
    for diff in DIFF:
        stata = Stats(starting_bank=400)
        statb = Stats(starting_bank=400)
        for day in testing_list:
            races = Race.findRaces(date=day[0],track=day[1], race_number=args.race)
            if not races:
                logger.error('Could not find races: {} {}'.format(day[0], day[1]))
            
            bets.exacta(races, stata, [1,2], 'All', diff)
            bets.exacta(races, statb, [2,3], 'All', diff)
        stata_list.append(stata)
        statb_list.append(stata)

    stata.printStats()
    statb.printStats()
    

if __name__ == '__main__':
    main()