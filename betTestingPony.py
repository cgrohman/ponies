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
import env_config

def plot_bet(bet_list, DIFF, bet_name):
    df = pd.DataFrame(np.array(bet_list), index=np.array(DIFF)).T
    plt.plot(df)
    plt.ylabel("Bank Value ($1)")
    plt.xlabel("Races")
    plt.title(bet_name)
    plt.legend(np.array(DIFF),loc='lower left')
    plt.show()
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-date', dest='date', default=r'[0-9]+')
    parser.add_argument('-track', dest='track', default=r'^[a-z]+')
    parser.add_argument('-race', dest='race', default=None)
    args = parser.parse_args()

    dictConfig(env_config.logging_config)
    logger = logging.getLogger()
    
    DIFF=[1,1.25,1.5,1.75,2,2.25,2.5]
    testing_list = []
    for f in glob('./data/*'):
        csv_name = f.split('/')[2]
        if not re.search(args.date, csv_name) or not re.match(args.track,csv_name): continue
        date = re.search(args.date, csv_name).group()
        track = re.match(args.track,csv_name).group()
        testing_list.append((date,track.upper()))
 

    stata_list = []
    statb_list = []
    all_test_list=[]
    first=[1,2,3,4]
    second=[1,2,3,4]
    for diff in DIFF:
        stata = Stats(starting_bank=400)
        statb = Stats(starting_bank=400)
        bank=[400]
        for day in testing_list:
            races = Race.findRaces(date=day[0],track=day[1], race_number=args.race)
            if not races:
                logger.error('Could not find races: {} {}'.format(day[0], day[1]))
            for race in races:
 #               pay_outa.append(pay_outa[-1]+bets.exacta(race, stata, [1,2], 'All', diff))
 #               bank.append(bank[-1]+bets.exacta(race, statb, first, second, diff))
                bank.append(bank[-1]+bets.exacta_box(race, statb, first, second, diff))
        all_test_list.append(bank)
    
    plot_bet(all_test_list, DIFF, 'Exacta: {} over {}'.format(first,second))

 #   stata.printStats()
 #   statb.printStats()

   

if __name__ == '__main__':
    main()