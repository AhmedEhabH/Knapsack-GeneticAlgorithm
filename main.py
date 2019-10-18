import knapsackGA
import readFile

test_cases, numbers_items, sizes, all_items = readFile.read_all('input_example.txt')
# test_cases, numbers_items, sizes, all_items = readFile.read_all('test.txt')
# print(items)
for i in range(test_cases):
    number_items = numbers_items[i]
    size_knapsack = sizes[i]
    items = all_items[i]
    # print(number_items)
    # print(size_knapsack)
    # print(items)
    print("Case: ", i + 1)
    knapsackGA.main(number_items, size_knapsack, items)
