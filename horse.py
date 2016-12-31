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

	def findHorses(number=None,gate_position=None,date=None,track=None,race_number=None,name=None,jockey=None
				,age=None,odds=None,position_splits=None,gender=None):
		find_dict = {}
		for k,v in locals().items():
			if v is None:continue
			print(v)
		pass