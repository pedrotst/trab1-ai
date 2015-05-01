import statistics
from math import sqrt
def mean(data_list):
    return sum(data_list) / len(data_list)

def stdev(data_list):
    data_mean = mean(data_list)
    variance = sum([(x - data_mean) ** 2 for x in data_list]) / (len(data_list) - 1)
    return sqrt(variance)

x = [1.5, 2.5, 2.5, 2.75, 3.25, 4.75]
print(statistics.mean(x), statistics.stdev(x))
print(mean(x), stdev(x))