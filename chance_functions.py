# This module stores the data for the Chance cards and functions

from property_data import Land
from random import randint

class ChanceCard:
    def __init__(self,description,function):
        self.description = description
        self.function = function

def CH1(player): # Advance to Go. Collect $200
    spaces = (0 - player.square) % 40
    
    player.move(spaces)
    
def CH2(player): # Advance to Illinois Avenue. If you pass Go, collect $200
    spaces = (24 - player.square) % 40
    
    player.move(spaces)
    
def CH3(player): # Advance to St. Charles Place. If you pass Go, collect $200
    spaces = (11 - player.square) % 40
    
    player.move(spaces)
    
def CH4(player): # Advance to nearest utility. If unowned, you may buy it from the bank. If owned, throw dice and pay owner 10 times the amount thrown
    spaces = min((12-player.square) % 40, (28-player.square) % 40)
    
    if player.square + spaces > 40:
        player.cash += 200
        print('You passed Go. Collect $200')
    
    player.square = (player.square + spaces) % 40
    print('You landed on {}'.format(player.get_position().name))
    
    prop = player.game.board[player.square]
    owner = prop.owner
    
    if owner == player.no:
        pass
    elif owner != None:
        d1 = randint(1,6)
        d2 = randint(1,6)
        total = d1 + d2
        rent = total * 10
        print('You rolled a {} and owe Player {} ${} for {}'.format(total,owner+1,rent,prop.name))
        player.pay_player(owner,rent)
    else:
        player.action()
    
def CH5(player): # Advance to nearest railroad and pay owner twice the rental. If unowned you may buy it from the bank
    spaces = (5 - player.square) % 10
    
    if player.square + spaces > 40:
        player.cash += 200
        print('You passed Go. Collect $200')
    
    player.square = (player.square + spaces) % 40
    print('You landed on {}'.format(player.get_position().name))
    
    prop = player.game.board[player.square]
    owner = prop.owner
    
    if owner == player.no:
        pass
    elif owner != None:
        rent = prop.get_rent() * 2
        print('You owe Player {} ${} for {}'.format(owner+1,rent,prop.name))
        player.pay_player(owner,rent)
    else:
        player.action()

def CH6(player): # Bank pays you a dividend of $50
    player.cash += 50

def CH7(player): # Get Out Of Jail Free Card - May be kept until needed or sold/traded
    player.get_out_of_jail_free_chance = True
    player.game.get_out_of_jail_free_chance = player.no

def CH8(player): # Go back 3 spaces
    player.move(-3)

def CH9(player): # Go to Jail. Go directly to Jail. Do not pass Go, Do not collect $200
    player.go_to_jail()

def CH10(player): # Make general repairs on your property: For each house pay $25, for each hotel $100
    total = 0
    for prop in player.owned_props:
        if isinstance(player.game.board[prop], Land):
            x = player.game.board[prop].houses
            if x == 5:
                total += 100
            else:
                total += x * 25
    print('Amount owed: ${}'.format(total))
    player.cash -= total

def CH11(player): # Pay poor tax of $15
    player.cash -= 15
    
def CH12(player): # Take a trip to Reading Railroad. If you pass Go, collect $200
    spaces = (5 - player.square) % 40
    
    player.move(spaces)

def CH13(player): # Take a walk on the Boardwalk. Advance to Boardwalk
    spaces = (39 - player.square) % 40
    
    player.move(spaces)

def CH14(player): # You have been elected chairman of the board. Pay each player $50
    for x in range(player.game.no_of_players):
        player.pay_player(x,50)

def CH15(player): # Your building loan matures. Collect $150
    player.cash += 150

def CH16(player): # You have won a crossword competition. Collect $100
    player.cash += 100

CHANCE = [ChanceCard('Advance to Go. Collect $200', CH1),
          ChanceCard('Advance to Illinois Avenue. If you pass Go, collect $200', CH2),
          ChanceCard('Advance to St. Charles Place. If you pass Go, collect $200', CH3),
          ChanceCard('Advance to nearest utility. If unowned, you may buy it from the bank. If owned, throw dice and pay owner 10 times the amount thrown', CH4),
          ChanceCard('Advance to nearest railroad and pay owner twice the rental. If unowned you may buy it from the bank', CH5),
          ChanceCard('Bank pays you a dividend of $50', CH6),
          ChanceCard('Get Out Of Jail Free Card - May be kept until need or sold/traded', CH7),
          ChanceCard('Go back 3 spaces', CH8),
          ChanceCard('Go to Jail. Go directly to Jail. Do not pass Go, Do not collect $200', CH9),
          ChanceCard('Make general repairs on your property: For each house pay $25, for each hotel $100', CH10),
          ChanceCard('Pay poor tax of $15', CH11),
          ChanceCard('Take a trip to Reading Railroad. If you pass Go, collect $200', CH12),
          ChanceCard('Take a walk on the Boardwalk. Advance to Boardwalk', CH13),
          ChanceCard('You have been elected chairman of the board. Pay each player $50', CH14),
          ChanceCard('Your building loan matures. Collect $150', CH15),
          ChanceCard('You have won a crossword competition. Collect $100', CH16)]