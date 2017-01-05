import numpy as np 
from horse import HorseInstance
from race import Race
from sklearn.neural_network import MLPClassifier
from pprint import pprint

dates = ['20150819', '20150812', '20150815', '20150724', '20150806', '20150814', '20151101', '20151107', '20151119', '20150816', '20150828', '20151105', '20150822', '20150805', '20150716', '20150722', '20151113', '20150719', '20150905', '20150729', '20151108', '20151127', '20151114', '20151031', '20151122', '20150903', '20150902', '20151128', '20151120', '20150718', '20150830', '20150907', '20150904', '20151112', '20151126', '20150723', '20150801', '20150808', '20150827', '20150802', '20150826', '20150906', '20151030', '20151115', '20150725', '20151121', '20150820', '20150717', '20151029', '20150821', '20150726', '20150807', '20150829', '20150813', '20150809', '20151106', '20150730', '20150731', '20150823']
test = ['20151129']
horses = []
for date in dates:
	horses.extend(HorseInstance.findHorses(track='DMR',date=date))

X=[]
Y=[]
for h in horses:
	X.append([int(h.age), int(h.gate_position)/10, float(h.jockey['weight'])/10, float(h.odds)])
	Y.append(int(h.finish_position['position']))

clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
clf.fit(X, Y)
print(clf.predict([[2,11/10,122/10,2.2]]))