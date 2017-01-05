import logging
import pdb
import numpy as np
import pandas as pd

class Stats(object):
	"""docstring for Stats"""
	def __init__(self, name='', bets_played=0, starting_bank=0, races_bet=None, payout_stats=None):
		super(Stats, self).__init__()
		self.bets_played = bets_played
		self.bank=starting_bank
		self.name=name
		if races_bet is None:
			self.races_bet=[]
		if payout_stats is None:
			self.payout_stats=[]

	def getStats(self):
		payout_data=pd.Series(self.payout_stats)
		#payout_data=self.payout_stats
		return(payout_data.describe())

	def appendBet(self,bet_info):
		self.bets_played+=1
		if bet_info[2]:
			self.bank+=(bet_info[1]-bet_info[0])
			self.payout_stats.append(bet_info[1]-bet_info[0])
		else:
			self.bank-=bet_info[0]
			self.payout_stats.append(bet_info[0])
		return

	def printStats(self):
		stats = self.getStats()
		logging.info('Name: {}\nFinal bank: {}\n{}'.format(self.name, round(self.bank,3), stats))
#		print('Name: {}\nFinal bank: {}\n{}'.format(self.name, round(self.bank,3), stats))
		return