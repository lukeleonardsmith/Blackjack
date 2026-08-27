import random

# Cards and values

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

deck = [ace, ace, ace, ace, two, two, two, two, three, three, three, three, four, four, four, four, five, five, five, five, six, six, six, six, seven, seven, seven, seven, eight, eight, eight, eight, nine, nine, nine, nine, ten, ten, ten, ten, jack, jack, jack, jack, queen, queen, queen, queen, king, king, king, king]

def n_deck(n):
    newdeck = []
    for i in range(n):
        newdeck.extend(deck)
    random.shuffle(newdeck)
    return newdeck

def gamestart(m, k, c):
    global decknumbers
    decknumbers = k
    global playingdeck
    playingdeck = n_deck(k)
    global money
    money = m
    global cutcard # How many cards are dealt before we stop.
    cutcard = (k-c)*52
    global cutinfo
    cutinfo = c

def get_total(hand):
    total = [0]
    for card in hand:
        length_total = len(total)

        if card != ace:
            for i in range(length_total):
                total[i] += card.value
        else:
            for i in range(length_total):
                total[i] += 1
                total.append(total[i] + 10)

    return list(set(total))
    
def roundstart(b):
    global playerhands
    global dealerhand
    global dealertotal
    global bet
    global playingdeck

    dealerhand = []
    dealertotal = [0]
    bet = b

    if len(playingdeck) < cutcard:
        print('We have reached the cutcard. Now the playing deck is reset.')
        playingdeck = n_deck(decknumbers)
        gamestart(money, decknumbers, cutinfo)
        return

    print('You have: ' + str(money) + ' money left.')

    if money < bet:
        print('You do not have enough money to bet this much.')
        return

    playerhands = [{"cards": [], "bet": bet, "finished": False, "split_aces": False, "from_split": False}] # The player starts with one hand

    playersetup()
    dealersetup()
    player_move(0) # Start playing

def deal_card_to_player(hand_index):

    selectedcard = playingdeck.pop()
    playerhands[hand_index]["cards"].append(selectedcard)

    print('You have been dealt: ' + str(selectedcard.name))

    playerhands[hand_index]["total"] = get_total(playerhands[hand_index]["cards"])

def deal_card_to_hand(hand_index):

    selectedcard = playingdeck.pop()
    playerhands[hand_index]["cards"].append(selectedcard)

    print('You have been dealt: ' + str(selectedcard.name))

    playerhands[hand_index]["total"] = get_total(playerhands[hand_index]["cards"])
    
    return selectedcard
    
def hit(hand_index):
    hand = playerhands[hand_index]

    print("\n")
    
    if hand["split_aces"]:
        print("You cannot hit after splitting aces")
        return

    if hand["finished"]:
        print("This hand has already finished.")
        return

    selectedcard = deal_card_to_hand(hand_index)

    print("Hand: ", hand["cards"])
    print("Your total is one of: ", hand["total"])
    
    if all(x > 21 for x in hand["total"]):
        print('Hand ' + str(hand_index) + ' has bust.')
        hand["finished"] = True
        next_hand(hand_index)
        return

def stand(hand_index):

    print("\n")
    playerhands[hand_index]["finished"] = True
    print('You stand on Hand', hand_index + 1)

    next_hand(hand_index)

def dealerdeal():
    global dealertotal
    random.shuffle(playingdeck)
    selectedcard = playingdeck.pop()
    dealerhand.append(selectedcard)
    length_total = len(dealertotal)
    if selectedcard != ace:
        for i in range(length_total):
            dealertotal[i] += selectedcard.value
    else:
        for i in range(length_total):
            dealertotal[i] += 1
            dealertotal.append(dealertotal[i] + 10)
    dealertotal = list(set(dealertotal))

