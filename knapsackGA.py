import random
import numpy as np
import knapsackDP


class Knapsack():
    number_items = 0
    size = 0
    population = []
    pop_copy = []
    items = []
    optimal_val = -1
    my_optimal = 0

    def __init__(self, number_items, size, items, optimal_val):
        self.number_items = number_items
        self.size = size
        self.items = items
        self.optimal_val = optimal_val
        self.population = []
        self.pop_copy = []

    def initialize_population(self, pop_size=500):
        self.population = []
        for _ in range(pop_size):
            cromosome = []
            j = 0
            while j < self.number_items:
                rand_num = random.randint(0, 1)
                if random.random() < .5:
                    cromosome.append(rand_num)
                    j += 1
            self.population.append(cromosome)
        self.pop_copy = self.population.copy()

    def calc_fitness(self, items):
        fitness = [0] * len(self.pop_copy)
        for i in range(len(self.pop_copy)):
            value = 0
            weight = 0
            for j in range(self.number_items):
                weight += self.pop_copy[i][j] * items[j][0]
                value += self.pop_copy[i][j] * items[j][1]
                if weight <= self.size:
                    fitness[i] = value
        return fitness

    def create_roulette_wheel(self, fitness):
        roulette_wheel = list(np.cumsum(fitness))
        return roulette_wheel

    def select_items(self, roulette_wheel):
        rand_num = 0
        selection = []
        for _ in range(len(roulette_wheel)):
            rand_num = random.randint(0, roulette_wheel[-1])
            for i in range(len(roulette_wheel)):
                if rand_num <= roulette_wheel[i]:
                    selection.append(i)
                    break
        return selection

    def crossover(self, item1, item2):
        r1 = random.randint(1, self.number_items - 1)  # Crossover point
        crossover_probability = .7
        r2 = random.uniform(0, 1)
        if r2 <= crossover_probability:
            item1[r1:], item2[r1:] = item2[r1:], item1[r1:]
        return item1, item2

    def mutation(self, item):
        for i in range(len(item)):
            if(random.uniform(0, 1) <= .1):
                item[i] = 1 if item[i] == 0 else 0
        return item

    def sort_according_to_fitness(self, fitness, selection):
        return [i for _, i in sorted(zip(fitness, selection))]

    def calc_profit(self, items):
        profits = [0] * len(self.pop_copy)
        for i in range(len(self.pop_copy)):
            value = 0
            for j in range(self.number_items):
                value += self.pop_copy[i][j] * items[j][1]
            profits[i] = value
        return profits

    def run(self):
        # Step 1 - initialize population
        self.initialize_population(100000)
        iteration = 0
        no_change = 0
        small_iteration = 0
        cromosome = []
        profits = []
        while self.my_optimal < self.optimal_val or iteration < 100000:
            iteration += 1
            small_iteration += 1
            # Step 2 - Fitness
            fitness = self.calc_fitness(self.items)

            # Step 3 - Selection
            roulette_wheel = self.create_roulette_wheel(fitness)
            selection = self.select_items(roulette_wheel)

            # Step 4 - Crossover
            sorted_selection = self.sort_according_to_fitness(
                fitness, selection)
            for i in range(1, len(sorted_selection), 2):
                self.pop_copy[sorted_selection[i-1]], self.pop_copy[sorted_selection[i]] = self.crossover(
                    self.pop_copy[sorted_selection[i-1]], self.pop_copy[sorted_selection[i]])

            # Step 5 - Mutation
            for i in range(len(sorted_selection)):
                self.pop_copy[sorted_selection[i]] = self.mutation(
                    self.pop_copy[sorted_selection[i]])

            # Step 6 - Calculate profits
            profits = self.calc_profit(self.items)
            self.my_optimal = self.optimal_val if self.optimal_val in profits else max(
                profits)
            index = profits.index(self.my_optimal)
            cromosome = self.pop_copy[index]
            
            if self.population == self.pop_copy:
                no_change += 1
                if no_change > 3: break
                continue
            else: 
                no_change = 0
                small_iteration = 0
            self.population = self.pop_copy.copy()
        print("Optimal after {0} iteration(s).".format(iteration))
        print("Optimal from knapsack GA", self.my_optimal)
        [print("{0} - {1}".format(self.items[i][0], self.items[i][1])) for i in range(len(cromosome)) if cromosome[i] == 1]
        return self.my_optimal

def main(number_items, size_knapsack, items):
    wt = [i[0] for i in items]
    val = [i[1] for i in items]
    optimal_val = knapsackDP.knapSack(size_knapsack, wt, val, len(val))
    print("The optimal value from normal knapsack = ", optimal_val)
    Knapsack_obj = Knapsack(number_items, size_knapsack, items, optimal_val)
    my_optimal = Knapsack_obj.run()
    if my_optimal < optimal_val: print('*' * 50)
    else: print('=' * 50)
