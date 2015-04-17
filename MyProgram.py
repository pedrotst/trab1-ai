import statistics
import math

class bayesstats():
	mean_yes = None
	mean_no = None
	dev_yes = None
	dev_no = None
	def __init__(self, mean_yes, mean_no, dev_yes, dev_no):
		self.mean_yes = mean_yes
		self.mean_no = mean_no
		self.dev_yes = dev_yes
		self.dev_no = dev_no

	def __str__(self):
		stats = "Mean yes: " + str(self.mean_yes)
		stats += ', Standard deviation yes: ' + str(self.dev_yes)
		stats += ', Mean no: ' + str(self.mean_no)
		stats += ', Standard deviation no: ' + str(self.dev_no)
		return stats

	def __repr__(self):
		return self.__str__()

def folding(training_set, fold_num):
	training_set_folded = []
	test_folded = []
	for i in range(len(training_set)):
		if i % 10 == fold_num:
			test_folded.append(training_set[i])
		else:
			training_set_folded.append(training_set[i])
	return test_folded, training_set_folded

def mean_dev(training_set):
	class_yes = []
	class_no = []
	mean_yes = {}
	mean_no = {}
	dev_yes = {}
	dev_no = {}
	for key in training_set[0]:
		for i in range(len(training_set)):
			if training_set[i]['DiabetesClass'] == 'yes':
				class_yes.append(training_set[i][key])
			else:
				class_no.append(training_set[i][key])
		if not key == 'DiabetesClass':
			mean_yes[key] = statistics.mean(class_yes)
			mean_no[key] = statistics.mean(class_no)
			dev_yes[key] = statistics.stdev(class_yes)
			dev_no[key] = statistics.stdev(class_no)
		else:
			prob_yes = float(len(class_yes) / len(training_set))
			prob_no = float(len(class_no) / len(training_set))
		class_yes = []
		class_no = []
	return mean_yes, mean_no, dev_yes, dev_no, prob_yes, prob_no

def naive_bayes_training(training_set):
    trained_values = {}
    mean_yes, mean_no, dev_yes, dev_no, prob_yes, prob_no = mean_dev(training_set)
    for key in training_set[0]:
    	if not key == 'DiabetesClass':
    		trained_values[key] = bayesstats(float(mean_yes[key]), float(mean_no[key]), float(dev_yes[key]), float(dev_no[key]))
    	else:
    		trained_values[key] = {'prob_yes': prob_yes, 'prob_no': prob_no}
    return trained_values

def prob_density(new_value, mean, dev):
	chunk_1 = (new_value - mean) ** 2
	chunk_2 = 2 * ((dev) ** 2)
	chunk_3 = - (chunk_1 / chunk_2)
	chunk_4 = math.exp(chunk_3)
	chunk_5 = dev * ((2 * math.pi) ** 0.5)
	chunk_6 = 1 / chunk_5
	chunk_7 = chunk_6 * chunk_4
	return chunk_7

def naive_bayes_testing(test, trained_values):
	prob_yes = 1
	prob_no = 1
	for key in trained_values:
		if not key == 'DiabetesClass':
			prob_yes *= prob_density(test[key], trained_values[key].mean_yes, trained_values[key].dev_yes)
			prob_no *= prob_density(test[key], trained_values[key].mean_no, trained_values[key].dev_no)
		else:
			prob_yes *= trained_values[key]['prob_yes']
			prob_no *= trained_values[key]['prob_no']
	if prob_yes >= prob_no:
		return 'yes'
	else:
		return 'no'


f_training = open('pima.csv','r')#later use user given address
training_set = []
i = 0
for line in f_training:
    line = line.split(',')
    training_set.append({})
    training_set[i]['TimesPregnant'] = float(line[0])
    training_set[i]['GlucoseConcentration'] = float(line[1])
    training_set[i]['DiastolicPressure'] = float(line[2])
    training_set[i]['SkinThickness'] = float(line[3])
    training_set[i]['SerumInsulin'] = float(line[4])
    training_set[i]['MassIndex'] = float(line[5])
    training_set[i]['PedigreeFunction'] = float(line[6])
    training_set[i]['Age'] = float(line[7])
    training_set[i]['DiabetesClass'] = line[8].rstrip('\n')
    i+=1

training_set = sorted(training_set, key = lambda k: k['DiabetesClass'])
test_folded, training_set_folded = folding(training_set, 0)
trained_values = naive_bayes_training(training_set_folded)

# raw_test = '0.058824,0.316129,0.469388,0.26087,0.169471,0.249489,0.101196,0.033333'
# raw_test = raw_test.split(',')
# test = {}
# test['TimesPregnant'] = float(raw_test[0])
# test['GlucoseConcentration'] = float(raw_test[1])
# test['DiastolicPressure'] = float(raw_test[2])
# test['SkinThickness'] = float(raw_test[3])
# test['SerumInsulin'] = float(raw_test[4])
# test['MassIndex'] = float(raw_test[5])
# test['PedigreeFunction'] = float(raw_test[6])
# test['Age'] = float(raw_test[7])
for i in range(len(test_folded)):
	print(naive_bayes_testing(test_folded[i], trained_values))