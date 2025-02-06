import random
import sys


def initialise_deck():
    # TODO: reference files for their respective images (card as the key)
    # ordered_deck_dictionary = {
    #     0: "AD",
    #     1: "2D",
    #     2: "3D",
    #     3: "4D",
    #     4: "5D",
    #     5: "6D",
    #     6: "7D",
    #     7: "8D",
    #     8: "9D",
    #     9: "10D",
    #     10: "JD",
    #     11: "QD",
    #     12: "KD",
    #     13: "AH",
    #     14: "2H",
    #     15: "3H",
    #     16: "4H",
    #     17: "5H",
    #     18: "6H",
    #     19: "7H",
    #     20: "8H",
    #     21: "9H",
    #     22: "10H",
    #     23: "JH",
    #     24: "QH",
    #     25: "KH",
    #     26: "AC",
    #     27: "2C",
    #     28: "3C",
    #     29: "4C",
    #     30: "5C",
    #     31: "6C",
    #     32: "7C",
    #     33: "8C",
    #     34: "9C",
    #     35: "10C",
    #     36: "JC",
    #     37: "QC",
    #     38: "KC",
    #     39: "AS",
    #     40: "2S",
    #     41: "3S",
    #     42: "4S",
    #     43: "5S",
    #     44: "6S",
    #     45: "7S",
    #     46: "8S",
    #     47: "9S",
    #     48: "10S",
    #     49: "JS",
    #     50: "QS",
    #     51: "KS"
    # }

    return [
        "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD",
        "QD", "KD", "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H",
        "10H", "JH", "QH", "KH", "AC", "2C", "3C", "4C", "5C", "6C", "7C",
        "8C", "9C", "10C", "JC", "QC", "KC", "AS", "2S", "3S", "4S", "5S",
        "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS"
    ]


def card_value(card):
    match (card):
        case "A":
            return 1
        case "J" | "Q" | "K":
            return 10
        case _:
            return int(card)


def calc_total(hand):
    card_values = list(map(lambda card: card_value(card[:-1]), hand))
    card_values.sort()
    total = sum(card_values)

    if total <= 11 and 1 in card_values:
        # Only one ace in a hand can ever be worth 11
        card_values.remove(1)
        card_values.append(11)
        return sum(card_values)
    else:
        return total


def deal_initial_hand(deck):
    player_hand, dealer_hand, new_deck = [deck[0],
                                          deck[2]], [deck[1],
                                                     deck[3]], deck[4:]
    player_total = calc_total(player_hand)
    print(f"Dealer hand: {dealer_hand[0]} **")
    print(
        f"Player hand: {player_hand[0]} {player_hand[1]} which is {player_total}"
    )
    return [player_hand], dealer_hand, new_deck


def draw_next_card(deck):
    return deck[0], deck[1:]


def check_if_player_is_alive(hands):
    for hand in hands:
        value = calc_total(hand)

        if value <= 21:
            return True

    return False


def conclude_game(player_hands, dealer_hand):
    dealer_total = calc_total(dealer_hand)
    results = []

    for hand in player_hands:
        player_total = calc_total(hand)
        hand_index = player_hands.index(hand) + 1

        if player_total < 22 and (player_total > dealer_total
                                  or dealer_total > 21):
            print(f"Hand {hand_index} ({' '.join(hand)}): Win")
            results.append("Player")
        elif player_total < 22 and player_total == dealer_total:
            print(f"Hand {hand_index} ({' '.join(hand)}): Draw")
            results.append("Draw")
        else:
            print(f"Hand {hand_index} ({' '.join(hand)}): Lose")
            results.append("Dealer")

    return results


def split_hand(hands, index, deck):
    hand = hands[index]
    next_card, deck = draw_next_card(deck)
    second_next_card, deck = draw_next_card(deck)

    print(f"You drew a {next_card} and {second_next_card}")

    hands.remove(hand)
    hands.insert(index, [hand[0], next_card])
    hands.insert(index + 1, [hand[1], second_next_card])

    print(
        f"Resulting in two hands: {' '.join(hands[index])} and {' '.join(hands[index + 1])}"
    )

    return hands, deck


