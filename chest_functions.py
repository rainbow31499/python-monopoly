# This module stores the data for the Community Chest cards and functions

from property_data import Land, BOARD

class CommunityChestCard:
    def __init__(self,description,function):
        self.description = description
        self.function = function

def CC1(player): # Advance to Go. Collect $200
    spaces = (0 - player.square) % 40
    
    player.move(spaces)

def CC2(player): # Bank error in your favor. Collect $200
    player.cash += 200

def CC3(player): # Doctor\'s fees. Pay $50
    player.cash -= 50

def CC4(player): # From sale of stock you get $50
    player.cash += 50

def CC5(player): # Get Out Of Jail Free Card - May be kept until needed or sold/traded
    player.get_out_of_jail_free_chest = True

def CC6(player): # Go to Jail. Go directly to Jail. Do not pass Go, Do not collect $200
    player.go_to_jail()

def CC7(player): # Grand Opera Night. Collect $50 from every player for opening night seats
    player.payments.append(('all',-50))

def CC8(player): # Holiday Fund matures. Collect $100
    player.cash += 100
    
def CC9(player): # Income tax refund. Collect $20
    player.cash += 20
    
def CC10(player): # Life insurance matures. Collect $100
    player.cash += 100
    
def CC11(player): # Hospital fees. Pay $50
    player.cash -= 50
    
def CC12(player): # School fees. Pay $50
    player.cash -= 50
    
def CC13(player): # Receive $25 consultancy fee
    player.cash += 25
    
def CC14(player): # You are assessed for street repairs: For each house pay $40, for each hotel $115
    total = 0
    for prop in player.owned_props:
        if isinstance(BOARD[prop], Land):
            x = BOARD[prop].houses
            if x == 5:
                total += 115
            else:
                total += x * 40
    print('Amount owed: ${}'.format(total))
    player.cash -= total
    
def CC15(player): # You have won second prize in a beauty contest. Collect $10
    player.cash += 10
    
def CC16(player): # You inherit $100
    player.cash += 100

CHEST = [CommunityChestCard('Advance to Go. Collect $200', CC1),
         CommunityChestCard('Bank error in your favor. Collect $200', CC2),
         CommunityChestCard('Doctor\'s fees. Pay $50', CC3),
         CommunityChestCard('From sale of stock you get $50', CC4),
         CommunityChestCard('Get Out Of Jail Free Card - May be kept until need or sold/traded', CC5),
         CommunityChestCard('Go to Jail. Go directly to Jail. Do not pass Go, Do not collect $200', CC6),
         CommunityChestCard('Grand Opera Night. Collect $50 from every player for opening night seats', CC7),
         CommunityChestCard('Holiday Fund matures. Collect $100', CC8),
         CommunityChestCard('Income tax refund. Collect $20', CC9),
         CommunityChestCard('Life insurance matures. Collect $100', CC10),
         CommunityChestCard('Hospital fees. Pay $50', CC11),
         CommunityChestCard('School fees. Pay $50', CC12),
         CommunityChestCard('Receive $25 consultancy fee', CC13),
         CommunityChestCard('You are assessed for street repairs: For each house pay $40, for each hotel $115', CC14),
         CommunityChestCard('You have won second prize in a beauty contest. Collect $10', CC15),
         CommunityChestCard('You inherit $100', CC16)]