import random
import matplotlib.pyplot as plt
import numpy as np

class cards(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


ace = cards('ace', 11)
two = cards('two', 2)
three = cards('three', 3)
four = cards('four', 4)
five = cards('five', 5)
six = cards('six', 6)
seven = cards('seven', 7)
eight = cards('eight', 8)
nine = cards('nine', 9)
ten = cards('ten', 10)
jack = cards('jack', 10)
queen = cards('queen', 10)
king = cards('king', 10)

deck = (
    [ace] * 4 +
    [two] * 4 +
    [three] * 4 +
    [four] * 4 +
    [five] * 4 +
    [six] * 4 +
    [seven] * 4 +
    [eight] * 4 +
    [nine] * 4 +
    [ten] * 4 +
    [jack] * 4 +
    [queen] * 4 +
    [king] * 4
)

def new_shoe(number_of_decks):

    shoe = deck * number_of_decks
    random.shuffle(shoe)

    return shoe

def hand_totals(hand):


    total = sum(card.value for card in hand)
    aces = sum(card is ace for card in hand)

    totals = [total]

    # Turn aces from 11 into 1 where possible
    for i in range(aces):
        total -= 10
        totals.append(total)

    return sorted(set(totals))

def best_total(hand):

    totals = hand_totals(hand)

    if any(a for a in totals if a <= 21):
        best_total = max(a for a in totals if a <= 21)
        return best_total
        
    else:
        return min(totals)

def is_soft(hand):

    totals = hand_totals(hand)

    return any(
        total <= 21 and total != min(totals) # As if there is the option for more than one total than there must be an ace, and it is soft if tne greater value is less than or equal to 21
        for total in totals
    )

def play_hand(shoe, bankroll, bet=1):

    player = [shoe.pop(), shoe.pop()]
    dealer = [shoe.pop(), shoe.pop()]

    player_up = dealer[0]

    player_blackjack = (len(player) == 2 and best_total(player) == 21) # Hence player has blackjack
    dealer_blackjack = (len(dealer) == 2 and best_total(dealer) == 21) # Hence dealer has blackjack

    if player_blackjack and dealer_blackjack:
        return bankroll # As both blackjack, bankroll is unaffected

    if player_blackjack:
        return bankroll + 1.5*bet # As only player has blackjack, return 1.5x bet

    if dealer_blackjack:
        return bankroll - bet # As only dealer has blackjack, player will lose, even if they eventually get 21

    while True:

        totals = hand_totals(player)
        current_total = best_total(player)
        dealer_value = player_up.value

        # If player has busted, lose immediately
        if current_total > 21:
            return bankroll - bet

        if is_soft(player): # Hand is soft

            if 13 <= current_total <= 14 and 5 <= dealer_value <= 6:
                # DOUBLE
                bankroll -= bet # Better to have doubling in the function as avoids having to use global variables, same with standing and hitting
                bet *= 2

                player.append(shoe.pop())

                if best_total(player) > 21:
                    return bankroll - bet

                break

            elif 13 <= current_total <= 14:
                player.append(shoe.pop())

            elif 15 <= current_total <= 16 and 4 <= dealer_value <= 6:
                # DOUBLE
                bankroll -= bet
                bet *= 2

                player.append(shoe.pop())

                if best_total(player) > 21:
                    return bankroll - bet

                break

            elif 15 <= current_total <= 16:
                player.append(shoe.pop())

            elif current_total == 17 and 3 <= dealer_value <= 6:
                # DOUBLE
                bankroll -= bet
                bet *= 2

                player.append(shoe.pop())

                if best_total(player) > 21:
                    return bankroll - bet

                break

            elif current_total == 17:
                player.append(shoe.pop())

            elif current_total == 18 and 2 <= dealer_value <= 6:
                # DOUBLE
                bankroll -= bet
                bet *= 2

                player.append(shoe.pop())

                if best_total(player) > 21:
                    return bankroll - bet

                break

            elif current_total == 18 and 7 <= dealer_value <= 8:
                player.append(shoe.pop())

            elif current_total == 18:
                # STAND
                break

            elif current_total == 19 and dealer_value == 6:
                # DOUBLE
                bankroll -= bet
                bet *= 2

                player.append(shoe.pop())

                if best_total(player) > 21:
                    return bankroll - bet

                break

            else:
                # STAND
                break

        else: # Hand is hard

            if current_total <= 8:
                # HIT
                player.append(shoe.pop())

            elif current_total == 9 and 3 <= dealer_value <= 6:
                # DOUBLE
                bankroll -= bet
                bet *= 2

                player.append(shoe.pop())

                if best_total(player) > 21:
                    return bankroll - bet

                break

            elif current_total == 9:
                # HIT
                player.append(shoe.pop())

            elif current_total == 10 and 2 <= dealer_value <= 9:
                # DOUBLE
                bankroll -= bet
                bet *= 2

                player.append(shoe.pop())

                if best_total(player) > 21:
                    return bankroll - bet

                break

            elif current_total == 10:
                # HIT
                player.append(shoe.pop())

            elif current_total == 11:
                # DOUBLE
                bankroll -= bet
                bet *= 2

                player.append(shoe.pop())

                if best_total(player) > 21:
                    return bankroll - bet

                break

            elif current_total == 12 and 4 <= dealer_value <= 6:
                # STAND
                break

            elif current_total == 12:
                # HIT
                player.append(shoe.pop())

            elif 13 <= current_total <= 16 and dealer_value <= 6:
                # STAND
                break

            elif 13 <= current_total <= 16:
                # HIT
                player.append(shoe.pop())

            else:
                # 17+
                break

    while True: # Now what the dealer has to do

        dealer_total = best_total(dealer)

        # Dealer busts
        if dealer_total > 21:
            return bankroll + bet

        # Dealer stands on 17+
        if dealer_total >= 17:
            break

        # Dealer hits
        dealer.append(shoe.pop())

    player_total = best_total(player) # Comparing hands
    dealer_total = best_total(dealer)

    if player_total > dealer_total:
        bankroll += bet

    elif player_total < dealer_total:
        bankroll -= bet

    # Otherwise even so nothing happens

    return bankroll

def simulation(number_of_hands=1000, starting_money=100, number_of_decks=6, cut_cards=52):

    bankroll = starting_money
    shoe = new_shoe(number_of_decks)

    hands_played = 0

    for hand_number in range(number_of_hands):

        # Bankrupt
        if bankroll <= 0:
            break

        # Re-shuffle when reaching the cut-card point
        if len(shoe) < cut_cards:
            shoe = new_shoe(number_of_decks)

        bankroll = play_hand(shoe, bankroll, bet=1)

        hands_played += 1

    busted = bankroll <= 0

    return {
        "final_money": bankroll,
        "profit": bankroll - starting_money,
        "bust": busted,
        "hands": hands_played
    }

def run_simulations(number_of_simulations=100000, number_of_hands=1000):

    profits = []

    for i in range(number_of_simulations):

        result = simulation(
            number_of_hands=number_of_hands,
            starting_money=100,
            number_of_decks=6,
            cut_cards=52
        )

        profits.append(result["profit"])

    return profits

profits = run_simulations(100000, 1000)
plt.hist(profits, bins=50)
plt.xlabel("Profit / Loss")
plt.ylabel("Number of simulations")
plt.title("Distribution of Profit/Loss after 1,000 Blackjack Hands")
plt.show()

print("Mean profit:", np.mean(profits))
print("Median profit:", np.median(profits))
print("Standard deviation:", np.std(profits))
print("Best result:", max(profits))
print("Worst result:", min(profits))
print("Probability of profit:", np.mean(np.array(profits) > 0))
print("Probability of loss:", np.mean(np.array(profits) < 0))
print("Probability of bust:", np.mean(np.array(profits) == -100))
