import statistics
import math

class bayesstats():
	'''
	Class to store the mean and standard deviation from classes yes and no
	'''
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
	'''
	Separates the data set in a ten fold matter using a counter to know which fold is to be used as testing set (from 0 to 9)
	'''
	training_set_folded = []
	test_folded = []
	for i in range(len(training_set)):
		if i % 10 == fold_num:
			test_folded.append(training_set[i])
		else:
			training_set_folded.append(training_set[i])
	return test_folded, training_set_folded

def mean_dev(training_set):
	'''
	Calculates and returns the mean and standard deviation to the classes yes and no of a given training set
	'''
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
	'''
	Returns a dictionary with the bayesstats for each atribute of a given training set, also the probability of the classes yes and no
	'''
	trained_values = {}
	mean_yes, mean_no, dev_yes, dev_no, prob_yes, prob_no = mean_dev(training_set)
	for key in training_set[0]:
		if not key == 'DiabetesClass':
			trained_values[key] = bayesstats(float(mean_yes[key]), float(mean_no[key]), float(dev_yes[key]), float(dev_no[key]))
		else:
			trained_values[key] = {'prob_yes': prob_yes, 'prob_no': prob_no}
	return trained_values

def prob_density(new_value, mean, dev):
	'''
	Returns the value of a probability density of a given class given a specific argument
	'''
	chunk_1 = (new_value - mean) ** 2
	chunk_2 = 2 * ((dev) ** 2)
	chunk_3 = - (chunk_1 / chunk_2)
	chunk_4 = math.exp(chunk_3)
	chunk_5 = dev * ((2 * math.pi) ** 0.5)
	chunk_6 = 1 / chunk_5
	chunk_7 = chunk_6 * chunk_4
	return chunk_7

def naive_bayes_testing(test, trained_values):
	'''
	Returns the class for a given test argument considering the trained values (means and standard deviations) 
	'''
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

def euclidian_distance(training_set, test):
	'''
	Returns a list of dictionaries with the values for the euclidian distance and class of each training argument
	'''
	distances = []
	for i in range(len(training_set)):
		distances.append({})
		distances[i]['Distance'] = 0
		for key in training_set[i]:
			if not key == 'DiabetesClass':
				distances[i]['Distance'] += (test[key] - training_set[i][key]) ** 2
			else:
				distances[i]['DiabetesClass'] = training_set[i]['DiabetesClass']
		distances[i]['Distance'] = distances[i]['Distance'] ** 0.5
	return distances


def knn(k, training_set, test):
	'''
	Returns the class for a given test argument considering euclidian distances of the training arguments 
	'''
	distances = euclidian_distance(training_set, test)
	distances = sorted(distances, key = lambda k: k['Distance'])
	# print(distances)
	if distances[k-2]['Distance'] == distances[k-1]['Distance'] or distances[k-1]['Distance'] == distances[k]['Distance']:
		if distances[k-2]['DiabetesClass'] != distances[k-1]['DiabetesClass'] or distances[k-1]['DiabetesClass'] != distances[k]['DiabetesClass']:
			return 'yes'
	return distances[k - 1]['DiabetesClass']

def dict_decode(data_row):
	timepreg = '{},'.format(data_row['TimesPregnant'])
	age = '{},'.format(data_row['Age'])
	mass_ind = '{},'.format(data_row['MassIndex'])
	insulin = '{},'.format(data_row['SerumInsulin'])
	pedigree = '{},'.format(data_row['PedigreeFunction'])
	diabetes = '{}\n'.format(data_row['DiabetesClass'])
	glucose = '{},'.format(data_row['GlucoseConcentration'])
	diastolic ='{},'.format(data_row['DiastolicPressure'])
	skinthickness = '{},'.format(data_row['SkinThickness'])
	return 	timepreg+glucose+diastolic+skinthickness+insulin+mass_ind+pedigree+age+diabetes

def create_folds_file():
	with open('pima-folds.csv', 'w') as arq:
		if arq:
			for i in range(10):
				arq.write("Fold {}\n".format(i))
				print("\nFold {}".format(i))
				for j in training_set[i::10]:
					print(j)
					arq.write(dict_decode(j))
			arq.close()
		else:
			print("Couldn't open file, program exiting")

def build_set_from(file_string):
	organized_list = []
	for line in file_string:
	    line = line.split(',')
	    dict_aux = {}
	    dict_aux['TimesPregnant'] = float(line[0])
	    dict_aux['GlucoseConcentration'] = float(line[1])
	    dict_aux['DiastolicPressure'] = float(line[2])
	    dict_aux['SkinThickness'] = float(line[3])
	    dict_aux['SerumInsulin'] = float(line[4])
	    dict_aux['MassIndex'] = float(line[5])
	    dict_aux['PedigreeFunction'] = float(line[6])
	    dict_aux['Age'] = float(line[7])
	    dict_aux['DiabetesClass'] = line[8].rstrip('\n')
	    organized_list.append(dict_aux)
	return organized_list


if __name__ == '__main__':
		
	# f_training = open('pima.csv','r')#later use user given address
	# training_set = build_set_from(f_training)
	# print(training_set)

	# training_set = sorted(training_set, key = lambda k: k['DiabetesClass'])
	# test_folded, training_set_folded = folding(training_set, 0)
	# create_folds_file()

	folds_file = open('pima-folds.csv', 'w')
	folds_aux = []
	folds_dict = {}
	i = 1
	# print(''.join(list(folds_file)).split('\n'))
	lines = ''.join(list(folds_file)).split('\n')[1::]
	for line in lines:
		# print(line, i)
		if not line == 'Fold {}'.format(i):
			folds_aux.append(line)
		else:
			folds_dict[i] = build_set_from((folds_aux))
			folds_aux = []
			i += 1
	# print(folds_dict[9])
	accuracy_list = []
	for key in folds_dict:
		to_train = []
		for key_ in folds_dict:
			if not key == key_:
				to_train = to_train + folds_dict[key]
		# print(len(to_train))
		trained_values = naive_bayes_training(to_train)
		test_set = folds_dict[key]
		count = 0
		for i in range(len(test_set)):
			# print("Running Baes at fold #", i)
			test = naive_bayes_testing(test_set[i], trained_values)
			# print(test, test_set[i]['DiabetesClass'])
			if test == test_set[i]['DiabetesClass']:
				count += 1
		print("Fold {} Accuracy: {}".format(key, count/len(test_set)))
		accuracy_list.append(count/len(test_set))
	print("Final accuracy:", statistics.mean(accuracy_list))

		# print(trained_value)
	# trained_values = naive_bayes_training(training_set_folded)

	# countNB = 0
	# countKNN = 0

	# print('NB')
	# for i in range(len(test_folded)):
	# 	aux = naive_bayes_testing(test_folded[i], trained_values)
	# 	print(aux, test_folded[i]['DiabetesClass'])
	# 	if aux == test_folded[i]['DiabetesClass']:
	# 		countNB += 1
	# print(countNB/len(test_folded))
	# print('KNN')
	# for i in range(len(test_folded)):
	# 	aux = knn(1, training_set_folded, test_folded[i])
	# 	# print(aux, test_folded[i]['DiabetesClass'])
	# 	if aux == test_folded[i]['DiabetesClass']:
	# 		countKNN += 1
	# print(countKNN/len(test_folded))