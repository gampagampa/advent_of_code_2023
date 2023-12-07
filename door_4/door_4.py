from main import read_txt_file


def get_winning_and_my_cards(split):
    game = split[1]

    all_cards = game.split('|')
    winning_cards = all_cards[0].split(' ')
    winning_cards = [int(i) for i in winning_cards if i != '']

    my_cards = all_cards[1].split(' ')
    my_cards = [int(i) for i in my_cards if i != '']

    return winning_cards, my_cards


def create_copies(game_nr, matches, cards_dict):
    for i in range(game_nr+1, game_nr + 1 + matches):
        if i in cards_dict:
            cards_dict[i] += 1 + cards_dict[game_nr]
        else:
            cards_dict[i] = 1 + cards_dict[game_nr]



def count_matches(my_cards, winning_cards, matches):
    for card in my_cards:
        if card in winning_cards:
            matches += 1
    return matches


def open_door_4():
    files = read_txt_file('door_4_2')

    all_points = 0
    cards_dict = {1: 0}
    for file in files:
        matches = 0
        split = file.split(':')

        game_nr = int(split[0].split(' ')[-1])

        winning_cards, my_cards = get_winning_and_my_cards(split)

        # count my cards in winning cards
        matches = count_matches(my_cards, winning_cards, matches)
        if game_nr not in cards_dict:
            cards_dict[game_nr] = 0

        create_copies(game_nr, matches, cards_dict)


    # sum all values of dict
    for key, value in cards_dict.items():
        all_points += value+1

    print('all points: ', all_points)


if __name__ == '__main__':
    open_door_4()
