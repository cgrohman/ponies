from pymongo import MongoClient
from race import Race
from horse import HorseInstance
from glob import glob



def main():
	count=0
	DIFF=1
	dates = []
	for f in glob('./data/bel*'):
		csv_name = f.split('/')[2]
		dates.append(csv_name[3:11])
	tracks = ['BEL']
	bank = Bank(400)
	for date in dates:
		for track in tracks:
			races = Race.findRaces(date=date,track=track)
			if not races: 
				print('Could not find races')
#			count+=one_two_overall(races,bank)
			count+=two_three_overall(races,bank,DIFF)
	print('Final bank: {}\nRaces bet: {}'.format(bank.amount,count))


def one_two_overall(races,bank,DIFF=1):
	count=0
	for race in races:
		exacta_payout = float(race.exacta['payout'])
		exacta_bet= int(race.exacta['bet_amount'])
		horses = race.sortedHorseOdds()
		cost_of_bet = (len(horses)-1)*2*exacta_bet

		if float(horses[1].odds)*DIFF <= float(horses[2].odds):
			bank.amount-=cost_of_bet
			count+=1
			if (horses[0].finish_position['position'] == '1' or horses[1].finish_position['position'] == '1'):
				#This means the bet made 
				bank.amount+=exacta_payout
				print('Date: {} Track: {} Race: {} Net: {}\nOdds: {}, {}, {}'.format(race.date, race.track, race.race_number,
																			 exacta_payout-cost_of_bet,horses[0].odds,horses[1].odds,horses[2].odds))
			else:
				print('LOST - Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
	return(count)

def two_three_overall(races,bank,DIFF=1):
	count=0
	for race in races:
		exacta_payout = float(race.exacta['payout'])
		exacta_bet= int(race.exacta['bet_amount'])
		horses = race.sortedHorseOdds()
		cost_of_bet = (len(horses)-1)*2*exacta_bet

		if float(horses[2].odds)*DIFF <= float(horses[1].odds):
			bank.amount-=cost_of_bet
			count+=1
			if (horses[1].finish_position['position'] == '1' or horses[2].finish_position['position'] == '1'):
				#This means the bet made 
				bank.amount+=exacta_payout
				print('Date: {} Track: {} Race: {} Net: {}\nOdds: {}, {}, {}'.format(race.date, race.track, race.race_number,
																			 exacta_payout-cost_of_bet,horses[0].odds,horses[1].odds,horses[2].odds))
			else:
				print('LOST - Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
	return(count)

class Bank(object):
	"""docstring for Bank"""
	def __init__(self, start_amount):
		super(Bank, self).__init__()
		self.amount = start_amount

	def calculateReturn(start, finish):
		return((finish-start)/start)
		

		


if __name__ == '__main__':
	main()