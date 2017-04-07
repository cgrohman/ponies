import numpy as np 
from horse import Horse
from race import Race
from pprint import pprint
from datetime import datetime
import re

#------------------------------------------------------------------------------
def main():
  h = Horse.findHorses(name='Chia Love')
  horse_to_csv(h)


#------------------------------------------------------------------------------
def horse_to_csv(horse_list):
  file_name = './data/horse_{}.csv'.format(datetime.now().strftime('%Y-%m-%d'))
  with open(file_name,'w') as f:
    for horse in horse_list:
      jockey_name   = ''
      jockey_weight = ''
      for k,v in horse.jockey.items():
        jockey_name   = re.sub(r'\s+',' ',k)
        jockey_weight = v
      text = '{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(horse.number, 
                            horse.gate_position, horse.date,
                            horse.track.strip(), horse.race_number, horse.name,
                            jockey_name, jockey_weight, horse.age, horse.odds, 
                            horse.gender, horse.finish_position['dist_behind'],
                            horse.finish_position['position'])
      f.write(text)
  return

#------------------------------------------------------------------------------
if __name__ == '__main__':
  main()