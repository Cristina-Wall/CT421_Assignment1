import random


def random_string(length):
    initial_string = ""

    for i in range(0, length):
        a = random.randint(0, 1)
        initial_string = initial_string + str(a)
    return initial_string


def random_array(length):
    initial_array = []

    for i in range(0, length):
        a = random.randint(0, 1)
        initial_array.append(a)
    return initial_array


def count_fitness_array(input_array):
    curr_fitness = 0

    for x in range(len(input_array)):
        if input_array[x] == 1:
            curr_fitness += 1
    return curr_fitness


def count_fitness_string(input_string):
    curr_fitness = 0

    for x in input_string:
        if x == "1":
            curr_fitness += 1
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


new1 = random_string(30)
new2 = random_string(30)
print("Parent1 :", new1)
print("Parent2 :", new2, "\n")
fitness1 = count_fitness_string(new1)
fitness2 = count_fitness_string(new2)
print("Fitness P1 :", fitness1)
print("Fitness P2 :", fitness2, "\n")

for i in range(5):
    print("Generation ", i+1, " Children:")
    best_point = best_crossover_point(new1, new2)
    print("Best point : ", best_point)
    new1, new2 = single_point_crossover(new1, new2, best_point)
    fitness1 = count_fitness_string(new1)
    fitness2 = count_fitness_string(new2)
    if fitness2 > fitness1:
        temp = new1
        new1 = new2
        new2 = temp
    print("Child1 :", new1)
    print("Child2 :", new2, "\n")
    fitness1 = count_fitness_string(new1)
    fitness2 = count_fitness_string(new2)
    print("Fitness C1 :", fitness1)
    print("Fitness C2 :", fitness2, "\n")

