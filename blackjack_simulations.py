import random
import matplotlib.pyplot as plt
import numpy as np
import os

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
        total <= 21 and total != min(totals) # As if there is the option for more than one total than there must be an ace, and it is soft if the greater value is less than or equal to 21
        for total in totals
    )

def can_split(hand):

    return (len(hand) == 2 and hand[0].value == hand[1].value) # Can only split when you have two cards in your hand and when the value of the cards is the same. Does allow for Queen-10 splitting, as both are valued at 10.

def should_split(hand, dealer_upcard):

    if not can_split(hand):
        return False

    dealer_value = dealer_upcard.value # Here we are calling the delaer up  card value as dealer_value so all face cards and 10s are looked at by the same case
    player_value = hand[0].value # Due to the fact that we can only split pairs of equal values, the player_value is the value of each card

    if hand[0] == ace and hand[1] == ace: # Always split Aces
        return True

    if player_value == 10: # Never split 10s
        return False

    if player_value == 9: # We should split 9s if the upcard is one of the following
        return dealer_value in [2, 3, 4, 5, 6, 8, 9]

    if player_value == 8: # Always split 8s
        return True

    if player_value == 7: # Should split 7s against dealers 2 to 7
        return 2 <= dealer_value <= 7

    if player_value == 6: # Here DAS is allowed so we include splitting after 2s, as well as the rest
        return 2 <= dealer_value <= 6

    if player_value == 5: # Never split 5s
        return False

    if player_value == 4: # As DAS is allowed, split against 5 and 6
        return dealer_value in [5, 6]

    if player_value in [2, 3]: # 2s and 3s have the same splits, where against 2 to 7 with DAS
        return 2 <= dealer_value <= 7

    return False # Otherwise do not split

def play_player_hand(shoe, hand, dealer_up, bankroll, hand_bet, committed):

    if(should_split(hand, dealer_up) and bankroll - committed >= hand_bet): # Check that we can both split and have the bankroll to facilitate it

        committed += hand_bet # Placing a new bet for the new hand
        
        hand1 = [hand[0]] # Split the original pair into two seperate hands
        hand2 = [hand[1]]

        hand1.append(shoe.pop()) # Deal a card to each hand 
        hand2.append(shoe.pop())

        if hand[0] == ace: # When splitting aces you receive one card and are forced to stand, cannot resplit
            return [(hand1, hand_bet), (hand2, hand_bet)], committed
            
        hands1, committed = play_player_hand(shoe, hand1, dealer_up, bankroll, hand_bet, committed) # Play hand1 recursively
        hands2, committed = play_player_hand(shoe, hand2, dealer_up, bankroll, hand_bet, committed) # Play hand2 recursively

        return hands1 + hands2, committed
    
    while True:

        current_total = best_total(hand)
        dealer_value = dealer_up.value

        if current_total > 21:
            return [(hand, hand_bet)], committed # Busts

        if is_soft(hand): # If hand is soft, do the following

            if 13 <= current_total <= 14:

                if (5 <= dealer_value <= 6 and bankroll - committed >= hand_bet):
                    committed += hand_bet # Double
                    hand_bet *= 2
                    hand.append(shoe.pop())
                    return [(hand, hand_bet)], committed

                else:
                    hand.append(shoe.pop()) # Hit as not enough bankroll to double


            elif 15 <= current_total <= 16:

                if (
                    4 <= dealer_value <= 6 and bankroll - committed >= hand_bet):
                    committed += hand_bet # Double
                    hand_bet *= 2
                    hand.append(shoe.pop())
                    return [(hand, hand_bet)], committed

                else:
                    hand.append(shoe.pop()) # Hit as not enough bankroll to double


            elif current_total == 17:

                if (3 <= dealer_value <= 6 and bankroll - committed >= hand_bet):
                    committed += hand_bet # Double
                    hand_bet *= 2
                    hand.append(shoe.pop())
                    return [(hand, hand_bet)], committed

                else:
                    hand.append(shoe.pop()) # Hit as not enough bankroll to double


            elif current_total == 18:

                if (2 <= dealer_value <= 6 and bankroll - committed >= hand_bet):
                    committed += hand_bet # Double
                    hand_bet *= 2
                    hand.append(shoe.pop())
                    return [(hand, hand_bet)], committed

                elif 7 <= dealer_value <= 8:
                    hand.append(shoe.pop()) # Hit

                else:
                    return [(hand, hand_bet)], committed # Stand (as not enough bankroll to double)


            elif current_total == 19:

                if (dealer_value == 6 and bankroll - committed >= hand_bet):
                    committed += hand_bet # Double
                    hand_bet *= 2
                    hand.append(shoe.pop())

                return [(hand, hand_bet)], committed # Stand as not enough bankroll to double


            else:
                return [(hand, hand_bet)], committed # Stand

        else: # If hand is hard, do the following

            if current_total <= 8: # Hit
                hand.append(shoe.pop())


            elif current_total == 9:

                if (3 <= dealer_value <= 6 and bankroll - committed >= hand_bet):
                    committed += hand_bet # Double
                    hand_bet *= 2
                    hand.append(shoe.pop())
                    return [(hand, hand_bet)], committed

                else:
                    hand.append(shoe.pop()) # Hit (as not enough bankroll to double)


            elif current_total == 10:

                if (2 <= dealer_value <= 9 and bankroll - committed >= hand_bet):
                    committed += hand_bet # Double
                    hand_bet *= 2
                    hand.append(shoe.pop())
                    return [(hand, hand_bet)], committed

                else:
                    hand.append(shoe.pop()) # Hit (as not enough bankroll to double)


            elif current_total == 11:

                if bankroll - committed >= hand_bet: # Double
                    committed += hand_bet
                    hand_bet *= 2
                    hand.append(shoe.pop())
                    return [(hand, hand_bet)], committed

                else:
                    hand.append(shoe.pop()) # Hit (as not enough bankroll to double)


            elif current_total == 12:

                if 4 <= dealer_value <= 6:
                    return [(hand, hand_bet)], committed

                hand.append(shoe.pop()) # Hit


            elif 13 <= current_total <= 16:

                if dealer_value <= 6:
                    return [(hand, hand_bet)], committed

                hand.append(shoe.pop()) # Hit


            else:
                return [(hand, hand_bet)], committed # Stand

