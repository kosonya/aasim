import random

def compute_stats(sample):
	res = {"count_A": 0,
		   "mean_A" : 0,
		   "count_B": 0,
		   "mean_B": 0,
		   "portion_A": 0,
		   "portion_B": 0,
		   "count_ratio_A_to_B": 0,
		   "mean_ratio_A_to_B": 0,
		   "total_count": 0,
		   "total_mean": 0}
	for item in sample:
		value, kind = item
		res["total_count"] += 1
		res["total_mean"] += value
		if kind == "A":
			res["count_A"] += 1
			res["mean_A"] += value
		elif kind == "B":
			res["count_B"] += 1
			res["mean_B"] += value
	if res["count_A"] > 0:		
		res["mean_A"] = float(res["mean_A"]) / res["count_A"]
	if res["count_B"] > 0:
		res["mean_B"]  = float(res["mean_B"]) / res["count_B"]
	res["total_mean"] = float(res["total_mean"]) / res["total_count"]
	res["portion_A"] = float(res["count_A"]) / res["total_count"]
	res["portion_B"] = float(res["count_B"]) / res["total_count"]
	if res["count_B"] > 0:
		res["count_ratio_A_to_B"] = float(res["count_A"]) / res["count_B"]
	if res["mean_B"] > 0:
		res["mean_ratio_A_to_B"] = float(res["mean_A"]) / res["mean_B"]
	
	return res
	
def biased_filter(sample, pro_a_bias = 1):
	res = []
	alpha = 0.5
	_beta = 2
	mean = sum(v for (v, _) in sample)/float(len(sample))
	_gamma = mean
	for item in sample:
		value, kind = item
		if value <= 0:
			continue
		beta = _beta
		gamma = _gamma
		if kind == "A":
			gamma = gamma / pro_a_bias
		if gamma / value < random.weibullvariate(alpha, beta):
			res.append(item)
	return res
	
def create_samples(n_samples = 100000, mu = 0.5, sigma = 1, pa = 0.5):
	res = []
	for _ in xrange(n_samples):
		value = random.lognormvariate(mu, sigma)
		if random.uniform(0,1) < pa:
			kind = "A"
		else:
			kind = "B"
		res.append((value, kind))
	return res
	
def main():
	general_population = create_samples()
	stats = compute_stats(general_population)
	print "General population:", stats, "\n\n"
	
	tier1_filtered = biased_filter(general_population, pro_a_bias = 10)
	stats = compute_stats(tier1_filtered)
	print "After tier 1 filtering:", stats, "\n\n"

	tier2_filtered = biased_filter(tier1_filtered, pro_a_bias = 0.1)
	stats = compute_stats(tier2_filtered)
	print "After tier 2 filtering:", stats, "\n\n"
	
	
if __name__ == "__main__":
	main()
	
