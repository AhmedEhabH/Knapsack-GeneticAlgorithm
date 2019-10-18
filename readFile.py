import re


test_cases = 0
numbers_items = []
sizes = []
items = []


def read_all(filename):
    input_example = open(filename, 'r+')
    test_cases = int(input_example.readline())
    numbers_items = []
    sizes = []
    items = []
    for line in input_example:
        if not re.search('[0-9]', line):
            continue
        line = re.sub('[A-z]', '', line)
        numbers_items.append(int(line))
        size = input_example.readline()
        size = re.sub('[A-z]', '', size)
        sizes.append(int(size))
        items_set = []
        for ___ in range(int(line)):
            item = input_example.readline()
            weight, value = item.split()
            items_set.append([int(weight), int(value)])
        items.append(items_set)
    return test_cases, numbers_items, sizes, items

# test_cases, numbers_items, sizes, items = read_all("input_example.txt")
# # print(items)
# print(items[len(items)-1])