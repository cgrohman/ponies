from datetime import datetime
import csv
import pdb

from race import Race
from horse import Horse
import utilities

date = '20150429'
track = 'BEL'
utilities.set_verbosity('HIGH')
# client = MongoClient()
# db = client.PONIES
# rdb = db.RACES
# hdb = db.HORSES

filename = 'results/ml_{}.csv'.format(datetime.now().strftime('%Y-%m-%d'))
with open(filename,'w') as f:
  races = Race.findRaces(track=track, date=date)
  for race in races:
    ordered_horses = race.sortedHorseOdds()
    race_text = '{},{},{},{},{},{},{},{},{},{},{},{},{},'.format(race.track, race.date, 
                               race.race_number, race.card_type, race.race_type, race.purse,
                               race.horse_age_req[:2], race.distance, race.dist_unit, race.surface,
                               race.class_rating, race.track_condition, race.weather)
    for horse in ordered_horses:
      row = race_text + '{},{},{},{},{},{},'.format(horse.weight, horse.age, horse.gender, horse.odds, 
                                  horse.gate_position, horse.claim_value)
      if horse.finish_position['position'] in ['1','2','3']:
        finish_wps = '1'
      else:
        finish_wps = '0'
      for h in ordered_horses:
        if h == horse:
          row += 'NaN,NaN,NaN,NaN,NaN,NaN,'
        else:
          row += '{},{},{},{},{},{},'.format(h.odds, h.age, h.gender, h.weight, 
                                  h.gate_position, h.claim_value)
      row += finish_wps+'\n'
      f.write(row)
  