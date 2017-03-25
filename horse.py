from pymongo import MongoClient

class Horse():
	def __init__(self,number,gate_position,date,track,race_number,name,jockey,age,
				odds,position_splits,gender,finish_position):
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
		self.finish_position=finish_position

	@staticmethod
	def findHorses(number=None,gate_position=None,date=None,track=None,race_number=None,name=None,jockey=None
				,age=None,odds=None,position_splits=None,gender=None,finish_position=None):
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
			horses_list.append(Horse(number=h['number'], gate_position=h['gate_position'],
								date=h['date'], track=h['track'], race_number=h['race_number'], 
								name=h['name'], jockey=h['jockey'], age=h['age'], odds=h['odds'], 
								position_splits=h['position_splits'], gender=h['gender'],
								finish_position=h['finish_position']))
		return(horses_list)
