from main import read_txt_file

def get_times(files):
    row = files[0].split(' ')
    # keep only values of row that are digits
    times = [x for x in row if x.isdigit()]
    # create one big string of all elements in times
    times = ''.join(times)

    row1 = files[1].split(' ')
    # keep only values of row that are digits
    distances = [x for x in row1 if x.isdigit()]
    # create one big string of all elements in times
    distances = ''.join(distances)

    return (times, distances)


def compute_wins(time, distance):
    wins = 0
    for i in range(0, time):
        remaining_time = time - i
        my_distance = i*remaining_time
        if my_distance > distance:
            wins += 1
    return wins


def open_door_6():
    files = read_txt_file('door_6_1_test')

    t_d = get_times(files)
    time = t_d[0]
    distance = t_d[1]

    wins = compute_wins(int(time), int(distance))
    # compute product of all elements in total wins
    print('product of wins: ', wins)


if __name__ == '__main__':
    open_door_6()