import statistics
import math
#math.exp(x)
class bayesstats():
	mean_yes = None
	mean_no = None
	dev_yes = None
	dev_no = None
	def __init__(self, mean_yes, mean_no, dev_yes, dev_no):
		self.mean_yes = mean_yes
		self.mean_n = mean_no
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
	# print(mean_yes, dev_yes, prob_yes, mean_no, dev_no, prob_no)

def naive_bayes_training(training_set):
    trained_values = {}
    mean_yes, mean_no, dev_yes, dev_no, prob_yes, prob_no = mean_dev(training_set)
    for key in training_set[0]:
    	if not key == 'DiabetesClass':
    		trained_values[key] = bayesstats(mean_yes[key], mean_no[key], dev_yes[key], dev_no[key])
    	else:
    		trained_values[key] = {'prob_yes': prob_yes, 'prob_no': prob_no}
    return trained_values

def naive_bayes_testing(test):


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
    # print(training_set[i])
    i+=1
# TrainedValues = naive_bayes_training(training_set)
trined_values = naive_bayes_training(training_set)
