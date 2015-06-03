import random, statistics

#the tables are upside down so it can follow 0 = False and 1 = True
class BayesNet():
	cloudy = 0.5
	sprinkler = [0.5, 0.1] # [P(S|~c), P(S|c)]
	rain = [0.2, 0.8] # [P(R|~c), P(R|c)]
	#row 0 = ~s; row 1 = s
	#colum 0 = ~r; colum 1 = r
	wet_grass = [[0.0, 0.9], [0.9, 0.99]] # [[P(W|~s, ~r), P(W|~s, r)], [P(W|s,~r), P(W|s,r)]] 

	# P(C, S, R, W) = P(C) * P(S|C) * P(R|C) * P(W|S,R)
	def evaluate(this, event_vector):
		c_val, s_val, r_val, w_val = event_vector
		return this.cloudy * this.sprinkler[c_val] * this.rain[c_val] * this.wet_grass[s_val][r_val]

	#returns 1 for True and 0 for False
	def sample_cloudy(this):
		return random.randint(0,1)

	def sample_sprinkler(this, c_val):
		s_iter = this.sprinkler[c_val] * 10
		s_iter = int(s_iter)
		choices = [1] * s_iter + [0] * (10 - s_iter)
		return random.choice(choices)

	def sample_rain(this, c_val):
		r_iter = this.rain[c_val] * 10
		r_iter = int(r_iter)
		choices = [1] * r_iter + [0] * (10 - r_iter)
		return random.choice(choices)

	def sample_wgrass(this, s_val, r_val):
		w_iter = this.wet_grass[s_val][r_val] * 100
		w_iter = int(w_iter)
		choices = [1] * w_iter + [0] * (100 - w_iter)
		return random.choice(choices)

#function to be used for filtering
def is_csw(tup):
	c, r, s, w = tup
	return True if c == 1 and s == 1 and w == 1 else False


def variance(sample):
	m = statistics.mean(sample)
	discriminant = map(lambda x: (x - m) ** 2, sample)
	return sum(discriminant) / (len(sample) - 1)




if __name__ == '__main__':
	my_net = BayesNet()


	vector_matrix = {}

	# x = input("Please insert m and n: ")
	x = '100, 1000'
	s = [int(num) for num in x.split(',')]
	m, n = s[0], s[1]

	for j in range(n):
		csw_prob_list = []
		for i in range(m):
			w = 1
			sample_vector = [0, 0, 1, 1] #(cloud, rain, sprinkler, wet grass)

			#cloudy iteration
			sample_vector[0] = my_net.sample_cloudy()

			#rain iteration
			sample_vector[1] = my_net.sample_rain(sample_vector[0])

			#sprinkler iterations
			sprink_prob = my_net.sprinkler[sample_vector[0]]
			w = w * sprink_prob

			#wet grass iteration
			grass_prob = my_net.wet_grass[1][sample_vector[1]]
			w = w * grass_prob

			sample_tuple = tuple(sample_vector)
			if sample_tuple in vector_matrix.keys():
				vector_matrix[sample_tuple] += w
			else:
				vector_matrix[sample_tuple] = w

			tot_prob = sum(vector_matrix.values())

			csw_keys = filter(is_csw, vector_matrix.keys())
			csw_tot = 0
			for key in csw_keys:
				csw_tot += vector_matrix[key]
			
			csw_prob = csw_tot / tot_prob
			csw_prob_list.append(csw_prob)


	csw_mean = round(statistics.mean(csw_prob_list), 6)
	csw_var = round(variance(csw_prob_list), 6)
	print(csw_mean, csw_var)	