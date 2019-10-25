import random
import numpy as np
import knapsackDP
import gc


class Knapsack:
    number_items = 0
    capacity = 0
    items = []
    population = []
    population_copy = []
    my_optimal = 0
    optimal_val = 0
    max_optimal = -1
    best_items = []

    def __init__(self, number_items, capacity, items, optimal_val):
        self.number_items = number_items
        self.capacity = capacity
        self.items = items
        self.optimal_val = optimal_val
        self.max_optimal = -1
        self.best_items = []

    def initialize_population(self, population_size=100):
        self.population = []
        i = 0
        while i < population_size:
            if random.uniform(0, 1) < .5:
                cromosome = [random.randint(0, 1) for i in range(self.number_items)]
                i += 1
                self.population.append(cromosome)
        self.population_copy = self.population.copy()

    def calculate_fitness(self, population):
        fitness = [0] * len(population)
        for i in range(len(population)):
            value = 0
            weight = 0
            for j in range(self.number_items):
                weight += population[i][j] * self.items[j][0]
                value += population[i][j] * self.items[j][1]
                if weight <= self.capacity:
                    fitness[i] = value
        return fitness.copy()

    def create_roulette_wheel(self, fitness):
        roulette_wheel = list(np.cumsum(fitness))
        return roulette_wheel.copy()

    def select_items(self, roulette_wheel):
        selection = []
        for _ in range(len(roulette_wheel)):
            rand_num = random.randint(0, roulette_wheel[-1])
            for i in range(len(roulette_wheel)):
                if rand_num <= roulette_wheel[i]:
                    selection.append(i)
                    break
        return selection.copy()

    def crossover(self, cromosome1, cromosome2):
        r2 = random.uniform(0, 1)
        if r2 <= .7:
            r1 = random.randint(1, self.number_items - 1)
            cromosome1[r1:], cromosome2[r1:] = cromosome2[r1:], cromosome1[r1:]
        return cromosome1.copy(), cromosome2.copy()

    def mutation(self, population):
        for i in range(len(population)):
            population[i] = self.mutation_cromosome(population[i])
        return population.copy()

    def mutation_cromosome(self, cromosome):
        for i in range(self.number_items):
            if random.random() <= .1:
                cromosome[i] = 1 if cromosome[i] == 0 else 0
        return cromosome.copy()

    # Ascending
    def sort_according_to_fitness(self, fitness, target):
        return [i for _, i in sorted(zip(fitness, target))].copy()

    def replacement(self, pop1, pop2):
        fitness_pop2 = self.calculate_fitness(pop2)
        fitness_pop1 = self.calculate_fitness(pop1)
        
        pop2 = self.sort_according_to_fitness(fitness_pop2, pop2)
        pop1 = self.sort_according_to_fitness(fitness_pop1, pop1)
        gc.collect()
        return pop2[len(pop2) // 2:].copy(), pop1[len(pop1) // 2:].copy()

    def run(self):
        # Step 1 - initialize population
        # print("Step #1 - initialize population")
        # population_size = (self.number_items * ((self.number_items))) * 5 if self.number_items <= 35 else ((self.number_items) ** 3) * 50
        # iteration_size = self.number_items if self.number_items <= 35 else population_size // 2
        population_size = 0
        iteration_size = 0
        if self.number_items < 20:
            population_size = self.number_items * 2
            iteration_size = 100
        elif self.number_items <= 30:
            population_size = self.number_items * 25
            iteration_size = 100
        elif self.number_items <= 50:
            population_size = self.number_items * 100
            iteration_size = 50
        else:
            population_size = self.number_items * 100
            iteration_size = 100
        # population_size = self.number_items * 20
        # iteration_size = 100
        self.initialize_population(population_size)
        iteration = 0
        profits = []
        while iteration < iteration_size:
            iteration += 1
            # print("Iteration #{}".format(iteration))

            # Step 2 - Fitness
            # print("Step #2 - Fitness")
            fitness = self.calculate_fitness(self.population_copy)

            # Step 3 - Selection
            # print("Step #3 - Selection")
            roulette_wheel = self.create_roulette_wheel(fitness)
            selection = self.select_items(roulette_wheel)

            # Step 4 - Crossover
            # print("Step #4 - Crossover")
            new_generation = [self.population_copy[i].copy() for i in selection]
            
            fitness_new_gen = self.calculate_fitness(new_generation) 
            new_generation = self.sort_according_to_fitness(fitness_new_gen, new_generation)

            fitness_population_copy = self.calculate_fitness(self.population_copy)
            self.population_copy = self.sort_according_to_fitness(fitness_population_copy, self.population_copy)

            self.population_copy[:len(self.population_copy) // 2] = new_generation[len(new_generation) // 2:]

            for i in range(1, len(self.population_copy), 2):
                self.population_copy[i - 1], self.population_copy[i] = self.crossover(self.population_copy[i], self.population_copy[i-1])
            random.shuffle(self.population_copy)
            
            # Step 5 - Mutation
            # print("Step #5 - Mutation")
            self.population_copy = self.mutation(self.population_copy)
            
            # Step 6 - Calculate profits
            profits = self.calculate_fitness(self.population_copy)
            self.my_optimal = max(profits)

            if self.my_optimal > self.max_optimal: 
                self.max_optimal = self.my_optimal
                index = profits.index(self.max_optimal)
                self.best_items = self.population_copy[index].copy()
                


            # Step 7 - try to avoid no change
            if self.population == self.population_copy:
                self.population_copy = self.mutation(self.population_copy)

            self.population_copy[:len(self.population_copy) // 2], self.population[:len(self.population) // 2] = self.replacement(self.population_copy, self.population)
            gc.collect()
        # print("Optimal after {0} iteration(s).".format(iteration))
        print("Optimal from knapsack GA:", self.max_optimal)
        # print("Best Items:")
        # print(self.best_items)
        value_sum = 0
        weight_sum = 0
        for i in range(len(self.best_items)):
                weight_sum += (self.items[i][0] * self.best_items[i])
                value_sum += (self.items[i][1] * self.best_items[i])
        # print("{0} => {1}".format(weight_sum, value_sum))
        # print(self.best_items)
        [print("{0} - {1}".format(self.items[i][0], self.items[i][1])) for i in range(len(self.best_items)) if self.best_items[i] == 1]
        if self.max_optimal < self.optimal_val: print("*" * 50)
        else: print("=" * 50)


def main(number_items, size_knapsack, items):
    wt = [i[0] for i in items]
    val = [i[1] for i in items]
    optimal_val = knapsackDP.knapSack(size_knapsack, wt, val, len(val))
    print("The optimal value from normal knapsack = {0} with weight = {1} by {2} items".format(optimal_val, size_knapsack, len(items)))
    # print("Items:")
    # print(items)
    Knapsack_obj = Knapsack(number_items, size_knapsack, items, optimal_val)
    Knapsack_obj.run()

# main(3, 10, [[4, 4], [7, 6], [5,3]])
# main(5, 14, [[4, 1], [7, 7], [1, 22], [3, 23], [3, 6]])
# main(5, 28, [[10, 27], [9, 27], [8, 12], [8, 28], [3, 23]])
