import random
import numpy as np
import knapsackDP
import gc
import time


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
        div = len(pop1) // 2
        pop1[:div], pop2[:div] = pop2[div:].copy(), pop1[div:].copy()
        return pop1, pop2

    def run(self):
        # Step 1 - initialize population
        population_size = 0
        iteration_size = 0
        if self.number_items < 15:
            population_size = self.number_items * 20
            iteration_size = 40
        elif self.number_items < 25:
            population_size = self.number_items * 25
            iteration_size = 50
        elif self.number_items < 50:
            population_size = self.number_items * 25
            iteration_size = 70
        else:
            population_size = self.number_items * 3
            iteration_size = 21 * self.number_items
        self.initialize_population(population_size)
        iteration = 0
        profits = []
        while iteration < iteration_size:
            iteration += 1
            # Step 2 - Fitness
            fitness = self.calculate_fitness(self.population_copy)

            # Step 3 - Selection
            roulette_wheel = self.create_roulette_wheel(fitness)
            selection = self.select_items(roulette_wheel)

            # Step 4 - Crossover
            new_generation = [self.population_copy[i].copy() for i in selection]

            self.population_copy[:len(self.population_copy) // 2] = new_generation[len(new_generation) // 2:]

            for i in range(1, len(self.population_copy), 2):
                self.population_copy[i - 1], self.population_copy[i] = self.crossover(self.population_copy[i], self.population_copy[i-1])
            
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

            self.population_copy, self.population = self.replacement(self.population_copy, self.population)
            gc.collect()
        
        print("Optimal from knapsack GA:", self.max_optimal)
        [print("{0} - {1}".format(self.items[i][0], self.items[i][1])) for i in range(len(self.best_items)) if self.best_items[i] == 1]
        if self.max_optimal < self.optimal_val: print("*" * 50)
        else: print("=" * 50)


def main(number_items, size_knapsack, items):
    print("Started:", time.ctime())
    wt = [i[0] for i in items]
    val = [i[1] for i in items]
    optimal_val = knapsackDP.knapSack(size_knapsack, wt, val, len(val))
    Knapsack_obj = Knapsack(number_items, size_knapsack, items, optimal_val)
    Knapsack_obj.run()
    print("Ended:", time.ctime())

# main(3, 10, [[4, 4], [7, 6], [5,3]])
# main(5, 14, [[4, 1], [7, 7], [1, 22], [3, 23], [3, 6]])
# main(5, 28, [[10, 27], [9, 27], [8, 12], [8, 28], [3, 23]])
# main(50, 886, [[50, 788], [50, 310], [17, 158], [28, 687], [16, 148], [48, 590], [21, 212], [36, 722], [9, 535], [49, 703], [33, 206], [49, 696], [20, 42], [35, 885], [47, 797], [19, 827], [8, 398], [31, 191], [36, 160], [17, 847], [44, 825], [32, 456], [1, 40], [8, 147], [37, 542], [31, 456], [13, 857], [30, 166], [6, 814], [25, 507], [20, 724], [8, 700], [22, 415], [38, 595], [24, 659], [29, 881], [22, 364], [32, 106], [4, 659], [35, 221], [18, 413], [32, 58], [4, 825], [3, 360], [30, 200], [4, 272], [31, 111], [50, 863], [4, 728], [8, 62]])
# main(50, 908, [[4, 286], [36, 239], [35, 591], [16, 784], [40, 244], [35, 546], [4, 769], [26, 93], [4, 598], [24, 500], [23, 273], [50, 846], [33, 882], [10, 347], [40, 592], [30, 527], [10, 623], [16, 288], [15, 68], [25, 599], [32, 595], [2, 592], [45, 336], [2, 99], [40, 64], [44, 135], [23, 261], [3, 53], [14, 203], [40, 279], [28, 628], [4, 392], [42, 162], [23, 109], [46, 116], [37, 248], [38, 46], [2, 406], [28, 912], [27, 784], [5, 335], [46, 536], [50, 394], [21, 893], [36, 657], [28, 168], [35, 200], [23, 88], [35, 599], [20, 299]])