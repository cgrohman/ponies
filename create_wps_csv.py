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

filename = 'results/ml_{}.csv'.format(datetime.now().strftime('%Y-%m-%d'))
with open(filename,'w') as f:
  races = Race.findRaces(track=track)

  first_row = 'track,date,race_number,card_type,race_type,purse,distance,dist_unit,surface,class_rating,track_condition,weather,breed,num_in_field'
  for i in range(MAX+1):
    first_row += ',h{}_odds,h{}_age,h{}_gender,h{}_weight,h{}_gate_position,h{}_claim_value'.format(i,i,i,i,i,i)
    if i == MAX:
      first_row += ',finish_wps\n'
  f.write(first_row)
  
  for race in races:
    ordered_horses = race.sortedHorseOdds()
    for horse in ordered_horses:
      race_text = '{},{},{},{},{},{},{},{},{},{},{},{},{},{},'.format(race.track,race.date, race.race_number, race.card_type, race.race_type, race.purse, race.distance, race.dist_unit, race.surface, race.class_rating, race.track_condition, race.weather, race.breed, len(ordered_horses))
      row = race_text + '{},{},{},{},{},{},'.format(horse.odds, horse.age, horse.gender, horse.weight, 
                                  horse.gate_position, horse.claim_value)
      if horse.finish_position['position'] in ['1','2','3']:
        finish_wps = '1'
      else:
        finish_wps = '0'
      horse_count = 0
      for h in ordered_horses:
        if h == horse:
          row += ',,,,,,'
        else:
          row += '{},{},{},{},{},{},'.format(h.odds, h.age, h.gender, h.weight, 
                                  h.gate_position, h.claim_value)
        horse_count += 1
      while(horse_count < MAX):
        row += ',,,,,,'
        horse_count+=1
      row += finish_wps+'\n'
      f.write(row)
  