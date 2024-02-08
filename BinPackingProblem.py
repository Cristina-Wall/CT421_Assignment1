import random
import math
import copy


def read_file():
    file_path = 'binpacking1.txt'
    num_bins = 0
    bins_capacity = []
    bin_cap_temp = 0
    items_and_cap = []
    items = []
    sum_items = 0
    sum_bins_cap = 0
    max_free_bins = 0

    with open(file_path, 'r') as file:
        num_bins = int(file.readline().strip())
        bin_cap_temp = int(file.readline().strip())

        for line in file:
            values = line.split()
            int_values = [int(value) for value in values]
            items_and_cap.append(int_values)

    for x in range(len(items_and_cap)):
        for y in range(items_and_cap[x][1]):
            items.append(items_and_cap[x][0])

    for z in range(num_bins):
        bins_capacity.append(bin_cap_temp)

    sum_items = sum(items)
    sum_bins_cap = bin_cap_temp * num_bins
    max_free_bins = math.floor((sum_bins_cap - sum_items)/1000)

    return num_bins, bins_capacity, items, max_free_bins


def count_fitness(bins_cap):
    num_empty_bins = 0
    fitness = 0
    small_fitness = 0

    for g in range(len(bins_cap)):
        if bins_cap[g] == 1000:
            num_empty_bins = num_empty_bins + 1
        elif bins_cap[g] < 0:
            fitness = -1
            return fitness
        else:
            small_fitness = small_fitness + bins_cap[g]/(1000 - bins_cap[g])

        fitness = num_empty_bins + small_fitness
    return fitness


def single_point_crossover(parent_list1, parent_list2, point):

    for y in range(point, len(parent_list1)):
        parent_list1[y], parent_list2[y] = parent_list2[y], parent_list1[y]

    return parent_list1, parent_list2


def best_crossover_point(list1, list2):
    best_fitness = 0
    temp1 = []
    temp2 = []
    best_cross_point = 0

    for z in range(len(items)):
        temp1, temp2 = single_point_crossover(list1, list2, z)
        fit1 = count_fitness(temp1)
        fit2 = count_fitness(temp2)
        if fit1 > fit2:
            if fit1 > best_fitness:
                best_fitness = fit1
                best_cross_point = z
        elif fit2 > fit1:
            if fit2 > best_fitness:
                best_fitness = fit2
                best_cross_point = z

    return best_cross_point


def choose_parents(population_in):
    parents = [random.choice(population_in), random.choice(population_in), random.choice(population_in),
               random.choice(population_in)]
    parents_fitness = []
    second_best = ""
    second_best_fitness = None

    for h in range(len(parents)):
        parents_fitness.append(count_fitness(parents[h]))

    pairs = zip(parents, parents_fitness)
    max_pair = max(pairs, key=lambda pair: pair[1])
    max_item, max_score = max_pair

    index_to_remove = parents.index(max_item)
    del parents[index_to_remove]
    del parents_fitness[index_to_remove]
    pairs = zip(parents, parents_fitness)

    second_max_pair = max(pairs, key=lambda pair: pair[1])
    second_max_item, second_max_score = second_max_pair

    second_best_fitness = parents_fitness[0]
    for x in range(len(parents)):
        if second_best_fitness < parents_fitness[x] and second_best != max_item:
            second_best_fitness = parents_fitness[x]

    return max_item, second_max_item


num_bins, bins_capacity, items, max_free_bins = read_file()

population = []
population_capacity = []
fitness_array = []
bins = []

# generate a population of 50 sets of bins
for k in range(50):
    bins_capacity1 = copy.copy(bins_capacity)

    # randomise order of items
    random.shuffle(items)

    curr_bin = 0
    temp_bin = []

    for i in range(len(items)):
        if items[i] <= bins_capacity1[curr_bin]:
            temp_bin.append(items[i])
            bins_capacity1[curr_bin] = bins_capacity1[curr_bin] - items[i]
        elif items[i] > bins_capacity1[curr_bin]:
            bins.append(copy.copy(temp_bin))
            temp_bin.clear()
            curr_bin = curr_bin + 1
            bins_capacity1[curr_bin] = bins_capacity1[curr_bin] - items[i]
            temp_bin.append(items[i])

    bins.append(copy.copy(temp_bin))
    temp_bin.clear()

    fitness = count_fitness(bins_capacity1)
    fitness_array.append(fitness)
    population_capacity.append(copy.copy(bins_capacity1))

population.append(copy.copy(bins))
avg_fitness = sum(fitness_array) / len(fitness_array)

for i in range(50):
    fitness_array.clear()
    children_population = copy.copy(population_capacity)

    for j in range(0, len(population_capacity), 2):
        parent1, parent2 = choose_parents(population_capacity)  # chooses 4 random strings and gets best 2 of 4
        best_point = best_crossover_point(parent1, parent2)  # finds the crossover point where the fitness is highest
        child1, child2 = single_point_crossover(parent1, parent2, best_point)

        fitness_array.append(count_fitness(child1))
        fitness_array.append(count_fitness(child2))

        children_population[j] = child1
        children_population[j+1] = child2

    avg_fitness = sum(fitness_array) / len(fitness_array)

    population = children_population
    print("Gen ", i+1, " fitness: ", avg_fitness)