def play_hand(shoe, bankroll, bet=1):

    if bankroll < bet: # Need to have the money left to bet
        return bankroll

    committed = bet

    player = [shoe.pop(), shoe.pop()]
    dealer = [shoe.pop(), shoe.pop()]

    dealer_up = dealer[0]

    player_blackjack = (len(player) == 2 and best_total(player) == 21) # Hence player has blackjack
    dealer_blackjack = (len(dealer) == 2 and best_total(dealer) == 21) # Hence dealer has blackjack

    if player_blackjack and dealer_blackjack:
        return bankroll # As both blackjack, bankroll is unaffected

    if player_blackjack:
        return bankroll + 1.5*bet # As only player has blackjack, return 1.5x bet

    if dealer_blackjack:
        return bankroll - bet # As only dealer has blackjack, player will lose, even if they eventually get 21

    final_hands, committed = play_player_hand(shoe, player, dealer_up, bankroll, bet, committed) # Player plays, splits can only happen now so if split Aces leads to 21, will just pay out 1:1

    while True: # Now dealer plays

        dealer_total = best_total(dealer)

        # Dealer busts
        if dealer_total > 21:
            break

        # Dealer stands on 17+
        if dealer_total >= 17:
            break

        # Dealer hits
        dealer.append(shoe.pop())

    for hand, hand_bet in final_hands: # Compare dealer's hand against however mand hands the player has due to splits

        player_total = best_total(hand)
        dealer_total = best_total(dealer)

        # Player busts
        if player_total > 21:
            bankroll -= hand_bet

        # Dealer busts
        elif dealer_total > 21:
            bankroll += hand_bet

        # Player wins
        elif player_total > dealer_total:
            bankroll += hand_bet

        # Player loses
        elif player_total < dealer_total:
            bankroll -= hand_bet

        # Draw: bankroll unchanged

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
        if len(shoe) < number_of_decks*52 - cut_cards:
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

profits = run_simulations(1000, 100) # Simulating 1000, 100 length hands
plt.hist(profits, bins=50)
plt.xlabel("Profit / Loss")
plt.ylabel("Number of simulations")
plt.title("Distribution of Profit/Loss after 100 Blackjack Hands")
os.makedirs("images", exist_ok=True)
plt.savefig("images/profit_distribution_1000_100.png", dpi=300, bbox_inches="tight")
plt.show()

print("Mean profit:", np.mean(profits))
print("Median profit:", np.median(profits))
print("Standard deviation:", np.std(profits))
print("Best result:", max(profits))
print("Worst result:", min(profits))
print("Probability of profit:", np.mean(np.array(profits) > 0))
print("Probability of loss:", np.mean(np.array(profits) < 0))
print("Probability of bust:", np.mean(np.array(profits) == -100))

profits = run_simulations(10000, 1000) # Simulating 10000, 1000 length hands
plt.hist(profits, bins=50)
plt.xlabel("Profit / Loss")
plt.ylabel("Number of simulations")
plt.title("Distribution of Profit/Loss after 1,000 Blackjack Hands")
plt.savefig("images/profit_distribution_1000_1000.png", dpi=300, bbox_inches="tight")
plt.show()

print("Mean profit:", np.mean(profits))
print("Median profit:", np.median(profits))
print("Standard deviation:", np.std(profits))
print("Best result:", max(profits))
print("Worst result:", min(profits))
print("Probability of profit:", np.mean(np.array(profits) > 0))
print("Probability of loss:", np.mean(np.array(profits) < 0))
print("Probability of bust:", np.mean(np.array(profits) == -100))

profits = run_simulations(100000, 1000) # Simulating 100000, 1000 length hands
plt.hist(profits, bins=50)
plt.xlabel("Profit / Loss")
plt.ylabel("Number of simulations")
plt.title("Distribution of Profit/Loss after 1,000 Blackjack Hands")
plt.savefig("images/profit_distribution_100000_1000).png", dpi=300, bbox_inches="tight")
plt.show()

print("Mean profit:", np.mean(profits))
print("Median profit:", np.median(profits))
print("Standard deviation:", np.std(profits))
print("Best result:", max(profits))
print("Worst result:", min(profits))
print("Probability of profit:", np.mean(np.array(profits) > 0))
print("Probability of loss:", np.mean(np.array(profits) < 0))
print("Probability of bust:", np.mean(np.array(profits) == -100))
