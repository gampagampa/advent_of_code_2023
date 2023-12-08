from main import read_txt_file

order = 'A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2'

#map_ = {'A': '13', 'K': '12', 'Q': '11', 'J': '10', 'T': '09', '9': '08', '8': '07', '7': '06', '6': '05', '5': '04', '4': '03', '3': '02', '2': '01'}
map_ = {'A': '13', 'K': '12', 'Q': '11', 'J': '00', 'T': '09', '9': '08', '8': '07', '7': '06', '6': '05', '5': '04', '4': '03', '3': '02', '2': '01'}

def get_prefix(one_count, two_count, three_count, four_count, five_count):
    if five_count == 1:
        return '50'
    elif four_count == 1:
        return '40'
    elif three_count == 1 and two_count == 1:
        return '32'
    elif three_count == 1:
        return '30'
    elif two_count == 2:
        return '22'
    elif two_count == 1:
        return '20'
    elif one_count == 5:
        return '10'


def get_postfix(cards):
    postfix_string = ''
    for card in cards:
        postfix_string += map_[card]
    return postfix_string


def get_strength(cards):
    count_dict = {}
    temp_card = cards.replace('J','')
    # count J in temp_card
    j_count = len(cards) - len(temp_card)

    for card in temp_card:
        if card in count_dict:
            count_dict[card] += 1
        else:
            count_dict[card] = 1

    duplicates = {key: value for key, value in count_dict.items() if value > 0}
    # count how often two occurs in duplicates as a value
    one_count = list(duplicates.values()).count(1)
    two_count = list(duplicates.values()).count(2)
    three_count = list(duplicates.values()).count(3)
    four_count = list(duplicates.values()).count(4)
    five_count = list(duplicates.values()).count(5)

    if j_count == 5:
        five_count = 1

    if j_count > 0:
        if four_count > 0:
            four_count = 0
            five_count = 1
        elif three_count > 0:
            three_count = 0
            if j_count == 1:
                four_count = 1
            else:
                five_count = 1
        elif two_count > 0:
            two_count -= 1
            if j_count == 1:
                three_count = 1
            elif j_count == 2:
                four_count = 1
            else:
                five_count = 1
        elif one_count > 0:
            if j_count == 1:
                two_count = 1
            elif j_count == 2:
                three_count = 1
            elif j_count == 3:
                four_count = 1
            else:
                five_count = 1


    prefix = get_prefix(one_count, two_count, three_count, four_count, five_count)
    postfix = get_postfix(cards)
    return prefix + postfix

def open_door_7():
    files = read_txt_file('door_7_1')

    cards_dict = {}
    for file in files:
        cards = file.split(' ')[0]
        bid = file.split(' ')[1]
        strenght_val = get_strength(cards)

        cards_dict[bid] = strenght_val

    # sort cards_dict by value
    sorted_cards_dict = {k: v for k, v in sorted(cards_dict.items(), key=lambda item: item[1])}

    total_val = 0
    i = 1
    for key, value in sorted_cards_dict.items():
        total_val += int(key) * i
        i += 1

    print(total_val)

if __name__ == '__main__':
    print('Door 7 is open!')
    open_door_7()
