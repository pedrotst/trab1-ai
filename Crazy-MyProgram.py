from __future__ import division
from __future__ import with_statement
import math
import sys
import re

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

def mean(data_list):
    return sum(data_list) / len(data_list)

def stdev(data_list):
    data_mean = mean(data_list)
    variance = sum([(x - data_mean) ** 2 for x in data_list]) / (len(data_list) - 1)
    return math.sqrt(variance)

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
            if training_set[i]['class'] == 'yes':
                class_yes.append(training_set[i][key])
            else:
                class_no.append(training_set[i][key])
        if not key == 'class':
            mean_yes[key] = mean(class_yes)
            mean_no[key] = mean(class_no)
            dev_yes[key] = stdev(class_yes)
            dev_no[key] = stdev(class_no)
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
        if not key == 'class':
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
        if not key == 'class':
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
    for i, train_ele in enumerate(training_set):
        distances.append({})
        distances[i]['Distance'] = 0
        for key in train_ele:
            if not key == 'class':
                distances[i]['Distance'] += (test[key] - train_ele[key]) ** 2
            else:
                distances[i]['class'] = train_ele['class']
        distances[i]['Distance'] = distances[i]['Distance'] ** 0.5
    return distances


def knn(k, training_set, test):
    '''
    Returns the class for a given test argument considering euclidian distances of the training arguments 
    '''
    distances = euclidian_distance(training_set, test)
    distances = sorted(distances, key = lambda l: l['Distance'])
    # print(distances)
    if k > 1:
        if distances[k-2]['Distance'] == distances[k-1]['Distance']:
            if distances[k-2]['class'] != distances[k-1]['class']:
                return 'yes'
    if distances[k-1]['Distance'] == distances[k]['Distance']:
        if distances[k-1]['class'] != distances[k]['class']:
            return 'yes'
    return distances[k - 1]['class']

def new_euclidian_distance(training_set, test):
    '''
    Returns a list of dictionaries with the values for the euclidian distance and class of each training argument
    '''
    distance = 1000
    aux = 0
    resp = ''
    for i, train_ele in enumerate(training_set):
        aux = 0
        for key in train_ele:
            if not key == 'class':
                aux += (test[key] - train_ele[key]) ** 2
        aux = aux ** 0.5
        if distance > aux:
            distance = aux
            resp = train_ele['class']
        if distance == aux:
            if resp != train_ele['class']:
                resp = 'yes'
    return resp

def dict_decode(data_row):
    str_aux = ''
    for data in data_row:
        str_aux += str(data_row[data])+','
    str_aux = str_aux.rstrip(',') + '\n'
    return  str_aux

def create_folds_file(training_set):
    with open('pima-folds.csv', 'w') as arq:
        if arq:
            for i in range(10):
                arq.write("Fold{}\n".format(i+1))
                for j in training_set[i::10]:
                    arq.write(dict_decode(j))
                arq.write("\n")
            arq.close()
        else:
            raise FileException("Couldn't open file, program exiting")

def build_set_from(input_set):
    '''Builds the file  as the number as keys
    :param: file name
    :return: list of dictionaries of the attributes with
      integers as keys, the last keynum i.e. the class key num
    '''
    is_file = False
    if (type(input_set) is not list) or (type(input_set) is not str):
        input_set = open(input_set, 'r')
        is_file = True
    organized_list = []
    for line in input_set:
        line = line.split(',')
        dict_aux = {}
        for i, attr in enumerate(line):
            attr = attr.strip()
            if attr == 'no' or attr == 'yes':
                dict_aux['class'] = attr
            else:
                dict_aux[i] = float(attr)
        if len(dict_aux.keys()) > 0:
            organized_list.append(dict_aux)
    if is_file:
        input_set.close()
    return organized_list

def build_folds_dict():
    with open('pima-folds.csv', 'r') as folds_file:
        if not folds_file:
            raise FileException("Could not open pima-folds, program exiting!")
        folds_aux = []
        folds_dict = {}
        i = 1
        lines = ''.join(list(folds_file)).split('\n')[1::]
        for line in lines:
            # print(line, i)
            if line == '':
                folds_dict[i] = build_set_from(folds_aux)
                folds_aux = []
                i += 1
            elif not line.startswith('Fold'):
                folds_aux.append(line)
        folds_file.close()
        del folds_dict[i-1]
    return folds_dict

