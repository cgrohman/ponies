from glob import glob
import csv
from pymongo import MongoClient
import pdb

from utilities import hook
from utilities import lineno
import utilities

def remove_trailing_blanks(row):
  while(row[-1] == ''):
    row = row[:-1]
  return row

def main():
  utilities.set_verbosity('HIGH')
  client = MongoClient()
  db = client.PONIES
  db = db.HORSES

  files = glob('data/*.csv')
  for f in files:
    with open(f) as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      for row in reader:
        if row[0] != 'H': continue
        date  = row[2].strip()
        track = row[1].strip()
        rn    = row[3].strip()
        name  = row[7].strip()
        if db.find_one({'date':date, 'track':track, 'race_number':rn, 'name':name}) is None:
          hook('add_wps.py', "WARNING", "XXX", lineno(), "Unable to find horse: Date:{} Track: {} RN: {} Name: {}".format(row[2], row[1], row[3], row[7])) 
          continue
        row = remove_trailing_blanks(row)
        weight = row[8]
        claim_value = row[16]
        hook('add_wps.py', "INFO", "HIGH", lineno(), "Updating: Date:{} Track: {} RN: {} Name: {} Weight: {} Claim Value: {}".format(row[2], row[1], row[3], row[7], weight, claim_value))
        db.update_one({'date':date, 'track':track, 'race_number':rn, 'name':name},{'$set': {'weight':weight, 'claim_value':claim_value}})


if __name__ == '__main__':
  main()