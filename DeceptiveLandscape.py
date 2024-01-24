import random


def random_string(length):
    initial_string = ""

    for i in range(0, length):
        a = random.randint(0, 1)
        initial_string = initial_string + str(a)
    return initial_string


def count_fitness_string(input_string):
    curr_fitness = 0

    curr_fitness = input_string.count("1")
    if curr_fitness == 0:
        curr_fitness = 2* len(input_string)

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


new1 = random_string(30)
new2 = random_string(30)
fitness_array = []

print("Parent1 :", new1)
print("Parent2 :", new2)
fitness1 = count_fitness_string(new1)
fitness2 = count_fitness_string(new2)
print("Fitness P1 :", fitness1)
print("Fitness P2 :", fitness2, "\n")
if fitness1 >= fitness2:
    fitness_array.append(fitness1)
elif fitness2 > fitness1:
    fitness_array.append(fitness2)

for i in range(50):
    print("Generation ", i+1)
    best_point = best_crossover_point(new1, new2)
    new1, new2 = single_point_crossover(new1, new2, best_point)
    fitness1 = count_fitness_string(new1)
    fitness2 = count_fitness_string(new2)
    if fitness2 > fitness1:
        temp = new1
        new1 = new2
        new2 = temp
    print("Child1 :", new1)
    print("Child2 :", new2)
    fitness1 = count_fitness_string(new1)
    fitness2 = count_fitness_string(new2)
    fitness_array.append(fitness1)
    print("Fitness C1 :", fitness1)
    print("Fitness C2 :", fitness2, "\n")

    new2 = mutate_string(new2)

print(fitness_array)