def play_game(deck_in_play=[]):
    # This is to maintain the current deck
    if deck_in_play == []:
        deck_in_play = initialise_deck()
        random.shuffle(deck_in_play)

    # TODO: add in betting
    early_conclusion = False
    player_hands, dealer_hand, deck_in_play = deal_initial_hand(deck_in_play)

    # Only offer insurance sidebet on the upfaced (first) card
    if "A" in dealer_hand[0]:
        insurance = input("Do you want to buy insurance? (y/n)")

        if insurance == "y":
            print("Increase bet by 50%")

        # dealer_hand[1][:-1] ignores the suit on the second card
        if dealer_hand[1][:-1] in ["10", "J", "Q", "K"]:
            print(f"Dealer has blackjack {' '.join(dealer_hand)}")
            early_conclusion = True

    # Player currently only has one hand here
    if calc_total(player_hands[0] == 21):
        # This is so that the dealer doesn't hit
        print(f"Player has blackjack {' '.join(player_hands[0])}")
        early_conclusion = True

    hand_in_play = 0

    # Let the user take their turn
    while hand_in_play < len(player_hands) and not early_conclusion:
        player_total = calc_total(player_hands[hand_in_play])
        hitable = player_total < 21

        while hitable:
            doublable = len(player_hands[hand_in_play]) == 2
            splitable = len(player_hands[hand_in_play]) == 2 and player_hands[
                hand_in_play][0][:-1] == player_hands[hand_in_play][1][:-1]

            player_total = calc_total(player_hands[hand_in_play])
            print(
                f"Your cards are: {' '.join(player_hands[hand_in_play])} which is {player_total}"
            )

            action = input(
                f"{'Double, ' if doublable else ''}{'Split, ' if splitable else ''}Hit or Stand?\n"
            ).lower()

            if action in ["hit", "h", "double", "d"]:
                next_card, deck_in_play = draw_next_card(deck_in_play)
                print(f"You get a {next_card}")
                player_hands[hand_in_play].append(next_card)
                player_total = calc_total(player_hands[hand_in_play])
            elif action in ["split"]:
                player_hands, deck_in_play = split_hand(
                    player_hands, hand_in_play, deck_in_play)

            # Subsequent hits are only available when hitting (not doubling)
            hitable = player_total < 21 and action in ["hit", "h", "split"]

        hand_in_play = hand_in_play + 1

    hand_still_in_play = check_if_player_is_alive(player_hands)

    # Let the dealer play if the player hasn't bust
    if hand_still_in_play and not early_conclusion:
        # Dealer hits on soft 17
        dealer_total = calc_total(dealer_hand)
        dealer_first_card = dealer_hand[0][:-1]
        dealer_second_card = dealer_hand[1][:-1]
        is_soft_17 = (dealer_first_card == "6" and dealer_second_card
                      == "A") or (dealer_first_card == "A"
                                  and dealer_second_card == "6")

        dealer_hitable = dealer_total < 17 or is_soft_17
        print(f"Dealer's cards are {dealer_hand[0]} {dealer_hand[1]}")

        while dealer_hitable:
            next_card, deck_in_play = draw_next_card(deck_in_play)
            print(f"Dealer's next card is {next_card}")
            dealer_hand.append(next_card)
            dealer_total = calc_total(dealer_hand)

            print(
                f"Dealer has: {' '.join(dealer_hand)} which is {dealer_total}")
            dealer_hitable = dealer_total < 17

    conclude_game(player_hands, dealer_hand)
    deck_in_play = deck_in_play + [
        # Flatten player_hands
        card for hand in player_hands for card in hand
    ] + dealer_hand
    answer = input("Play again? (y/n)\n")

    if answer == "y":
        play_game(deck_in_play)
    else:
        print("Thanks for playing")


# We don't want to run the entire progran dring tests
# if "pytest" not in sys.modules:
#     play_game()
