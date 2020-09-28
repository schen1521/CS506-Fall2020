from collections import defaultdict
from math import inf
import random
import csv


def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """
    x = 0
    y = 0
    for i in range(len(points)):
        x += points[i][0]
        y += points[i][1]
    x /= len(points)
    y /= len(points)
    return [x, y]


def update_centers(dataset, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the center for each of the assigned groups.
    Return `k` centers in a list
    """
    dictionary = {}
    for i in range(len(dataset)):
        if assignments[i] not in dictionary:
            dictionary[assignments[i]] = []
        dictionary[assignments[i]].append(dataset[i])

    for i in dictionary:
        dictionary[i] = point_avg(dictionary[i])
    return [dictionary[i] for i in sorted(dictionary.keys())]
    

def assign_points(data_points, centers):
    """
    """
    assignments = []
    for point in data_points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    Returns the Euclidean distance between a and b
    """
    if (len(a) != len(b)) :
        raise ValueError("Length must be equal")
    result = sum([(a[i] - b[i])**2 for i in range(len(a))])
    return result**(1/2)


def distance_squared(a, b):
    return distance(a, b)**2


def generate_k(dataset, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    """
    # create a list of number 0 - len(dataset)
    # chooses k random numbers
    nums = list(range(0, len(dataset)))
    points = random.choices(nums, k=k)
    return [dataset[i] for i in points]


def cost_function(clustering):
    cost = 0
    for i in clustering:
        temp = 0
        avg = point_avg(clustering[i])
        for j in clustering[i]:
            temp += distance_squared(j, avg)

        cost += temp
    return cost


def generate_k_pp(dataset, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    where points are picked with a probability proportional
    to their distance as per kmeans pp
    """
    centers = []
    for i in range(k):
        if centers == []:
            centers.append(random.choice(list(range(0, len(dataset)))))
        else:
            dist = []
            for j in dataset:
                dist.append(min([distance_squared(j, dataset[x]) for x in centers]))
            summ = sum(dist)
            dist = [x/summ for x in dist]
            centers.append(random.choices(population = list(range(0, len(dataset))), weights = dist, k = 1)[0])
    return [dataset[i] for i in centers]


def _do_lloyds_algo(dataset, k_points):
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, dataset):
        clustering[assignment].append(point)
    return clustering


def k_means(dataset, k):
    if k not in range(1, len(dataset)+1):
        raise ValueError("lengths must be in [1, len(dataset)]")
    
    k_points = generate_k(dataset, k)
    return _do_lloyds_algo(dataset, k_points)


def k_means_pp(dataset, k):
    if k not in range(1, len(dataset)+1):
        raise ValueError("lengths must be in [1, len(dataset)]")

    k_points = generate_k_pp(dataset, k)
    return _do_lloyds_algo(dataset, k_points)
