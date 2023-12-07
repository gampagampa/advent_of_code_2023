from main import read_txt_file


def get_seeds(files):
    seeds = files[0].split(': ')[1].split(' ')
    seeds = [int(i) for i in seeds]

    return seeds


def get_x_to_y_map(files, x_map):
    x_to_y_map = []
    start = 0

    found = False
    for num, file in enumerate(files):
        if file.startswith(x_map):
            start = num+1
            found = True
        elif found and file == '' or num == len(files)-1:
            end = num
            break

    for i in range(start, end):
        first_row = files[i].split(' ')
        map_to = int(first_row[0])
        map_from_start = int(first_row[1])
        step = int(first_row[2])
        map_from_end = map_from_start + step -1

        diff = map_from_start - map_to
        x_to_y_map.append({'map_from_start': map_from_start, 'map_from_end': map_from_end, 'diff': diff})

    return x_to_y_map


def do_map(seed, seed_to_soil_map):
    for map in seed_to_soil_map:
        if map['map_from_start'] <= seed <= map['map_from_end']:
            seed = seed - map['diff']
            break

    return seed

def open_door_5():
    files = read_txt_file('door_5_1')

    seeds_to_be_planted = get_seeds(files)

    seed_to_soil_map = get_x_to_y_map(files, 'seed-to-soil map:')
    soil_to_fert_map = get_x_to_y_map(files, 'soil-to-fertilizer map:')
    fert_to_water_map = get_x_to_y_map(files, 'fertilizer-to-water map:')
    water_to_light_map = get_x_to_y_map(files, 'water-to-light map:')
    light_to_temp_map = get_x_to_y_map(files, 'light-to-temperature map:')
    temp_to_humidity_map = get_x_to_y_map(files, 'temperature-to-humidity map:')
    humidity_to_location_map = get_x_to_y_map(files, 'humidity-to-location map:')

    location_list = []
    for seed in seeds_to_be_planted:
        val = do_map(seed, seed_to_soil_map)
        val = do_map(val, soil_to_fert_map)
        val = do_map(val, fert_to_water_map)
        val = do_map(val, water_to_light_map)
        val = do_map(val, light_to_temp_map)
        val = do_map(val, temp_to_humidity_map)
        val = do_map(val, humidity_to_location_map)

        location_list.append(val)

    print('lowest location number: ', min(location_list))


if __name__ == '__main__':
    open_door_5()
