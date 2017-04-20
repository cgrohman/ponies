from glob import glob
import csv
from pymongo import MongoClient
import pdb

from utilities import hook
from utilities import lineno
import utilities

SCRIPT_NAME = 'update_race_data.py'

def remove_trailing_blanks(row):
  while(row[-1] == ''):
    row = row[:-1]
  return row

def main():
  utilities.set_verbosity('HIGH')
  client = MongoClient()
  db = client.PONIES
  db = db.RACES

  files = glob('data/*.csv')
  for f in files:
    with open(f) as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      for row in reader:
        if row[0] != 'R': continue
        date  = row[3].strip()
        track = row[2].strip()
        rn    = row[4].strip()
        if db.find_one({'date':date, 'track':track, 'race_number':rn}) is None:
          hook(SCRIPT_NAME, "WARNING", "XXX", lineno(), "Unable to find horse: Date:{} Track: {} RN: {}".format(date, track, rn)) 
          continue
        #row = remove_trailing_blanks(row)
        distance  = row[13]
        dist_unit = row[14]
        if dist_unit != 'Y':
          continue

        distance_f = float(distance)/220

        hook(SCRIPT_NAME, "INFO", "HIGH", lineno(), "Updating: Date:{} Track: {} RN: {}".format(date, track, rn))
        db.update_one({'date':date, 'track':track, 'race_number':rn},
          {'$set': {'distance':distance_f, 'dist_unit':'F'}})


if __name__ == '__main__':
  main()