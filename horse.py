from pymongo import MongoClient

class HorseInstance():
	def __init__(self,number,gate_position,date,track,race_number,name,jockey,age,
				odds,position_splits,gender):
		self.number=number					# O
		self.gate_position=gate_position	# P
		self.date=date						# C
		self.track=track					# B
		self.race_number=race_number		# D
		self.name=name						# H
		self.jockey=jockey					# M I
		self.age=age						# J
		self.odds=odds						# N
		self.position_splits=position_splits # [{S:T},{U:V},{W:X},{Y:Z}]
		self.gender=gender					# K

	@staticmethod
	def findHorses(number=None,gate_position=None,date=None,track=None,race_number=None,name=None,jockey=None
				,age=None,odds=None,position_splits=None,gender=None):
		query = {}
		for k,v in locals().items():
			if v is None or k == 'query':continue
			query[k]=v
		try:
			client = MongoClient()
			db = client["PONIES"]
			col = db.HORSES
		except:
			col = None
		if col is None: return([])
		horses = col.find(query)
		client.close()

		horses_list=[]
		for h in horses:
			horses_list.append(HorseInstance(h['number'], h['gate_position'], h['date'], 
								h['track'], h['race_number'], h['name'], h['jockey'], 
								h['age'], h['odds'], h['position_splits'], h['gender']))
		return(horses_list)
