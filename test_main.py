from main import calc_total, conclude_game


def test_calc_total():
    blackjack_hand = ["AC", "10H"]
    assert calc_total(blackjack_hand) == 21

    pair_sixes = ["6C", "6D"]
    assert calc_total(pair_sixes) == 12

    good_hand = ["9D", "JS"]
    assert calc_total(good_hand) == 19

    low_hand = ["3D", "2D"]
    assert calc_total(low_hand) == 5

    five_of_a_kind = ["5D", "2C", "2S", "4H", "7D"]
    assert calc_total(five_of_a_kind) == 20

    busted_hand = ["QS", "6D", "8H"]
    assert calc_total(busted_hand) == 24

    multiple_aces = ["AH", "7D", "6S", "AC"]
    assert calc_total(multiple_aces) == 15

    multiple_aces_eleven = ["AH", "7D", "2S", "AC"]
    assert calc_total(multiple_aces_eleven) == 21


def test_conclude_game():
    blackjack_hand = ["AC", "10H"]
    good_hand = ["9D", "JS"]
    five_of_a_kind = ["5D", "2C", "2S", "4H", "7D"]
    busted_hand = ["QS", "6D", "8H"]
    pair_sixes = ["6C", "6D"]
    multiple_aces_eleven = ["AH", "7D", "2S", "AC"]

    assert conclude_game(blackjack_hand, good_hand) == "Player"
    assert conclude_game(good_hand, five_of_a_kind) == "Dealer"
    assert conclude_game(busted_hand, pair_sixes) == "Dealer"
    assert conclude_game(multiple_aces_eleven, good_hand) == "Player"