def run_folded_bayes(train_set, test_set):
    nb_l = []
    trained_values = naive_bayes_training(train_set)
    for item in test_set:
        naive_class = naive_bayes_testing(item, trained_values)
        nb_l += [(naive_class)]
    return(nb_l)
    # print '\n'.join(nb_l)
    # for key in folds_dict:
    #     to_train = []
    #     for key_ in folds_dict:
    #         if not key == key_:
    #             to_train = to_train + folds_dict[key]
    #     # print(len(to_train))
    #     trained_values = naive_bayes_training(to_train)
    #     test_set = folds_dict[key]
    #     count = 0
    #     for i in range(len(test_set)):
    #         # print("Running Baes at fold #", i)
    #         test = naive_bayes_testing(test_set[i], trained_values)
    #         # print(test, test_set[i]['class'])
    #         if test == 'no':
    #             if test == test_set[i]['class']:
    #                 count += 1
    #                 rightclass_no += 1
    #             else:
    #                 missclass_no_yes += 1
    #         else:
    #             if test == test_set[i]['class']:
    #                 count += 1
    #                 rightclass_yes += 1
    #             else:
    #                 missclass_yes_no += 1

        # print("Fold {} Accuracy: {}".format(key, count/len(test_set)))
        # accuracy_list.append(count/len(test_set))
    # total_tests = rightclass_yes + rightclass_no + missclass_no_yes + missclass_yes_no
    # print('\n ---------- NAIVE BAYES------------------')
    # print("Final accuracy:", (rightclass_yes+rightclass_no) / total_tests)
    # print("Confusion Matrix: yes   no")
    # print("Correct Class     {}    {}".format(rightclass_yes, rightclass_no))
    # print("Misclassified     {}    {}".format(missclass_yes_no, missclass_no_yes))

def run_knn(k, train_set, test_set):
    knn_l = []


    for item in test_set:
        knn_class = new_euclidian_distance(train_set, item)
        knn_l += [knn_class]
    return knn_l

    # for key in folds_dict:
    #     to_train = []
    #     for key_ in folds_dict:
    #         if key_ != key:
    #             to_train = to_train + folds_dict[key_]
    #     for line in folds_dict[key]:
    #         aux = knn(k, to_train, line)
    #         if aux == "no":
    #             if aux == line['class']:
    #                 countKNN += 1   
    #                 rightclass_no += 1
    #             else:
    #                 missclass_no_yes += 1
    #         if aux == "yes":
    #             if aux == line['class']:
    #                 countKNN += 1
    #                 rightclass_yes += 1
    #             else:
    #                 missclass_yes_no += 1
    # total_tests = rightclass_yes + rightclass_no + missclass_no_yes + missclass_yes_no
    # print("\n ------------------ {}NN -------------------".format(k))
    # print("Final Accuracy: {}".format(countKNN/total_tests))
    # print("Confusion Matrix: yes    no")
    # print("Correct Class     {}    {}".format(rightclass_yes, rightclass_no))
    # print("Misclassified     {}    {}".format(missclass_yes_no, missclass_no_yes))

                
if __name__ == '__main__':
    # print("Number of arguments:", len(sys.argv))
    # print("Arguments", sys.argv[3])

    train_file = sys.argv[1]
    training_set = build_set_from(train_file)
    test_file = sys.argv[2]
    test_set = build_set_from(test_file)
    # print(training_set[500])
    training_set = sorted(training_set, key = lambda k: k['class'])
    
    # create_folds_file(training_set)
    # folds_dict = build_folds_dict()

    if(sys.argv[3].endswith('NN')):
        k = re.findall('\d+', sys.argv[3])
        k = int(k[0])
        tested_set = run_knn(k, training_set, test_set)

    if sys.argv[3] == 'NB':
        tested_set = run_folded_bayes(training_set, test_set)

    for i in tested_set:
        print i