def dealerdealshow():
    global dealertotal
    global dealerupcard
    random.shuffle(playingdeck)
    selectedcard = playingdeck.pop()
    dealerhand.append(selectedcard)
    length_total = len(dealertotal)
    if selectedcard != ace:
        for i in range(length_total):
            dealertotal[i] += selectedcard.value
    else:
        for i in range(length_total):
            dealertotal[i] += 1
            dealertotal.append(dealertotal[i] + 10)
    dealertotal = list(set(dealertotal))
    print('The dealer has: '+str(selectedcard.name)+' and an unkown card')
    dealerupcard = selectedcard

def playersetup():
    deal_card_to_player(0)
    deal_card_to_player(0)

    print('Your hand is: ' + str(playerhands[0]["cards"]))
    print('Your total is one of: ' + str(playerhands[0]["total"]))

def dealersetup():
    dealerdealshow()
    dealerdeal()

def double(hand_index):

    hand = playerhands[hand_index]

    print("\n")
    
    if len(hand["cards"]) != 2: # can only double with two cards in hand
        print("You can only double on your first two cards.")
        player_move(hand_index)
        return

    if hand["split_aces"]: # Cannot double split aces
        print("You cannot double after splitting aces.")
        player_move(hand_index)
        return

    if money < hand["bet"]: # Check you can afford the additional bet
        print("You do not have enough money to double.")
        player_move(hand_index)
        return

    hand["bet"] *= 2 # Double the bet for this hand

    print("Your bet for Hand " + str(hand_index) + " is now " + str(hand["bet"]))

    deal_card_to_hand(hand_index)  # You receive exactly one more card

    print("Hand:", hand["cards"])
    print("Your total is one of:", hand["total"])

    hand["finished"] = True #Automatically stand after doubling

    if all(x > 21 for x in hand["total"]):    # Check whether the player bust
        print("You have bust.")

    else:
        print("You automatically stand after doubling.")

    next_hand(hand_index) # Move to next hand

def split(hand_index):
    global playerhands

    hand = playerhands[hand_index]
    cards = hand["cards"]

    if len(cards) != 2: # You can ponly split hands with two cards
        print("You can only split a two-card hand.")
        return 

    if cards[0].value != cards[1].value: # You can only split cards of equal values (e.g. Queen-10 is allowed)
        print("You can only split matching cards.")
        return 

    if money < hand["bet"]: # When splitting, the overall money comitted is doubled; have to have the funds for this.
        print("You do not have enough money to split.")
        return 

    if hand["split_aces"]: # We are not allowing the resplitting of aces
        print("You cannot resplit aces")
        return

    splitting_aces = (cards[0] == ace and cards[1] == ace) # Check if we are splitting aces

    hand1 = {"cards": [cards[0]], "total": [], "bet": hand["bet"], "finished": False, "split_aces": splitting_aces, "from_split": True}
    hand2 = {"cards": [cards[1]], "total": [], "bet": hand["bet"], "finished": False, "split_aces": splitting_aces, "from_split": True}

    playerhands[hand_index] = hand1 # Replace the old hand with the first new hand

    playerhands.insert(hand_index + 1, hand2) # Insert the second hand after it, indexing allows multiple splits

    print("\n")
    deal_card_to_player(hand_index) # Deal one card to both new hands
    deal_card_to_player(hand_index + 1)

    if splitting_aces: # Special rules for splitting aces
        
        print('\nYou split aces.')
        print('Hand ' + str(hand_index + 1) + ':', playerhands[hand_index]["cards"])
        print('Hand ' + str(hand_index + 2) + ':', playerhands[hand_index + 1]["cards"])

        print('Split aces receive one card only and automatically stand.')

        playerhands[hand_index]["finished"] = True
        playerhands[hand_index + 1]["finished"] = True
        next_hand(hand_index)

        return    

    print('\nYou have split your hand.')

    print('Hand ' + str(hand_index) + ': ' + str(playerhands[hand_index]["cards"]))
    print('Total: ' + str(playerhands[hand_index]["total"]))
    print('Hand ' + str(hand_index + 1) + ': ' + str(playerhands[hand_index + 1]["cards"]))
    print('Total: ' + str(playerhands[hand_index + 1]["total"]))

    player_move(hand_index)

