from pymongo import MongoClient
from horse import Horse
import pandas as pd
import numpy as np
import pprint
import logging

class Race():
	def __init__(self, track, date, race_type, race_number, description,
				horse_age_req, distance, start_time, time_splits, finish_time, purse, weather,
				card_type, breed, dist_unit, track_condition, class_rating, surface,
				exacta=None, trifecta=None, superfecta=None, quinella=None, pick_3=None,
				pick_4=None, pick_5=None, daily_double=None, consolation_pick=None):
		self.track = track 						# C
		self.date = date						# D
		self.race_type = race_type					# G
		self.race_number = race_number			# E
		self.description=description		# IJKl
		self.horse_age_req=horse_age_req		# M
		self.distance=distance					# N
		self.start_time=start_time				# V
		self.time_splits=time_splits			# XYZ,AA,AB
		self.finish_time=finish_time			# AC
		self.purse=purse						# AH?
		self.exacta=exacta						# tuple (payout,pool) Start at AT
		self.trifecta=trifecta 	
		self.superfecta=superfecta
		self.quinella=quinella
		self.pick_3=pick_3
		self.pick_4=pick_4
		self.pick_5=pick_5
		self.daily_double=daily_double
		self.consolation_pick=consolation_pick
		self.weather=weather
		self.card_type=card_type
		self.breed=breed
		self.track_condition=track_condition
		self.class_rating=class_rating
		self.surface=surface
		self.dist_unit=dist_unit
		self.horses = Horse.findHorses(track=track, date=date, race_number=race_number)

	@staticmethod
	def findRaces(track=None,date=None,race_type=None,race_number=None,
				horse_age_req=None,distance=None,start_time=None,time_splits=None,
				finish_time=None,purse=None,exacta=None,trifecta=None,superfecta=None,
				quinella=None,pick_3=None,pick_4=None,pick_5=None,daily_double=None,
				consolation_pick=None,weather=None):
		query = {}
		for k,v in locals().items():
			if v is None or k == 'query':continue
			query[k]=v
		try:
			client = MongoClient()
			db = client["PONIES"]
			col = db.RACES
		except:
			col = None
		if col is None: return([])
		races = col.find(query)
		client.close()
		races_list=[]
		for r in races:
			temp_race= Race(track=r['track'], date=r['date'], race_number=r['race_number'],
				race_type=r['race_type'], horse_age_req=r['horse_age_req'], distance=r['distance'],
				start_time=r['start_time'], time_splits=r['time_splits'], finish_time=r['finish_time'],
				purse=r['purse'], weather=r['weather'], exacta=r['exacta'], trifecta=r['trifecta'], 
				superfecta=r['superfecta'], quinella=r['quinella'], pick_3=r['pick_3'], pick_4=r['pick_4'],
				pick_5=r['pick_5'], daily_double=r['daily_double'], consolation_pick=r['consolation_pick'],
				description=r['description'], card_type=r['card_type'], breed=r['breed'], dist_unit=r['dist_unit'],
				track_condition=r['track_condition'], class_rating=r['class_rating'], surface=r['surface'])
			races_list.append(temp_race)
		return(races_list)

	def sortedHorseOdds(self):
		horses_list = sorted(self.horses, key=lambda x:float(x.odds))
		horses_list_clean=[]
		for h in horses_list:
			if float(h.odds) == 0:continue				
			horses_list_clean.append(h)
		return(horses_list_clean)

	def toDict(self):
		horses_list=[]
		for h in self.horses:
			horses_list.append(h.__dict__)
		self.horses = horses_list
		return(self.__dict__)

	def _col2num(col):
	    num = 0
	    for c in col:
	        if c in string.ascii_letters:
	            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
	    return num-1