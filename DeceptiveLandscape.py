import random


def random_string(length):
    initial_string = ""

    for h in range(0, length):
        a = random.randint(0, 1)
        initial_string = initial_string + str(a)
    return initial_string


def count_fitness_string(input_string):
    curr_fitness = 0

    curr_fitness = input_string.count("1")
    if curr_fitness == 0:
        curr_fitness = 2 * len(input_string)

    return curr_fitness


def single_point_crossover(parent_string1, parent_string2, point):
    string1 = list(parent_string1)
    string2 = list(parent_string2)

    for y in range(point, len(parent_string1)):
        string1[y], string2[y] = string2[y], string1[y]
    new_string1 = ''.join(string1)
    new_string2 = ''.join(string2)

    return new_string1, new_string2


def best_crossover_point(string1, string2):
    best_fitness = 0
    temp1 = ""
    temp2 = ""
    best_cross_point = 0

    for z in range(30):
        temp1, temp2 = single_point_crossover(string1, string2, z)
        fit1 = count_fitness_string(temp1)
        fit2 = count_fitness_string(temp2)
        if fit1 > fit2:
            if fit1 > best_fitness:
                best_fitness = fit1
                best_cross_point = z
        elif fit2 > fit1:
            if fit2 > best_fitness:
                best_fitness = fit2
                best_cross_point = z

    return best_cross_point


def mutate_string(string):
    element = random.randint(1, len(string)-1)
    string = string[:element-1] + str(abs(int(string[element])-1)) + string[element:]
    return string


def choose_parents(population_in):
    parents = [random.choice(population_in), random.choice(population_in), random.choice(population_in),
               random.choice(population_in)]
    parents_fitness = []
    second_best = ""
    second_best_fitness = None

    for k in range(len(parents)):
        parents_fitness.append(count_fitness_string(parents[k]))
    best_parent_fitness = max(parents_fitness)

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


# make population of strings and calculate fitness
population = []
fitness_array = []
children_population = []

for i in range(50):
    temp_string = random_string(30)
    population.append(temp_string)
    fitness_array.append(count_fitness_string(temp_string))
    children_population.append('')

avg_fitness = sum(fitness_array) / len(fitness_array)
print("Gen 0 fitness: ", avg_fitness)

for i in range(50):
    fitness_array.clear()

    for j in range(0, len(population), 2):
        parent1, parent2 = choose_parents(population)  # chooses 4 random strings and gets best 2 of 4
        best_point = best_crossover_point(parent1, parent2)  # finds the crossover point where the fitness is highest
        child1, child2 = single_point_crossover(parent1, parent2, best_point)
        child1 = mutate_string(child1)  # random mutation of one bit
        child2 = mutate_string(child2)

        fitness_array.append(count_fitness_string(child1))
        fitness_array.append(count_fitness_string(child2))

        children_population[j] = child1
        children_population[j+1] = child2

    avg_fitness = sum(fitness_array) / len(fitness_array)

    population = children_population
    print("Gen ", i+1, " fitness: ", avg_fitness)
