from pymongo import MongoClient
from race import Race
from horse import HorseInstance
from stats import Stats
from glob import glob



def main():
	DIFF=1
	dates = []
	for f in glob('./data/bel*'):
		csv_name = f.split('/')[2]
		dates.append(csv_name[3:11])
	tracks = ['BEL']
	statc = Stats(starting_bank=400)
	statd = Stats(starting_bank=400)
	for date in dates:
		for track in tracks:
			races = Race.findRaces(date=date,track=track)
			if not races: 
				print('Could not find races')
			one_two_overall(races, statc, DIFF)
			two_three_overall(races, statd, DIFF)
	statc.printStats()
	statd.printStats()
	

def one_two_overall(races,stat,DIFF=1):
	stat.name = "One/Two Overall"
	for race in races:
		exacta_payout = float(race.exacta['payout'])
		exacta_bet= int(race.exacta['bet_amount'])
		horses = race.sortedHorseOdds()
		cost_of_bet = (len(horses)-1)*2*exacta_bet

		if float(horses[1].odds)*DIFF <= float(horses[2].odds):
			stat.bank-=cost_of_bet
			stat.bets_played+=1
			stat.races_bet.append(race)
			if (horses[0].finish_position['position'] == '1' or horses[1].finish_position['position'] == '1'):
				#This means the bet was won 
				stat.bank+=exacta_payout
				stat.races_won.append(race)
#				print('Date: {} Track: {} Race: {} Net: {}\nOdds: {}, {}, {}'.format(race.date, race.track, race.race_number,
																			 exacta_payout-cost_of_bet,horses[0].odds,horses[1].odds,horses[2].odds))
			else:
				print('LOST - Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
	return()

def two_three_overall(races,stat,DIFF=1):
	stat.name = "Two/Three Overall"
	for race in races:
		exacta_payout = float(race.exacta['payout'])
		exacta_bet= int(race.exacta['bet_amount'])
		horses = race.sortedHorseOdds()
		cost_of_bet = (len(horses)-1)*2*exacta_bet

#		if float(horses[2].odds)*DIFF <= float(horses[1].odds):
		stat.bank-=cost_of_bet
		stat.bets_played+=1
		stat.races_bet.append(race)
		if (horses[1].finish_position['position'] == '1' or horses[2].finish_position['position'] == '1'):
			#This means the bet made 
			stat.bank+=exacta_payout
			stat.races_won.append(race)
#			print('Date: {} Track: {} Race: {} Net: {}\nOdds: {}, {}, {}'.format(race.date, race.track, race.race_number,
																		 exacta_payout-cost_of_bet,horses[0].odds,horses[1].odds,horses[2].odds))
		else:
#			print('LOST - Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
	return()		


if __name__ == '__main__':
	main()