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
        # self.population = [[random.randint(0, 1) for _ in range(
        #     self.number_items)] for __ in range(pop_size)]
        for _ in range(pop_size):
            cromosome = []
            j = 0
            while j < self.number_items:
                rand_num = random.randint(0, 1)
                if random.uniform(0, 1) >= .5:
                    cromosome.append(rand_num)
                    j += 1
            self.population.append(cromosome)
        self.pop_copy = self.population.copy()

    def calc_fitness(self, items):
        fitness = [0] * len(self.population)
        for i in range(len(self.population)):
            value = 0
            weight = 0
            for j in range(self.number_items):
                weight += self.population[i][j] * items[j][0]
                value += self.population[i][j] * items[j][1]
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
            rand_num = random.randint(0, len(roulette_wheel)-1)
            for i in range(len(roulette_wheel)):
                if rand_num <= roulette_wheel[i]:
                    selection.append(i)
                    break
        return selection

    def crossover(self, item1, item2):
        r1 = random.randint(1, self.number_items-1)  # Crossover point
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
        profits = [0] * len(self.population)
        for i in range(len(self.pop_copy)):
            value = 0
            for j in range(self.number_items):
                value += self.population[i][j] * items[j][1]
            profits[i] = value
        return profits

    def run(self):
        # Step 1 - initialize population
        self.initialize_population(1000)
        iteration = 0
        cromosome = []
        profits = []
        while (self.my_optimal != self.optimal_val) and iteration < 1000 or self.my_optimal <= self.optimal_val:
            iteration += 1
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
            self.population = self.pop_copy.copy()
        print("Optimal after {0} iteration(s).".format(iteration))
        print("Optimal from knapsack GA", self.my_optimal)
        [print(self.items[i])
         for i in range(len(cromosome)) if cromosome[i] == 1]


def main(number_items, size_knapsack, items):
    wt = [i[0] for i in items]
    val = [i[1] for i in items]
    optimal_val = knapsackDP.knapSack(size_knapsack, wt, val, len(val))
    print("The optimal value from normal knapsack = ", optimal_val)
    Knapsack_obj = Knapsack(number_items, size_knapsack, items, optimal_val)
    Knapsack_obj.run()


# main(50, 908, [[4, 286], [36, 239], [35, 591], [16, 784], [40, 244], [35, 546], [4, 769], [26, 93], [4, 598], [24, 500], [23, 273], [50, 846], [33, 882], [10, 347], [40, 592], [30, 527], [10, 623], [16, 288], [15, 68], [25, 599], [32, 595], [2, 592], [45, 336], [2, 99], [40, 64], [44, 135], [23, 261], [3, 53], [14, 203], [40, 279], [28, 628], [4, 392], [42, 162], [23, 109], [46, 116], [37, 248], [38, 46], [2, 406], [28, 912], [27, 784], [5, 335], [46, 536], [50, 394], [21, 893], [36, 657], [28, 168], [35, 200], [23, 88], [35, 599], [20, 299]])
