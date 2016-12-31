from pymongo import MongoClient
from race import Race
from horse import HorseInstance

def main():

	race = Race.findRaces(date="20151129",track='DMR')
	if race:
		for r in race:
			print(r.horses[0].name)
'''
	horses = HorseInstance.findHorses(date="20151129",race_number="5",track='DMR')
	if horses:
		for horse in horses:
			print(horse.name)
	else:
		print("Could not find horses")
'''
	

if __name__ == '__main__':
	main()