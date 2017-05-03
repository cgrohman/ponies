from datetime import datetime
import csv
import pdb

from race import Race
from horse import Horse
import utilities

MAX = 18


date = '20150429'
track = 'CD'
utilities.set_verbosity('HIGH')
# client = MongoClient()
# db = client.PONIES
# rdb = db.RACES
# hdb = db.HORSES

filename = 'results/singleHorse_{}.csv'.format(datetime.now().strftime('%Y-%m-%d'))
with open(filename,'w') as f:
  races = Race.findRaces()

  first_row = 'race_number,purse,distance,class_rating,num_in_field,h_odds,h_age,h_weight,h_gate_position,h_claim_value,h_odds_index,finish_wps\n'
  f.write(first_row)
  for race in races:
    if int(race.class_rating) <0: continue 
    ordered_horses = race.sortedHorseOdds()
    for i,horse in enumerate(ordered_horses):
      race_text = '{},{},{},{},{},'.format(race.race_number, race.purse, race.distance, race.class_rating, len(ordered_horses))
      row = race_text + '{},{},{},{},{},{},'.format(horse.odds, horse.age, horse.weight, horse.gate_position, horse.claim_value, i)
      if horse.finish_position['position'] in ['1','2','3']:
        finish_wps = '1'
      else:
        finish_wps = '0'
      horse_count = 0

      row += finish_wps+'\n'
      f.write(row)