from pymongo import MongoClient

class Race():
	def __init__(self, track, date, race_type, race_number, race_description,
				horse_age_req, distance, start_time, time_splits, finish_time, horses, weather,
				exacta=None, trifecta=None, superfecta=None, quinella=None, pick_three=None,
				daily_double=None, consolation_pick=None):
		self.track = track 						# C
		self.date = date						# D
		self.race_type = race_type					# G
		self.race_number = race_number			# E
		self.description=race_description		# IJKL
		self.horse_age_req=horse_age_req		# M
		self.distance=distance					# N
		self.start_time=start_time				# V
		self.time_splits=time_splits			# XYZ,AA,AB
		self.finish_time=finish_time			# AC
		self.purse=purse						# AH?
		self.horses=horses						# AE horses list
		self.exacta=exacta						# tuple (payout,pool) Start at AT
		self.trifecta=trifecta 	
		self.superfecta=superfecta
		self.quinella=quinella
		self.pick_three=pick_three
		self.daily_double=daily_double
		self.consolation_pick=consolation_pick
		self.weather=weather

	def create_race(row):
		track = row[_col2num('C')]
		date = row[_col2num('D')]
		race_type=row[_col2num('G')]
		race_number= row[_col2num('E')]
		description= '{} {} {} {}'.format(row[_col2num('I')], row[_col2num('J')], row[_col2num('K')], row[_col2num('L')])
		horse_age_req= row[_col2num('M')]		
		distance= row[_col2num('N')]
		start_time= row[_col2num('V')]
		time_splits=[]
		for l in ['X','Y','Z','AA','AB']:
			time_splits.append(row[_col2num(l)])
		finish_time= row[_col2num('AC')]			# AC
		purse= row[_col2num('AH')]					# AH?
		
		horses = _getHorses(track, date, race_number)	# AE horses list
		weather= row[_col2num('C')]

		# Need to find these starting at row AT
		exacta=exacta		# t
		trifecta=trifecta	# Start at AT
		superfecta=superfecta
		quinella=quinella
		pick_three=pick_three
		daily_double=daily_double
		consolation_pick=consolation_pick
		
		return(Race())


	def _getHorses(track, date, race_number):
		horse = []
		return horses

	def _getExacta(row):
		return(exacta)


	def _col2num(col):
	    num = 0
	    for c in col:
	        if c in string.ascii_letters:
	            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
	    return num-1