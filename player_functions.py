# This module stores the in-game methods of players

from property_data import BOARD, Property, Utility, Land, FG_COLORS, BG_COLORS, LAND_COLORS
import chance_functions, chest_functions

import os
from random import randint
from colorit import init_colorit, color, background

clear = lambda: os.system('cls')

init_colorit()

class Player:
    players = []

    def __init__(self,no,cash=1500):
        # Basic player attributes
        self.no = no
        self.cash = cash
        self.owned_props = [] # List of numbers
        self.injail = False
        self.get_out_of_jail_free_chance = False # Owns the Get Out of Jail Free card?
        self.get_out_of_jail_free_chest = False
        self.square = 0 # A square from 0 to 39 indicating the position
        self.bankrupt = False
        
        # Turn-related attributes
        self.doubles = 0 # Number of successive doubles rolled until this turn
        self.repeat_turn = False

        Player.players.append(self)

    def __str__(self):
        if self.injail == False:
            result = "Player {}\nCurrent cash: ${}\nCurrent position: {}".format(self.no+1,self.cash,self.get_position().name)
        elif self.injail == True:
            result = "Player {}\nCurrent cash: ${}\nIn Jail (rolled {} times)".format(self.no+1,self.cash,self.jailrolls)
        return result
    
    def get_position(self):
        pos = self.game.board[self.square]
        return pos
    
    def run_turn(self):
        if self.bankrupt == True:
            # Skip player if bankrupt
            print('Player {} is bankrupt'.format(self.no+1))
            self.game.turn = (self.game.turn + 1) % self.game.no_of_players
            print('\nPass turn to Player {}'.format(self.game.turn+1))
            input('')
            clear()
        else:
            # Choose an option
            while True:
                print(self)
                if self.cash < 0:
                    print('\nWarning: You are running low on cash. Please mortgage properties or sell houses before rolling')
                print('\nPlease select option:')
                if self.cash >= 0:
                    print('0 or blank - Roll Dice')
                    options = ['0','1','2','3','4','5','']
                else:
                    print(color('0 or blank - Roll Dice', (128,128,128)))
                    options = ['1','2','3','4','5']
                print('1 - View Properties')
                print('2 - Trade Properties')
                print('3 - Build Houses')
                print('4 - Mortgage Properties')
                print('5 - Quit (Declare Bankruptcy)')

                opt = input('>>> ')
                if opt in options:
                    clear()
                    break
                else:
                    print('\nPlease enter a valid input.')
                    input('')
                    clear()
                    continue
            
            if opt == '' or opt == '0':
                print(self)
                # Roll dice
                self.roll_dice()
                
                input('')
                clear()
                
                # Transfer turn to next player
                print(self)

                if self.repeat_turn == False:
                    self.game.turn = (self.game.turn + 1) % self.game.no_of_players
                    print('\nPass turn to Player {}'.format(self.game.turn+1))
                else:
                    print('\nPlay again')
                input('')
                clear()
            
            elif opt == '1':
                print(self)
                print('\nOwned properties:\n')
                for prop in self.owned_props:
                    print(str(self.game.board[prop]) + '\n\n--------------------\n')
                if self.get_out_of_jail_free_chance == True:
                    print('Get Out Of Jail Free Card -\nMay be kept until needed or sold/traded (Chance)')
                if self.get_out_of_jail_free_chest == True:
                    print('Get Out Of Jail Free Card -\nMay be kept until needed or sold/traded (Community Chest)')
                print('\nPress Enter to continue')
                input('')
                clear()
            
            elif opt == '2':
                self.trade_properties()
    
            elif opt == '3':
                self.build_houses()
                clear()
    
            elif opt == '4':
                self.mortgage_properties()
                clear()
    
            elif opt == '5':
                while True:
                    print(self)
                    print("Are you sure you want to declare bankruptcy and quit?")
                    print('0 or blank - No')
                    print('1 - Yes')
                    x = input('\n>>> ')

                    if x in ['','0']:
                        break
                    elif x == '1':
                        print('\nYou have declared bankruptcy and left the game')
                        self.bankrupt = True
                        for prop in self.owned_props:
                            self.game.board[prop].owner = None
                            self.game.board[prop].mortgaged = False
                            if isinstance(self.game.board[prop], Land):
                                self.game.board[prop].houses = 0
                        if self.get_out_of_jail_free_chance == True:
                            self.get_out_of_jail_free_chance = False
                            self.game.get_out_of_jail_free_chance = None
                        if self.get_out_of_jail_free_chest == True:
                            self.get_out_of_jail_free_chest = False
                            self.game.get_out_of_jail_free_chest = None
                        input('')
                        break
                    else:
                        print('\nInvalid option.')
                        input('')
                        clear()
                        continue
                
                clear()

    def roll_dice(self):
        if self.injail == False:
            d1 = randint(1,6)
            d2 = randint(1,6)
            total = d1 + d2
            if d1 == d2:
                # Rolled a double
                if self.doubles < 2:
                    # Rolled fewer than two doubles before - repeat turn
                    self.doubles += 1
                    self.repeat_turn = True
                    print('\nYou rolled a double {}'.format(total))
                    self.move(total)
                else:
                    # Rolled two doubles before - 3 successive doubles go to jail, must pass turn
                    self.doubles = 0
                    self.repeat_turn = False
                    print('\nYou rolled 3 doubles. Go to Jail')
                    self.go_to_jail()
                    
            else:
                # No double
                self.doubles = 0
                self.repeat_turn = False
                print('\nYou rolled a {}'.format(total))
                self.move(total)
        elif self.injail == True:
            while True:
                options = ['','0','1']
                print('\nYou are in jail now.')
                print('\nPlease select option:')
                print('0 or blank --- Roll Dice')
                print('1 ------------ Pay $50 to Get Out Of Jail')
                if self.get_out_of_jail_free_chance == True:
                    print('2 ------------ Use Get Out Of Jail Free Card - Chance')
                    options.append('2')
                if self.get_out_of_jail_free_chest == True:
                    print('3 ------------ Use Get Out Of Jail Free Card - Community Chest')
                    options.append('3')
                opt = input('>>> ')
                if opt in options:
                    break
                else:
                    print('\nPlease enter a valid input.')
                    input('')
                    clear()
                    continue
            clear()
            
            print(self)
            if opt == '' or opt == '0':
                d1 = randint(1,6)
                d2 = randint(1,6)
                total = d1 + d2
                if d1 == d2:
                    # Roll double to get out (no extra turns)
                    print('\nYou rolled a double {} out of jail'.format(total))
                    self.out_of_jail()
                    self.move(total)
                elif self.jailrolls == 2:
                    # Pay a $50 fine on the third non-double roll
                    print('\nYou rolled a {} on the third roll to get out of jail'.format(total))
                    print('You have been fined $50')
                    self.cash -= 50
                    self.out_of_jail()
                    self.move(total)
                else:
                    if self.jailrolls == 0:
                        roll = 'first'
                    elif self.jailrolls == 1:
                        roll = 'second'
                    print('\nYou rolled a {} on the {} roll'.format(total,roll))
                    print('You are still in jail')
                    self.jailrolls += 1
            
                self.doubles = 0
                self.repeat_turn = False
                
            elif opt == '1':
                print('\nYou have paid $50 to get out of jail')
                self.cash -= 50
                self.out_of_jail()
                self.roll_dice()
            
            elif opt == '2':
                print('\nYou have used a Get Out Of Jail Free card')
                self.get_out_of_jail_free_chance = False
                self.game.get_out_of_jail_free_chance = None
                self.out_of_jail()
                self.roll_dice()
                
            elif opt == '3':
                print('\nYou have used a Get Out Of Jail Free card')
                self.get_out_of_jail_free_chest = False
                self.game.get_out_of_jail_free_chest = None
                self.out_of_jail()
                self.roll_dice()
            
    def move(self,spaces):
        if self.square + spaces >= 40:
            self.cash += 200
            print('You passed Go. Collect $200')
        self.square = (self.square + spaces) % 40
        print('You landed on {}'.format(self.get_position().name))
        input('')
        clear()
        self.action()
        
    def action(self):
        get_square = self.get_position()
        print(self)
        if isinstance(get_square,Property):
            if get_square.owner == self.no:
                pass
            elif get_square.owner != None:
                if get_square.mortgaged == False:
                    self.pay_rent(self.square)
            elif self.cash - get_square.price < 0:
                print('\n{} is not owned, but you do not have enough cash to buy this property.'.format(get_square.name))
                print(get_square)
            else:
                while True:
                    print('\n{} is not owned. Do you buy the property?\n'.format(get_square.name))
                    print(get_square)
                    print('0 - No')
                    print('1 - Yes')
                    x = input('>>> ')
                    if x == '0':
                        clear()
                        print(self)
                        print('\nYou declined {}'.format(get_square.name))
                        break
                    elif x == '1':
                        self.buy_prop(self.square)
                        clear()
                        print(self)
                        print('\nYou bought {} for ${}'.format(get_square.name,get_square.price))
                        break
                    else:
                        print('Invalid option.')
                        input('')
                        clear()
                        print(self)
                        continue
        elif get_square.name == 'Chance':
            print('\nPress Enter to open Chance card')
            input('')
            clear()
            self.get_chance()
        elif get_square.name == 'Community Chest':
            print('\nPress Enter to open Community Chest card')
            input('')
            clear()
            self.get_community_chest()
        elif get_square.name == 'Go To Jail':
            self.go_to_jail()
        elif get_square.name == 'Income Tax':
            print('\nYou owe $200 for Income Tax')
            self.cash -= 200
        elif get_square.name == 'Luxury Tax':
            print('\nYou owe $75 for Luxury Tax')
            self.cash -= 75
    
    def pay_player(self,player,amount):
        self.cash -= amount
        self.players[player].cash += amount

    def buy_prop(self,square):
        # Parameter square refers to the position on the board
        prop = self.game.board[square]
        self.owned_props.append(square)
        self.owned_props.sort()
        self.cash -= prop.price
        prop.owner = self.no
            
    def pay_rent(self,square):
        # Parameter square refers to the position on the board
        prop = self.game.board[square]
        
        if isinstance(prop,Utility):
            d1 = randint(1,6)
            d2 = randint(1,6)
            total = d1 + d2
            rent_owed = total * prop.rent_factor()

            self.pay_player(prop.owner, rent_owed)
            
            print('\nYou rolled a {} and owe Player {} ${} for {}'\
            .format(total,prop.owner+1,rent_owed,prop.name))
        else:
            rent_owed = prop.get_rent()

            self.pay_player(prop.owner, rent_owed)
            
            print('\nYou owe Player {} ${} for {}'\
            .format(prop.owner+1,rent_owed,prop.name))
    
    def trade_properties(self):
        # Step 1: Select a player to trade with
        player_options = ['0', '']
        for player in self.players:
            if player.no != self.no and player.bankrupt == False:
                player_options.append(str(player.no+1))
        while True:
            print('Player {}'.format(self.no+1))
            trader = input('\nChoose a player to trade with, or input 0 or leave blank to cancel: ')
            if trader in player_options:
                if trader not in ['0', '']:
                    trading_player = self.players[int(trader)-1]
                    clear()
                break
            else:
                print('Invalid option. Please try again.')
                input('')
                clear()
            
        if trader in ['0', '']:
            clear()
        else:
            # Step 2: Choose items to exchange
            traded_items = []
            cash_exchange = 0
            while True:
                print('Player {}'.format(self.no+1))
                print('\nYou have decided to offer Player {}:'.format(trader))
                for prop in traded_items:
                    if prop in self.owned_props:
                        print('{} - {}'.format(prop, self.board[prop].name))
                    elif prop == 41:
                        if self.game.get_out_of_jail_free_chance == self.no:
                            print('41 - Get Out Of Jail Free Card - Chance')
                    elif prop == 42:
                        if self.game.get_out_of_jail_free_chest == self.no:
                            print('42 - Get Out Of Jail Free Card - Community Chest')
                if cash_exchange > 0:
                    print('Cash: ${}'.format(cash_exchange))
                print('\nIn exchange for:')
                for prop in traded_items:
                    if prop in trading_player.owned_props:
                        print('{} - {}'.format(prop, self.board[prop].name))
                    elif prop == 41:
                        if self.game.get_out_of_jail_free_chance == trading_player.no:
                            print('41 - Get Out Of Jail Free Card - Chance')
                    elif prop == 42:
                        if self.game.get_out_of_jail_free_chest == trading_player.no:
                            print('42 - Get Out Of Jail Free Card - Community Chest')
                if cash_exchange < 0:
                    print('Cash: ${}'.format(-cash_exchange))
                        
                print('\nChoose properties to trade, or enter to delete items above:')
                trading_options = ['0', '', '50']
                print('0 or blank - Continue')
                print('Owned by you:')
                for prop in self.owned_props:
                    if self.board[prop].mortgaged == False:
                        if prop not in traded_items:
                            print('{} - {}'.format(prop, self.board[prop].name))
                        trading_options.append(str(prop))
                if self.game.get_out_of_jail_free_chance == self.no:
                    if 41 not in traded_items:
                        print('41 - Get Out Of Jail Free Card - Chance')
                    trading_options.append('41')
                if self.game.get_out_of_jail_free_chest == self.no:
                    if 42 not in traded_items:
                        print('42 - Get Out Of Jail Free Card - Community Chest')
                    trading_options.append('42')
                print('Cash: ${}'.format(self.cash))
                print('Owned by Player {}'.format(trader))
                for prop in trading_player.owned_props:
                    if self.board[prop].mortgaged == False:
                        if prop not in traded_items:
                            print('{} - {}'.format(prop, self.board[prop].name))
                        trading_options.append(str(prop))
                if self.game.get_out_of_jail_free_chance == trading_player.no:
                    if 41 not in traded_items:
                        print('41 - Get Out Of Jail Free Card - Chance')
                    trading_options.append('41')
                if self.game.get_out_of_jail_free_chest == trading_player.no:
                    if 42 not in traded_items:
                        print('42 - Get Out Of Jail Free Card - Community Chest')
                    trading_options.append('42')
                print('Cash: ${}'.format(trading_player.cash))
                
                print('\n50 - Exchange Cash')
                
                trade = input('>>> ')
                
                if trade in trading_options:
                    if trade in ['0', '']:
                        break
                    elif trade == '50':
                        while True:
                            try:
                                cash_exchange = int(input('Enter amount to offer (- to receive): $'))
                                break
                            except ValueError:
                                continue
                    elif int(trade) in traded_items:
                        traded_items.remove(int(trade))
                    else:
                        traded_items.append(int(trade))
                else:
                    print('\nInvalid option.')
                    input('')
                clear()
                        
            # Step 3: Trading player agrees or disagrees with trade
            if traded_items != [] or cash_exchange != 0:
                print('Pass turn to Player {}'.format(trading_player.no+1))
                input('')
                clear()
                while True:
                    print('Player {}'.format(trading_player.no+1))
                    print('Current cash: ${}'.format(trading_player.cash))
                    print('\nPlayer {} offers:'.format(self.no+1))
                    for prop in traded_items:
                        if prop in self.owned_props:
                            print('{} - {}'.format(prop, self.board[prop].name))
                        elif prop == 41:
                            if self.game.get_out_of_jail_free_chance == self.no:
                                print('41 - Get Out Of Jail Free Card - Chance')
                        elif prop == 42:
                            if self.game.get_out_of_jail_free_chest == self.no:
                                print('42 - Get Out Of Jail Free Card - Community Chest')
                    if cash_exchange > 0:
                        print('Cash: ${}'.format(cash_exchange))
                    print('In exchange for:')
                    for prop in traded_items:
                        if prop in trading_player.owned_props:
                            print('{} - {}'.format(prop, self.board[prop].name))
                        elif prop == 41:
                            if self.game.get_out_of_jail_free_chance == trading_player.no:
                                print('41 - Get Out Of Jail Free Card - Chance')
                        elif prop == 42:
                            if self.game.get_out_of_jail_free_chest == trading_player.no:
                                print('42 - Get Out Of Jail Free Card - Community Chest')
                    if cash_exchange < 0:
                        print('Cash: ${}'.format(-cash_exchange))
                    
                    print('Do you agree with the trade?')
                    print('0 - No')
                    print('1 - Yes')
                    x = input('\n>>> ')
                    if x == '0':
                        print('\nTrade declined.')
                        break
                    elif x == '1':
                        # Step 4: Apply trade
                        for prop in traded_items:
                            if prop == 41:
                                if self.game.get_out_of_jail_free_chance == self.no:
                                    self.get_out_of_jail_free_chance = False
                                    trading_player.get_out_of_jail_free_chance = True
                                    self.game.get_out_of_jail_free_chance = trading_player.no
                                elif self.game.get_out_of_jail_free_chance == trading_player.no:
                                    self.get_out_of_jail_free_chance = True
                                    trading_player.get_out_of_jail_free_chance = False
                                    self.game.get_out_of_jail_free_chance = self.no
                            elif prop == 42:
                                if self.game.get_out_of_jail_free_chest == self.no:
                                    self.get_out_of_jail_free_chest = False
                                    trading_player.get_out_of_jail_free_chest = True
                                    self.game.get_out_of_jail_free_chest = trading_player.no
                                elif self.game.get_out_of_jail_free_chest == trading_player.no:
                                    self.get_out_of_jail_free_chest = True
                                    trading_player.get_out_of_jail_free_chest = False
                                    self.game.get_out_of_jail_free_chest = self.no
                            else:
                                if prop in self.owned_props:
                                    self.owned_props.remove(prop)
                                    trading_player.owned_props.append(prop)
                                    trading_player.owned_props.sort()
                                    self.board[prop].owner = trading_player.no
                                elif prop in trading_player.owned_props:
                                    trading_player.owned_props.remove(prop)
                                    self.owned_props.append(prop)
                                    self.owned_props.sort()
                                    self.board[prop].owner = self.no
                                    
                        self.cash -= cash_exchange
                        trading_player.cash += cash_exchange
                        print('\nTrade successful.')
                        break
                    else:
                        print('\nInvalid option.')
                        input('')
                        clear()
                        continue
                input('')
                clear()
            else:
                clear()

    def build_houses(self):
        x = None
        # Choose a color
        while True:
            print(self)
            valid_colors = []
            for prop in self.owned_props:
                if isinstance(self.game.board[prop], Land):
                    if self.game.board[prop].house_buildable():
                        valid_colors.append(self.game.board[prop].color)
            
            color_index = {'1': 'brown',
                           '2': 'light blue',
                           '3': 'pink',
                           '4': 'orange',
                           '5': 'red',
                           '6': 'yellow',
                           '7': 'green',
                           '8': 'blue'}
            
            options = ['0', '']
            print('\nYou may build houses on the following color groups:')
            print('0 or blank - Cancel')
            for value in color_index:
                if color_index[value] in valid_colors:
                    print(color(background('{} - {}' \
                        .format(value, color_index[value]), \
                            BG_COLORS[color_index[value]]), \
                            FG_COLORS[color_index[value]]))
                    options.append(value)
                
            x = input('Choose an option: ')

            if x in ['0', '']:
                break
            elif x in options:
                clear()
                # Build houses on chosen color
                color_chosen = color_index[x]
                self.build_houses_on_color(color_chosen)
            else:
                print('\nInvalid input.')
                input('')
                clear()
    
    def build_houses_on_color(self, color_chosen):
        added_houses = {prop.position: 0 for prop in LAND_COLORS[color_chosen]}
        
        while True:
            print(self)
            print('Color chosen: ' + color(background(color_chosen, BG_COLORS[color_chosen]), FG_COLORS[color_chosen]))
            options = ['0', '', 'c', 'C']
            
            print('\nChoose a property to build houses on:')
            print('0 or blank - Done')
            print('C - Cancel')

            leftover_houses = self.game.total_houses
            leftover_hotels = self.game.total_hotels

            for prop in LAND_COLORS[color_chosen]:
                if prop.houses == 5:
                    leftover_hotels += 1
                else:
                    leftover_houses += prop.houses
                if prop.houses + added_houses[prop.position] == 5:
                    leftover_hotels -= 1
                else:
                    leftover_houses -= prop.houses + added_houses[prop.position]

            if self.game.house_limited == True:
                print('\nNumber of houses available: {}'.format(leftover_houses))
                print('Number of hotels available: {}'.format(leftover_hotels))

            for prop in LAND_COLORS[color_chosen]:
                if prop.houses + added_houses[prop.position] == 0:
                    houses_str = 'Unimproved'
                elif prop.houses + added_houses[prop.position] <= 4:
                    houses_str = '{} houses'.format(prop.houses + added_houses[prop.position])
                elif prop.houses + added_houses[prop.position] == 5:
                    houses_str = 'Hotel'
                print('{} - {} - {} - ${} per house'.format(prop.position, prop.name, houses_str, prop.house_price))
                options.append(str(prop.position))
            
            total_price = 0
            for prop in LAND_COLORS[color_chosen]:
                if added_houses[prop.position] >= 0:
                    total_price += added_houses[prop.position] * prop.house_price
                elif added_houses[prop.position] < 0:
                    total_price += int(added_houses[prop.position] * prop.house_price / 2)
            print('\nTotal price: ${}'.format(total_price))
            
            opt = input('\n>>> ')
            
            # Enter number of houses to add or remove
            if opt in options:
                if opt == '0' or opt == '':
                    check1 = (leftover_houses >= 0) and (leftover_hotels >= 0) # Are there enough houses remaining?
                    color_houses = [prop.houses + added_houses[prop.position] for prop in LAND_COLORS[color_chosen]]
                    check2 = max(color_houses) - min(color_houses) <= 1 # Are the houses built evenly?
                    check3 = self.cash - total_price >= 0 # Do you have enough cash?
                    if all([check1,check2,check3]):
                        clear()
                        for prop in LAND_COLORS[color_chosen]:
                            prop.houses += added_houses[prop.position]
                        self.cash -= total_price
                        print(self)
                        print('\nTransaction successful.')
                        input('')
                        clear()
                        self.game.total_houses = leftover_houses
                        self.game.total_hotels = leftover_hotels
                        break
                    elif check1 == False:
                        print('\nInsufficient houses and hotels.')
                        input('')
                        clear()
                    elif check2 == False:
                        print('\nInvalid configuration. A square in a color set may not have more than one house more than any other square in the same set')
                        input('')
                        clear()
                    elif check3 == False:
                        print('\nYou do not have enough cash for this transaction.')
                        input('')
                        clear()
                elif opt.lower() == 'c':
                    clear()
                    break
                else:
                    prop = self.game.board[int(opt)]
                    add_houses = input('Enter number of houses to add or remove on {}: '.format(prop.name))
                    try:
                        add_houses = int(add_houses)
                        
                        if 0 <= prop.houses + added_houses[prop.position] + add_houses <= 5:
                            added_houses[prop.position] += add_houses
                            if add_houses > 0:
                                print('You added {} houses on {}'.format(add_houses, prop.name))
                            elif add_houses < 0:
                                print('You removed {} houses from {}'.format(-add_houses, prop.name))
                        else:
                            print('\nInvalid input. A property may have up to 5 houses (a hotel)')
                    except ValueError:
                        print('\nInvalid input. Must be an integer')
            else:
                print('\nInvalid input.')
            input('')
            clear()

    def mortgage_properties(self):
        x = None
        while True:
            print(self)
            options = []
            print('\nChoose a property to mortgage or unmortgage:')
            print('0 or blank - Cancel')
            for prop in self.owned_props:
                if prop.mortgageable() == True:
                    options.append(str(prop))
                    if self.game.board[prop].mortgaged == True:
                        price = int(self.game.board[prop].mortgage * 1.1)
                        print('{} - {} (Mortgaged) - Unmortgage Price: ${}'.format(prop, self.game.board[prop].name, price))
                    elif self.game.board[prop].mortgaged == False:
                        price = self.game.board[prop].mortgage
                        print('{} - {} - Mortgage Price: ${}'.format(prop, self.game.board[prop].name, price))
                elif prop.mortgageable() == False:
                    print(color('{} - {}{} - Mortgage Price: ${}'.format(prop, self.game.board[prop].name, price), (128,128,128)))
            
            x = input('>>> ')

            if x in ['', '0']:
                break
            elif x in options:
                x = int(x)
                if self.game.board[x].mortgaged == False:
                    self.cash += self.game.board[x].mortgage
                    self.game.board[x].mortgage_prop()
                elif self.game.board[x].mortgaged == True:
                    if self.cash - int(self.game.board[x].mortgage * 1.1) < 0:
                        print('\nYou do not have enough cash to unmortgage this property.')
                    else:
                        self.cash -= int(self.game.board[x].mortgage * 1.1)
                        self.game.board[x].mortgage_prop()
            else:
                print('\nInvalid Input:\nYou do not own this property, this property is not mortgageable, or the input is invalid.\nRemove all houses in the color group before mortgaging')
            input('')
            clear()
    
    def get_chance(self):
        print(self)
        while True:
            x = randint(0,15)
            if self.game.get_out_of_jail_free_chance != None and x == 6:
                continue
            else:
                card = chance_functions.CHANCE[x]
                break
        
        print('\nYou got the following card:')
        print(card.description)
        
        card.function(self)
        
    def get_community_chest(self):
        print(self)
        while True:
            x = randint(0,15)
            if self.game.get_out_of_jail_free_chest != None and x == 4:
                continue
            else:
                card = chest_functions.CHEST[x]
                break
        
        print('\nYou got the following card:')
        print(card.description)
        
        card.function(self)
    
    def go_to_jail(self):
        print('\nYou are now in jail.')
        self.injail = True
        self.jailrolls = 0
        self.repeat_turn = False # If player lands in jail, then turn unconditionally ends
        
    def out_of_jail(self):
        print('\nYou are now out of jail.')
        self.injail = False
        self.square = 10