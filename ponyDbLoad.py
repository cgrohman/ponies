#from race import Race
#from horse import HorseInstance
from glob import glob
import csv
from pymongo import MongoClient
import string

def main():
    pclient = MongoClient()
    pdb = pclient["PONIES"]
    rcol = pdb.RACES
    hcol = pdb.HORSES

    count = 0
    for f in glob("./data/*.csv"):
        with open(f, newline='') as csvfile:
            csvreader= csv.reader(csvfile, delimiter=',')
            for row in csvreader:
                checkExit(count)
                if row[0]=='H':
                    horse = {
                            'name':row[_col2num('H')],
                            "number":row[_col2num('O')],
                            "gate_position":row[_col2num('P')],
                            "date":row[_col2num('C')],
                            "track":row[_col2num('B')],
                            "race_number":row[_col2num('D')],
                            "jockey":{row[_col2num('M')]:row[_col2num('I')]},
                            "age":row[_col2num('J')],
                            "odds":row[_col2num('N')],
                            "position_splits":{row[_col2num('S')]:row[_col2num('T')],
                                               row[_col2num('U')]:row[_col2num('V')],
                                               row[_col2num('W')]:row[_col2num('X')],
                                               row[_col2num('Y')]:row[_col2num('Z')],
                                               },
                            "finish_position":{row[_col2num('AE')]:row[_col2num('AD')]},
                            "trainer":row[_col2num('AH')],
                            "stable":row[_col2num('AI')],
                            'gender':row[_col2num('K')]}
                    hcol.insert_one(horse)

                if row[0]=='R':
                    exacta_pay,exacta_pool,exacta_bet=_findData(["Exacta","Exactor"],row)
                    tri_pay,tri_pool,tri_bet=_findData(["Trifecta","Triactor"],row)
                    super_pay,super_pool,super_bet=_findData(["Superfecta","Superfector"],row)
                    quin_pay,quin_pool,quin_bet=_findData(["Quinella"],row)
                    cons_pay,cons_pool,cons_bet=_findData(["Consolation"],row)
                    dd_pay,dd_pool,dd_bet=_findData(["Daily Double"],row)
                    pick_3_pay,pick_3_pool,pick_3_bet=_findData(["Pick 3"],row)
                    pick_4_pay,pick_4_pool,pick_4_bet=_findData(["Pick 4"],row)
                    pick_5_pay,pick_5_pool,pick_5_bet=_findData(["Pick 5"],row)

                    race ={
                            "track":row[_col2num('C')].strip(),
                            'date':row[_col2num('D')].strip(),
                            'race_type':row[_col2num('G')].strip(),
                            'race_number':row[_col2num('E')].strip(),
                            'description':"{} {} {} {}".format(row[_col2num('I')].strip(),row[_col2num('J')].strip(),row[_col2num('K')].strip(),row[_col2num('L')].strip()),
                            'horse_age_req':row[_col2num('M')].strip(),
                            'distance':row[_col2num('N')].strip(),
                            'start_time':row[_col2num('V')].strip(),
                            'time_splits':[row[_col2num('X')].strip(),
                                            row[_col2num('Y')].strip(),
                                            row[_col2num('Z')].strip(),
                                            row[_col2num('AA')].strip(),
                                            row[_col2num('AB')].strip(),
                                            ],
                            'finish_time':row[_col2num('AC')],
                            'purse':row[_col2num('AH')],
                            'exacta':{'bet_amount':exacta_bet,'payout':exacta_pay,'pool':exacta_pool},
                            'trifecta':{'bet_amount':tri_bet,'payout':tri_pay,'pool':tri_pool},
                            'superfecta':{'bet_amount':super_bet,'payout':super_pay,'pool':super_pool},
                            'quinella':{'bet_amount':quin_bet,'payout':quin_pay,'pool':quin_pool},
                            'consolation_pick':{'bet_amount':cons_bet,'payout':cons_pay,'pool':cons_pool},
                            'daily_double':{'bet_amount':dd_bet,'payout':dd_pay,'pool':dd_pool},
                            'pick_3':{'bet_amount':pick_3_bet,'payout':pick_3_pay,'pool':pick_3_pool},
                            'pick_4':{'bet_amount':pick_4_bet,'payout':pick_4_pay,'pool':pick_4_pool},
                            'pick_5':{'bet_amount':pick_4_bet,'payout':pick_5_pay,'pool':pick_5_pool},
                            'weather':row[_col2num('T')],
                    }
                    rcol.insert_one(race)

            continue

def _findData(search,row):
    for c,i in enumerate(row):
        for s in search:
            if s in i:
                return(row[c+2],row[c+3],i.split()[0])
    print('WARNING: Unable to find -{} in row {}'.format(search,row))        
    return('0','0','0')


def _col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num-1

def checkExit(count):
    if count >5:exit()

if __name__ == '__main__':
    main()
