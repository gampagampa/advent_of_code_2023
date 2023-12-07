from main import read_txt_file


def open_door_4():
    files = read_txt_file('door_4_1')

    all_points = 0
    for file in files:
        points = 0
        first_match = False
        split = file.split(':')

        game_nr = int(split[0].split(' ')[-1])
        game = split[1]

        all_cards = game.split('|')
        winning_cards = all_cards[0].split(' ')
        winning_cards = [int(i) for i in winning_cards if i != '']

        my_cards = all_cards[1].split(' ')
        my_cards = [int(i) for i in my_cards if i != '']

        for card in my_cards:
            if card in winning_cards and not first_match:
                points = 1
                first_match = True
            elif card in winning_cards and first_match:
                points *=2

        all_points += points

    print(all_points)


if __name__ == '__main__':
    open_door_4()
