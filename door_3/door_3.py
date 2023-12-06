import re

from main import read_txt_file

#symbols = ['+', '*', '#', '$']
symbols = ['`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}','|','\\',':','?','/']

def check_neighbours(key, start, end, lines):
    # start with checking the right neighbour
    relevant_lines = lines[max(0,key-1):min(len(lines),(key+2))]
    for relevant_line in relevant_lines:
        relevant_line = relevant_line[max(0, start-1):min(end+1, len(relevant_line))]
        # check if any symbol of relevant line is in symbols
        for symbol in symbols:
            if symbol in relevant_line:
                return True
    return False


def open_door_3():
    lines = read_txt_file('door_3_1')

    sum = 0
    for key, line in enumerate(lines):
        for m in re.finditer(r'\d+', line):
            start = m.start()
            end = m.end()

            if check_neighbours(key, start, end, lines):
                sum += int(m.group())

    print('sum: ', sum)


if __name__ == '__main__':
    open_door_3()