def player_move(hand_index):

    hand = playerhands[hand_index]
    
    if hand["finished"]: # Skip hand if already finished
        next_hand(hand_index)
        return

    print('\n----------------------')
    print('Playing Hand', hand_index)
    print('Cards:', hand["cards"])
    print('Total:', hand["total"])

    command = input('What would you like to do? ''(hit / stand / double / split / basic strategy): ').lower()

    if command == "hit":
        hit(hand_index)

        if not playerhands[hand_index]["finished"]: # Skip if this hand is already finished
            player_move(hand_index)

    elif command == "stand":
        stand(hand_index)
        
    elif command == "double":
        double(hand_index)

    elif command == "split":
        split(hand_index)

    elif command == "basic strategy":
        basic_strategy(hand_index)

    else:
        print('That is not a valid command.')
        player_move(hand_index)

    roundstart(hand["bet"])  #Play next hand

def next_hand(hand_index):

    for i in range(len(playerhands)): # Look for another unfinished hand

        if not playerhands[i]["finished"]:
            player_move(i)
            return

    print('\nAll player hands have finished.') # If all hands are finished, dealer plays

    dealer_play()
    resolve_hands()

def dealer_play():

    global dealertotal

    dealertotal = [x for x in dealertotal if x <= 21]

    while dealertotal and not any(17 <= x <= 21 for x in dealertotal): # As otherwise dealer stands on 17 and above, or is bust

        dealerdeal()
        dealertotal = [x for x in dealertotal if x <= 21]

    print('\nDealer hand:', dealerhand)
    
    if dealertotal: # If valid total
        print('Dealer total:', max(dealertotal))

    else:
        print('Dealer busts')

def is_blackjack(hand_index):

    hand = playerhands[hand_index]

    return (len(hand["cards"]) == 2 and 21 in hand["total"] and not hand["from_split"]) # Cannot get blackjack after splitting

def resolve_hands():
    global money

    dealer_bust = not dealertotal # Dealer busts

    dealer_blackjack = (len(dealerhand) == 2 and 21 in dealertotal)

    maxdealer = max(dealertotal) if dealertotal else None

    print('\n')
    print('Results')

    for i, hand in enumerate(playerhands):
        totals = hand["total"]
        valid_totals = [x for x in totals if x <= 21]

        hand_blackjack = is_blackjack(i)

        print('\nHand', i)
        print('Cards:', hand["cards"])

        if not valid_totals: # Player busts
            print('You bust, you lose.')
            money -= hand["bet"]
            continue

        maxplayer = max(valid_totals)

        print('Your Total:', maxplayer)

        if hand_blackjack and dealer_blackjack: # Both player and dealer get blackjack
            print('Both you and the dealer have blackjack, draw.')

        elif hand_blackjack: # Only player has blackjack
            print('You have blackjack, you win 1.5 times your bet.')
            money += 1.5 * hand["bet"]

        elif dealer_blackjack: # Only dealer has blackjack
            print('Dealer has blackjack - you lose.')
            money -= hand["bet"]

        elif dealer_bust: # Dealer busts
            print('Dealer busts, you win.')
            money += hand["bet"]

        elif maxplayer > maxdealer: # Both hands play, and neither have blackjack, and you have higher
            print('You win.')
            money += hand["bet"]

        elif maxplayer < maxdealer: # Both hands play, and neither have blackjack, and you have lower
            print('You lose.')
            money -= hand["bet"]

        else:
            print('Draw.')

    print('\nYou have:', money, 'money left.')
    print('\n')

