import re

from main import read_txt_file

star = '*'
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


def check_neighbours_numbers(key, start, end, lines):
    count = 0

    relevant_lines = lines[max(0, key - 1):min(len(lines), (key + 2))]
    full_numbers = []
    for key2, relevant_line in enumerate(relevant_lines):
        line_start = max(0, start - 1)
        line_end = min(end + 1, len(relevant_line))
        relevant_line = relevant_line[line_start:line_end]

        # check if any digit is in relevant line
        for m in re.finditer(r'\d+', relevant_line):
            n_start = m.start()
            n_end = m.end()

            left_pos = line_start + n_start
            right_pos = line_start + n_end
            current_number = relevant_lines[key2][left_pos:right_pos]

            while relevant_lines[key2][left_pos-1] != '.' and relevant_lines[key2][left_pos-1] not in symbols:
                current_number = relevant_lines[key2][left_pos-1] + current_number
                left_pos += -1

            while right_pos < len(relevant_lines[key2]) and relevant_lines[key2][right_pos] != '.' and relevant_lines[key2][right_pos] not in symbols:
                current_number = current_number + relevant_lines[key2][right_pos]
                right_pos += 1

            full_numbers.append(current_number)

            count += 1

    if count == 2:
        return int(full_numbers[0]) * int(full_numbers[1])

    else:
        return 0



def check_gears(key, line, lines):
    # find * in line
    sum = 0
    if star in line:
        # find all * in line
        for m in re.finditer(r'\*', line):
            start_star = m.start()
            end_star = m.end()

            sum += check_neighbours_numbers(key, start_star, end_star, lines)
    return sum



def open_door_3():
    lines = read_txt_file('door_3_2')

    sum = 0
    sum_gears = 0
    for key, line in enumerate(lines):
        for m in re.finditer(r'\d+', line):
            start = m.start()
            end = m.end()

            if check_neighbours(key, start, end, lines):
                sum += int(m.group())

        sum_gears += check_gears(key, line, lines)

    print('sum: ', sum)
    print('sum_gears: ', sum_gears)


if __name__ == '__main__':
    open_door_3()
