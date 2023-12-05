from main import read_txt_file
import re

relevant_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
relevant_numbers_written = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def find_all_numbers(line):
    numbers_dict = {}

    all_relevant_numbers = relevant_numbers + relevant_numbers_written
    for number in all_relevant_numbers:
        # find number in line
        if number in line:
            for m in re.finditer(number, line):
                if number in relevant_numbers_written:
                    # if number is written, get the number
                    number = relevant_numbers[relevant_numbers_written.index(number)]
                numbers_dict[m.start()] = number

    # sort dict by key
    numbers_dict = dict(sorted(numbers_dict.items()))
    return list(numbers_dict.values())


path = 'door_1_2.txt'

lines = read_txt_file(path)

sum = 0
for line in lines:
    # extract all numbers and written numbers
    all_numbers = find_all_numbers(line)

    # get first number from numbers
    first_number = int(all_numbers[0])
    last_number = int(all_numbers[-1])

    sum += first_number*10 + last_number

print('sum: ', sum)