def basic_strategy(hand_index):

    hand = playerhands[hand_index]
    cards = hand["cards"]
    totals = hand["total"]

    dealer_value = dealerhand[0].value

    if dealer_value == 11:
        dealer_value = 11

    print("\n")
    
    if len(cards) == 2 and not hand["split_aces"]: # Check if hand should be split
        card1 = cards[0]
        card2 = cards[1]

        if card1.value == card2.value:
            pair_value = card1.value

            if card1 == ace and card2 == ace: # Always split aces
                print("Split according to basic strategy")
                return "split"

            elif pair_value == 10: # Never split 10s
                pass

            elif pair_value == 9: #Rest are all according to basic strategy

                if dealer_value in [2, 3, 4, 5, 6, 8, 9]:
                    print("Split according to basic strategy")
                    return "split"

            elif pair_value == 8:
                print("Split according to basic strategy")
                return "split"

            elif pair_value == 7:

                if 2 <= dealer_value <= 7:
                    print("Split according to basic strategy")
                    return "split"

            elif pair_value == 6:

                if 2 <= dealer_value <= 6:
                    print("Split according to basic strategy")
                    return "split"

            elif pair_value == 4:

                if dealer_value in [5, 6]:
                    print("Split according to basic strategy")
                    return "split"

            elif pair_value == 3:

                if 2 <= dealer_value <= 7:
                    print("Split according to basic strategy")
                    return "split"

            elif pair_value == 2:

                if 2 <= dealer_value <= 7:
                    print("Split according to basic strategy")
                    return "split"


    valid_totals = [x for x in totals if x <= 21] #Find valid totals

    if len(valid_totals) == 0: # Check if bust
        print("Bust")
        return "bust"

    is_soft = len(valid_totals) > 1

    if is_soft: # If the ace can count as an 11, it is soft and do the following:

        player_total = max(valid_totals)

        if player_total == 13:

            if dealer_value in [5, 6]:
                print("Double according to basic strategy")
                return "double"
            else:
                print("Hit according to basic strategy")
                return "hit"

        elif player_total == 14:

            if dealer_value in [5, 6]:
                print("Double according to basic strategy")
                return "double"
            else:
                print("Hit according to basic strategy")
                return "hit"

        elif player_total == 15:

            if 4 <= dealer_value <= 6:
                print("Double according to basic strategy")
                return "double"
            else:
                print("Hit according to basic strategy")
                return "hit"

        elif player_total == 16:

            if 4 <= dealer_value <= 6:
                print("Double according to basic strategy")
                return "double"
            else:
                print("Hit according to basic strategy")
                return "hit"

        elif player_total == 17:

            if 3 <= dealer_value <= 6:
                print("Double according to basic strategy")
                return "double"
            else:
                print("Hit according to basic strategy")
                return "hit"

        elif player_total == 18:

            if 2 <= dealer_value <= 6:
                print("Double according to basic strategy")
                return "double"

            elif dealer_value in [7, 8]:
                print("Stand according to basic strategy")
                return "stand"

            else:
                print("Hit according to basic strategy")
                return "hit"

        elif player_total == 19:

            if dealer_value == 6:
                print("Double according to basic strategy")
                return "double"

            else:
                print("Stand according to basic strategy")
                return "stand"

        else:
            print("Stand according to basic strategy")
            return "stand"

    else: # Play the hand hard

        player_total = max(valid_totals)

        if player_total <= 8:
            print("Hit according to basic strategy")
            return "hit"

        elif player_total == 9:

            if 3 <= dealer_value <= 6:
                print("Double according to basic strategy")
                return "double"
            else:
                print("Hit according to basic strategy")
                return "hit"

        elif player_total == 10:

            if 2 <= dealer_value <= 9:
                print("Double according to basic strategy")
                return "double"
            else:
                print("Hit according to basic strategy")
                return "hit"

        elif player_total == 11:
            print("Double according to basic strategy")
            return "double"

        elif player_total == 12:

            if 4 <= dealer_value <= 6:
                print("Stand according to basic strategy")
                return "stand"
            else:
                print("Hit according to basic strategy")
                return "hit"

        elif 13 <= player_total <= 16:

            if 2 <= dealer_value <= 6:
                print("Stand according to basic strategy")
                return "stand"
            else:
                print("Hit according to basic strategy")
                return "hit"

        else:
            print("Stand according to basic strategy")
            return "stand" 
            
    player_move(hand_index) # Choose what command to do

gamestart(100, 2, 1) # Set up game and start playing 
roundstart(1)
