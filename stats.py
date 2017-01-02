
class Stats(object):
	"""docstring for Stats"""
	def __init__(self, name='', bets_played=0, starting_bank=0, races_bet=None, races_won=None):
		super(Stats, self).__init__()
		self.bets_played = bets_played
		self.bank=starting_bank
		self.name=name
		if races_bet is None:
			self.races_bet=[]
		if races_won is None:
			self.races_won=[]

	def getStats(self):
		pass

	def printStats(self):
		print('Name: {}\nFinal bank: {} Races bet: {}'.format(self.name, round(self.bank,3), self.bets_played))
		return