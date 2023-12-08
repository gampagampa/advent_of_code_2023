from main import read_txt_file

def get_times(files):
    row = files[0].split(' ')
    # keep only values of row that are digits
    times = [x for x in row if x.isdigit()]

    row1 = files[1].split(' ')
    # keep only values of row that are digits
    distances = [x for x in row1 if x.isdigit()]

    combined = zip(times, distances)
    return combined


def compute_wins(time, distance):
    wins = 0
    for i in range(0, time):
        remaining_time = time - i
        my_distance = i*remaining_time
        if my_distance > distance:
            wins += 1
    return wins


def open_door_6():
    files = read_txt_file('door_6_1')

    t_d = get_times(files)

    total_wins = 1
    for time, distance in t_d:
        wins = compute_wins(int(time), int(distance))
        total_wins *= wins

    # compute product of all elements in total wins
    print('product of wins: ', total_wins)



if __name__ == '__main__':
    open_door_6()