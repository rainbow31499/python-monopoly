# This module stores the in-game methods of players

from property_data import BOARD, Property, Utility, Land, FG_COLORS, BG_COLORS, LAND_COLORS
import chance_functions, chest_functions

import os
from random import randint
from colorit import init_colorit, color, background

clear = lambda: os.system('cls')

init_colorit()

class Player:
    def __init__(self,no,cash=1500):
        # Basic player attributes
        self.no = no
        self.cash = cash
        self.owned_props = [] # List of numbers
        self.injail = False
        self.get_out_of_jail_free_chance = False
        self.get_out_of_jail_free_chest = False
        self.square = 0 # A square from 0 to 39 indicating the position
        self.bankrupt = False
        
        # Turn-related attributes
        self.get_out_of_jail_free_chance_used = False
        self.get_out_of_jail_free_chest_used = False
        self.doubles = 0 # Number of successive doubles rolled until this turn
        self.repeat_turn = False
        self.payments = []
        
    def get_position(self):
        if self.injail == False:
            pos = BOARD[self.square].name
            return pos
        elif self.injail == True:
            return 'In Jail'
    
    def __str__(self):
        result = "Player {}\nCurrent cash: ${}\nCurrent position: {}".format(self.no+1,self.cash,self.get_position())
        return result
    
    def roll_dice(self):
        if self.injail == False:
            d1 = randint(1,6)
            d2 = randint(1,6)
            total = d1 + d2
            if d1 == d2:
                # Rolled a double
                if self.doubles == 2:
                    # Rolled two doubles before - 3 successive doubles go to jail
                    self.doubles = 0
                    self.repeat_turn = False
                    print('\nYou rolled 3 doubles. Go to Jail')
                    self.go_to_jail()
                else:
                    # Rolled fewer than two doubles before - repeat turn
                    self.doubles += 1
                    self.repeat_turn = True
                    print('\nYou rolled a double {}'.format(total))
                    self.move(total)
                    
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
                self.out_of_jail()
                self.roll_dice()
                
            elif opt == '3':
                print('\nYou have used a Get Out Of Jail Free card')
                self.get_out_of_jail_free_chest = False
                self.out_of_jail()
                self.roll_dice()
            
    def move(self,spaces):
        if self.square + spaces >= 40:
            self.cash += 200
            print('You passed Go. Collect $200')
        self.square = (self.square + spaces) % 40
        print('You landed on {}'.format(self.get_position()))
        input('')
        clear()
        self.action()
        
    def action(self):
        get_square = BOARD[self.square]
        print(self)
        if isinstance(get_square,Property):
            if get_square.owner == self.no:
                pass
            elif get_square.owner != None:
                if get_square.mortgaged == False:
                    self.pay_rent(self.square)
            elif self.cash - get_square.price < 0:
                print('\n{} is not owned, but you do not have enough cash to buy this property.'.format(get_square.name))
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
        elif get_square.name == 'Go':
            pass
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
        elif get_square.name == 'Jail (Just Visiting)':
            pass
        elif get_square.name == 'Free Parking':
            pass
        elif get_square.name == 'Go To Jail':
            self.go_to_jail()
        elif get_square.name == 'Income Tax':
            print('\nYou owe $200 for Income Tax')
            self.cash -= 200
        elif get_square.name == 'Luxury Tax':
            print('\nYou owe $75 for Luxury Tax')
            self.cash -= 75
        
    def buy_prop(self,square):
        # Parameter square refers to the position on the board
        prop = BOARD[square]
        self.owned_props.append(square)
        self.owned_props.sort()
        self.cash -= prop.price
        prop.owner = self.no
            
    def pay_rent(self,square):
        # Parameter square refers to the position on the board
        prop = BOARD[square]
        prop_owner = prop.owner
        
        if isinstance(prop,Utility):
            d1 = randint(1,6)
            d2 = randint(1,6)
            total = d1 + d2
            rent_owed = total * prop.rent_factor()
            
            print('\nYou rolled a {} and owe Player {} ${} for {}'\
            .format(total,prop_owner+1,rent_owed,prop.name))
        else:
            rent_owed = prop.get_rent()
            
            print('\nYou owe Player {} ${} for {}'\
            .format(prop_owner+1,rent_owed,prop.name))
        
        self.payments.append((prop_owner, rent_owed))
    
    def build_houses(self,houses,hotels,limited):
        x = None
        # Choose a color
        while True:
            print(self)
            valid_colors = []
            for prop in self.owned_props:
                if isinstance(BOARD[prop], Land):
                    if BOARD[prop].full_set_owned() and not any([land.mortgaged for land in BOARD[prop].full_set()]):
                        valid_colors.append(BOARD[prop].color)
            
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
                    print(color(background('{} - {}'.format(value, color_index[value]), BG_COLORS[color_index[value]]),FG_COLORS[color_index[value]]))
                    options.append(value)
                
            x = input('Choose an option: ')
            if x in ['0', '']:
                break
            elif x in options:
                clear()
                # Build houses on chosen color
                color_chosen = color_index[x]
                properties_in_color = []
                added_houses = {}
                current_houses = 0
                current_hotels = 0
                for prop in self.owned_props:
                    get_square = BOARD[prop]
                    if isinstance(get_square, Land):
                        if get_square.color == color_chosen:
                            properties_in_color.append(prop)
                            added_houses[prop] = 0
                            if get_square.houses == 5:
                                current_hotels += 1
                            else:
                                current_houses += get_square.houses
                available_houses = houses + current_houses
                available_hotels = hotels + current_hotels
                
                while True:
                    print(self)
                    print('Color chosen: ' + color(background(color_chosen, BG_COLORS[color_chosen]), FG_COLORS[color_chosen]))
                    options = ['0', '', 'c', 'C']
                    leftover_houses = available_houses
                    leftover_hotels = available_hotels
                    for prop in properties_in_color:
                        get_square = BOARD[prop]
                        if get_square.houses + added_houses[prop] == 5:
                            leftover_hotels -= 1
                        else:
                            leftover_houses -= (get_square.houses + added_houses[prop])
                    if limited == True:
                        print('\nNumber of houses available: {}'.format(leftover_houses))
                        print('Number of hotels available: {}'.format(leftover_hotels))
                    print('\nChoose a property to build houses on:')
                    print('0 or blank - Done')
                    print('C - Cancel')
                    for prop in properties_in_color:
                        get_square = BOARD[prop]
                        if get_square.houses + added_houses[prop] == 0:
                            houses_str = 'Unimproved'
                        elif get_square.houses + added_houses[prop] <= 4:
                            houses_str = '{} houses'.format(get_square.houses + added_houses[prop])
                        elif get_square.houses + added_houses[prop] == 5:
                            houses_str = 'Hotel'
                        print('{} - {} - {} - ${} per house'.format(prop, get_square.name, houses_str, get_square.house_price))
                        options.append(str(prop))
                    total_price = 0
                    for prop in properties_in_color:
                        if added_houses[prop] >= 0:
                            total_price += added_houses[prop] * BOARD[prop].house_price
                        elif added_houses[prop] < 0:
                            total_price += int(added_houses[prop] * BOARD[prop].house_price / 2)
                    print('\nTotal price: ${}'.format(total_price))
                    
                    y = input('\n>>> ')
                    
                    # Enter number of houses to add or remove
                    if y in options:
                        if y == '0' or y == '':
                            check1 = (leftover_houses >= 0) and (leftover_hotels >= 0)
                            color_houses = [BOARD[prop].houses + added_houses[prop] for prop in added_houses]
                            check2 = max(color_houses) - min(color_houses) <= 1
                            if check1 == True and check2 == True and (self.cash - total_price >= 0 or total_price <= 0):
                                clear()
                                for prop in properties_in_color:
                                    get_square = BOARD[prop]
                                    get_square.houses += added_houses[prop]
                                self.cash -= total_price
                                print(self)
                                print('\nTransaction successful.')
                                input('')
                                clear()
                                houses = leftover_houses
                                hotels = leftover_hotels
                                break
                            elif check1 == False:
                                clear()
                                print(self)
                                print('\nInsufficient houses and hotels.')
                                input('')
                                clear()
                            elif check2 == False:
                                clear()
                                print(self)
                                print('\nInvalid configuration. A square in a color set may not have more than one house more than any other square in the same set')
                                input('')
                                clear()
                            else:
                                clear()
                                print(self)
                                print('\nYou do not have enough cash for this transaction.')
                                input('')
                                clear()
                        elif y == 'c' or y == 'C':
                            clear()
                            break
                        else:
                            prop = int(y)
                            get_square = BOARD[prop]
                            z = input('Enter number of houses: ')
                            try:
                                number = int(z)
                                
                                if 0 <= get_square.houses + added_houses[prop] + number <= 5:
                                    added_houses[prop] += number
                                    if number > 0:
                                        print('You added {} houses on {}'.format(number, get_square.name))
                                    elif number < 0:
                                        print('You removed {} houses from {}'.format(-number, get_square.name))
                                else:
                                    print('\nInvalid input. A property may have up to 5 houses (a hotel)')
                            except ValueError:
                                print('\nInvalid input. Must be an integer')
                    else:
                        print('\nInvalid input.')
                    input('')
                    clear()
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
                mortgageable = True
                if isinstance(BOARD[prop], Land):
                    for land in BOARD[prop].full_set():
                        if land.houses == 0:
                            continue
                        else:
                            mortgageable = False
                            break
                if mortgageable == True:
                    options.append(prop)
                    if BOARD[prop].mortgaged == True:
                        mortgage_status = ' (Mortgaged)'
                        price = int(BOARD[prop].mortgage * 1.1)
                    elif BOARD[prop].mortgaged == False:
                        mortgage_status = ''
                        price = BOARD[prop].mortgage
                    print('{} - {}{} - Mortgage/Unmortgage Price: ${}'.format(prop, BOARD[prop].name, mortgage_status, price))
            try:
                x_input = input('>>> ')
                if x_input == '':
                    x = 0
                else:
                    x = int(x_input)
                    
                if x == 0:
                    break
                else:
                    if x in options:
                        if BOARD[x].mortgaged == False:
                            self.cash += BOARD[x].mortgage
                            BOARD[x].mortgage_prop()
                        elif BOARD[x].mortgaged == True:
                            if self.cash - int(BOARD[x].mortgage * 1.1) < 0:
                                print('\nYou do not have enough cash to unmortgage this property.')
                            else:
                                self.cash -= int(BOARD[x].mortgage * 1.1)
                                BOARD[x].mortgage_prop()
                    else:
                        print('\nYou do not own this property, or this property is not mortgageable. Remove all houses in the color group before mortgaging')
                    input('')
                    clear()
                
            except ValueError:
                print('\nInvalid input. Must be an integer or blank')
                input('')
                clear()
    
    def get_chance(self):
        print(self)
        while True:
            x = randint(0,15)
            if self.get_out_of_jail_free_chance_used == True and x == 6:
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
            if self.get_out_of_jail_free_chest_used == True and x == 4:
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
        self.repeat_turn = False
        
    def out_of_jail(self):
        print('\nYou are now out of jail.')
        self.injail = False
        self.square = 10