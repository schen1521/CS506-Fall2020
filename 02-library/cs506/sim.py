def euclidean_dist(x, y):
    result = sum([(abs(x[i] - y[i]))**2 for i in range(len(x))])
    return result**(1/2)

def manhattan_dist(x, y):
    result = sum([abs(x[i] - y[i]) for i in range(len(x))])
    return result


def jaccard_dist(x, y):
	if (len(x) == 0 or len(y) == 0):
		return "lengths must not be zero"
	elif (x == y):
		return 0
	else:
		result = 1 - (len(intersection(x,y))/len(union(x,y)))
		return result


def cosine_sim(x, y):
	lx = len(x)

	if (lx != len(y)):
		return "lengths must be equal"
	elif (lx == 0 or len(y) == 0):
		return "lengths must not be zeros"
	else:
		numerator = sum([x[i]*y[i] for i in range(lx)])
		denom = ((sum([x[i]**2 for i in range(lx)]))**(1/2))*((sum([y[i]**2 for i in range(lx)]))**(1/2))
		return numerator/denom


# Feel free to add more
# helper functions
def intersection(x,y):
	return list(set(x) & set(y))
def union(x,y):
	return list(set(x) | set(y)) 