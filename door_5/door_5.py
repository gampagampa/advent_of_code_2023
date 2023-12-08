import tqdm

from main import read_txt_file
from functools import partial

def get_seeds(files):
    seeds = files[0].split(': ')[1].split(' ')
    seeds = [int(i) for i in seeds]

    seeds_touple = [(seeds[i],seeds[i] + seeds[i+1]) for i in range(0, len(seeds), 2)]
    return seeds_touple


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


def do_reverse_map(seed, seed_to_soil_map):
    for map in seed_to_soil_map:
        if map['map_to_start'] <= seed <= map['map_to_end']:
            seed = seed + map['diff']
            break

    return seed

def do_map(seed, seed_to_soil_map):
    for map in seed_to_soil_map:
        if map['map_from_start'] <= seed <= map['map_from_end']:
            seed = seed - map['diff']
            break

    return seed


def min_val(seeds_to_be_planted, seed_to_soil_map, soil_to_fert_map, fert_to_water_map, water_to_light_map,
            light_to_temp_map, temp_to_humidity_map, humidity_to_location_map):
    lowest_val = 100000000000000000

    seed_start = seeds_to_be_planted[0]
    seed_end = seed_start + seeds_to_be_planted[1]
    for seed in range(seed_start, seed_end):
        val = do_map(seed, seed_to_soil_map)
        val = do_map(val, soil_to_fert_map)
        val = do_map(val, fert_to_water_map)
        val = do_map(val, water_to_light_map)
        val = do_map(val, light_to_temp_map)
        val = do_map(val, temp_to_humidity_map)
        val = do_map(val, humidity_to_location_map)

        if val < lowest_val:
            lowest_val = val
    return lowest_val


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

    # do multiprocessing of seeds_to_be_planted
    import multiprocessing
    with multiprocessing.Pool(processes=5) as pool:
        g = partial(min_val, seed_to_soil_map=seed_to_soil_map, soil_to_fert_map=soil_to_fert_map
                    , fert_to_water_map=fert_to_water_map, water_to_light_map=water_to_light_map
                    , light_to_temp_map=light_to_temp_map, temp_to_humidity_map=temp_to_humidity_map
                    , humidity_to_location_map=humidity_to_location_map)
        results = pool.map(g, seeds_to_be_planted)

    lowest_val = min(results)
    print('lowest location number: ', lowest_val)


def check_found(val, seeds_to_be_planted):
    for seed_range in seeds_to_be_planted:
        if seed_range[0] <= val <= seed_range[0] + seed_range[1]:
            return True
    return False

def open_door_5_smooth():
    files = read_txt_file('door_5_1')

    seeds_to_be_planted = get_seeds(files)

    seed_to_soil_map = get_x_to_y_map(files, 'seed-to-soil map:')
    soil_to_fert_map = get_x_to_y_map(files, 'soil-to-fertilizer map:')
    fert_to_water_map = get_x_to_y_map(files, 'fertilizer-to-water map:')
    water_to_light_map = get_x_to_y_map(files, 'water-to-light map:')
    light_to_temp_map = get_x_to_y_map(files, 'light-to-temperature map:')
    temp_to_humidity_map = get_x_to_y_map(files, 'temperature-to-humidity map:')
    humidity_to_location_map = get_x_to_y_map(files, 'humidity-to-location map:')

    found = False
    start = 1 # should be 98
    while not found:
        val = do_reverse_map(start, humidity_to_location_map)
        val = do_reverse_map(val, temp_to_humidity_map)
        val = do_reverse_map(val, light_to_temp_map)
        val = do_reverse_map(val, water_to_light_map)
        val = do_reverse_map(val, fert_to_water_map)
        val = do_reverse_map(val, soil_to_fert_map)
        val = do_reverse_map(val, seed_to_soil_map)

        found = check_found(val, seeds_to_be_planted)

        if not found:
            start += 1

        print(start) if start % 1000 == 0 else None

    print('lowest location number: ', start)


def seed_range_split(seed_range, seed_to_soil_map):
    seed_start = seed_range[0]
    seed_end = seed_range[1]

    current_seed_range = [(seed_start, seed_end)]
    s_r_s = []
    for map in seed_to_soil_map:
        map_from_start = map['map_from_start']
        for seed_range in current_seed_range:
            if seed_range[0] < map_from_start < seed_range[1]:
                # remove seed range from current seed range
                current_seed_range.remove(seed_range)
                current_seed_range.append((seed_range[0], map_from_start))
                current_seed_range.append((map_from_start+1, seed_range[1]))

        map_from_end = map['map_from_end']
        for seed_range in current_seed_range:
            if seed_range[0] < map_from_end < seed_range[1]:
                # remove seed range from current seed range
                current_seed_range.remove(seed_range)
                # split seed range
                current_seed_range.append((seed_range[0], map_from_end))
                current_seed_range.append((map_from_end+1, seed_range[1]))
    return current_seed_range






    return s_r_s


def map_seed_range(seed_range, seed_to_soil_map):
    seed_range_s = seed_range[0]
    seed_range_e = seed_range[1]
    for map in seed_to_soil_map:
        if map['map_from_start'] <= seed_range_s <= map['map_from_end'] and map['map_from_start'] <= seed_range_e <= map['map_from_end']:
            seed_range_s = seed_range_s - map['diff']
            seed_range_e = seed_range_e - map['diff']
            break
    return (seed_range_s, seed_range_e)


def do_range_map(seed_ranges, seed_to_soil_map):
    final_seed_ranges = []
    send_back_list = []

    for seed_range in seed_ranges:
        seed_range_splt = seed_range_split(seed_range, seed_to_soil_map)
        final_seed_ranges.extend(seed_range_splt)

    for final_seed_ranges in final_seed_ranges:
        final_seed_ranges = map_seed_range(final_seed_ranges, seed_to_soil_map)
        send_back_list.append(final_seed_ranges)

    return send_back_list


def open_door_5_this_time_rly():
    files = read_txt_file('door_5_1')

    seeds_to_be_planted = get_seeds(files)

    seed_to_soil_map = get_x_to_y_map(files, 'seed-to-soil map:')
    soil_to_fert_map = get_x_to_y_map(files, 'soil-to-fertilizer map:')
    fert_to_water_map = get_x_to_y_map(files, 'fertilizer-to-water map:')
    water_to_light_map = get_x_to_y_map(files, 'water-to-light map:')
    light_to_temp_map = get_x_to_y_map(files, 'light-to-temperature map:')
    temp_to_humidity_map = get_x_to_y_map(files, 'temperature-to-humidity map:')
    humidity_to_location_map = get_x_to_y_map(files, 'humidity-to-location map:')

    min_val = 10000000000
    for seed in tqdm.tqdm(seeds_to_be_planted, total=len(seeds_to_be_planted)):
        range = do_range_map([seed], seed_to_soil_map)
        #print('seed_to_soil_map')
        range = do_range_map(range, soil_to_fert_map)
        #print('soil_to_fert_map')
        range = do_range_map(range, fert_to_water_map)
        #print('fert_to_water_map')
        range = do_range_map(range, water_to_light_map)
        #print('water_to_light_map')
        range = do_range_map(range, light_to_temp_map)
        #print('light_to_temp_map')
        range = do_range_map(range, temp_to_humidity_map)
        #print('temp_to_humidity_map')
        range = do_range_map(range, humidity_to_location_map)
        print('humidity_to_location_map')

        for r in range:
            if r[0] < min_val:
                min_val = r[0]

    # print minimal value of ranges
    print(min_val)


if __name__ == '__main__':
    # open_door_5()
    # open_door_5_smooth()
    open_door_5_this_time_rly()
