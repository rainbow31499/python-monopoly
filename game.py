# This module manages and runs the overall game

from property_data import BOARD, Land
from player_functions import Player

import os
from random import randint
from colorit import init_colorit, color

clear = lambda: os.system('cls')

init_colorit()

class Game:
    def __init__(self, house_limited):
        self.house_limited = house_limited
    
    def main(self):
        clear()
        # Game running function
        print('Python Monopoly\nVersion June 28, 2021\nby Ray Ng (done by myself)\n\nPress Enter to start')
        input('')
        clear()
        self.start()
    
    def start(self):
        # Start the game (initialize Game options)
        while True:
            x = input('Enter number of players: ')
            try:
                self.nop = int(x)
                clear()
                break
            except ValueError:
                print('\nInvalid input. Must be a number')
                input('')
                clear()

        while True:
            y = input('Enter starting cash or leave blank for default (Default is $1500): ')
            try:
                if y == '':
                    start_cash = 1500
                else:
                    start_cash = int(y)
                clear()
                break
            except ValueError:
                print('\nPlease enter a valid input. Must be a number or blank\n')
                input('')
                clear()
        
        self.running = True
        
        self.players = [Player(x,cash=start_cash) for x in range(self.nop)]
        
        self.board = BOARD
        self.get_out_of_jail_free_chance = None
        self.get_out_of_jail_free_chest = None
        
        if self.house_limited == True:
            self.total_houses = 32
            self.total_hotels = 12
        elif self.house_limited == False:
            self.total_houses = float('inf')
            self.total_hotels = float('inf')
            
        self.houses = self.total_houses
        self.hotels = self.total_hotels
        
        self.turn = randint(0,self.nop-1) # Start with a random player
        print('Player {} starts. Press Enter to continue'.format(self.turn+1))
        input('')
        clear()
        
        while self.running == True:
            self.run_turn()

    def run_turn(self):
        # Run each turn
        
        current_player = self.players[self.turn]
        
        if self.get_out_of_jail_free_chance == None:
            current_player.get_out_of_jail_free_chance_used = False
        else:
            current_player.get_out_of_jail_free_chance_used = True
        if self.get_out_of_jail_free_chest == None:
            current_player.get_out_of_jail_free_chest_used = False
        else:
            current_player.get_out_of_jail_free_chest_used = True
        
        if current_player.bankrupt == True:
            # Skip player if bankrupt
            print('Player {} is bankrupt'.format(self.turn+1))
            self.turn = (self.turn+1) % self.nop
            print('Pass turn to Player {}'.format(self.turn+1))
            input('')
            clear()
        else:
            # Choose an option
            while True:
                print(current_player)
                if current_player.cash < 0:
                    print('\nWarning: You are running low on cash. Please mortgage properties or sell houses before rolling')
                print('\nPlease select option:')
                if current_player.cash >= 0:
                    print('0 or blank --- Roll Dice')
                else:
                    print(color('0 or blank --- Roll Dice', (128,128,128)))
                print('1 ------------ View Properties')
                print('2 ------------ Trade Properties')
                print('3 ------------ Build Houses')
                print('4 ------------ Mortgage Properties')
                print('5 ------------ Quit (Declare Bankruptcy)')
                if current_player.cash < 0:
                    options = ['1','2','3','4','5']
                else:
                    options = ['0','1','2','3','4','5','']
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
                print(current_player)
                # Roll dice
                current_player.roll_dice()
                # Pay outstanding owed amounts
                for payment in current_player.payments:
                    if payment[0] == 'all':
                        for player in range(self.nop):
                            if self.players[player].bankrupt == False:
                                current_player.cash -= payment[1]
                                self.players[player].cash += payment[1]
                    else:
                        if self.players[payment[0]].bankrupt == False:
                            current_player.cash -= payment[1]
                            self.players[payment[0]].cash += payment[1]
                        else:
                            print('Player {} is bankrupt'.format(payment[0]+1))
                current_player.payments = []
                
                # Update Get Out Of Jail Free Status
                if current_player.get_out_of_jail_free_chance == True:
                    self.get_out_of_jail_free_chance = current_player.no
                if current_player.get_out_of_jail_free_chance == False and self.get_out_of_jail_free_chance == current_player.no:
                    self.get_out_of_jail_free_chance = None
                    
                if current_player.get_out_of_jail_free_chest == True:
                    self.get_out_of_jail_free_chest = current_player.no
                if current_player.get_out_of_jail_free_chest == False and self.get_out_of_jail_free_chest == current_player.no:
                    self.get_out_of_jail_free_chest = None
                
                input('')
                clear()
                
                # Transfer turn to next player
                if current_player.repeat_turn == False:
                    self.turn = (self.turn + 1) % self.nop
                    print('\nPass turn to Player {}'.format(self.turn+1))
                else:
                    print('\nPlay again')
                input('')
                clear()
            
            elif opt == '1':
                print(current_player)
                print('\nOwned properties:\n')
                for prop in current_player.owned_props:
                    print(str(self.board[prop]) + '\n\n--------------------\n')
                if self.get_out_of_jail_free_chance == self.turn:
                    print('Get Out Of Jail Free Card -\nMay be kept until needed or sold/traded (Chance)')
                if self.get_out_of_jail_free_chest == self.turn:
                    print('Get Out Of Jail Free Card -\nMay be kept until needed or sold/traded (Community Chest)')
                print('\nPress Enter to continue')
                input('')
                clear()
            
            elif opt == '2':
                # Step 1: Select a player to trade with
                player_options = ['0', '']
                for player in self.players:
                    if player.no != current_player.no and player.bankrupt == False:
                        player_options.append(str(player.no+1))
                while True:
                    print('Player {}'.format(self.turn+1))
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
                        print('Player {}'.format(self.turn+1))
                        print('\nYou have decided to offer Player {}:'.format(trader))
                        for prop in traded_items:
                            if prop in current_player.owned_props:
                                print('{} - {}'.format(prop, self.board[prop].name))
                            elif prop == 41:
                                if self.get_out_of_jail_free_chance == current_player.no:
                                    print('41 - Get Out Of Jail Free Card - Chance')
                            elif prop == 42:
                                if self.get_out_of_jail_free_chest == current_player.no:
                                    print('42 - Get Out Of Jail Free Card - Community Chest')
                        if cash_exchange > 0:
                            print('Cash: ${}'.format(cash_exchange))
                        print('\nIn exchange for:')
                        for prop in traded_items:
                            if prop in trading_player.owned_props:
                                print('{} - {}'.format(prop, self.board[prop].name))
                            elif prop == 41:
                                if self.get_out_of_jail_free_chance == trading_player.no:
                                    print('41 - Get Out Of Jail Free Card - Chance')
                            elif prop == 42:
                                if self.get_out_of_jail_free_chest == trading_player.no:
                                    print('42 - Get Out Of Jail Free Card - Community Chest')
                        if cash_exchange < 0:
                            print('Cash: ${}'.format(-cash_exchange))
                                
                        print('\nChoose properties to trade, or enter to delete items above:')
                        trading_options = ['0', '', '50']
                        print('0 or blank - Continue')
                        print('Owned by you:')
                        for prop in current_player.owned_props:
                            if self.board[prop].mortgaged == False:
                                if prop not in traded_items:
                                    print('{} - {}'.format(prop, self.board[prop].name))
                                trading_options.append(str(prop))
                        if self.get_out_of_jail_free_chance == current_player.no:
                            if 41 not in traded_items:
                                print('41 - Get Out Of Jail Free Card - Chance')
                            trading_options.append('41')
                        if self.get_out_of_jail_free_chest == current_player.no:
                            if 42 not in traded_items:
                                print('42 - Get Out Of Jail Free Card - Community Chest')
                            trading_options.append('42')
                        print('Cash: ${}'.format(current_player.cash))
                        print('Owned by Player {}'.format(trader))
                        for prop in trading_player.owned_props:
                            if self.board[prop].mortgaged == False:
                                if prop not in traded_items:
                                    print('{} - {}'.format(prop, self.board[prop].name))
                                trading_options.append(str(prop))
                        if self.get_out_of_jail_free_chance == trading_player.no:
                            if 41 not in traded_items:
                                print('41 - Get Out Of Jail Free Card - Chance')
                            trading_options.append('41')
                        if self.get_out_of_jail_free_chest == trading_player.no:
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
                    if traded_items != []:
                        print('Pass turn to Player {}'.format(trading_player.no+1))
                        input('')
                        clear()
                        while True:
                            print('Player {}'.format(trading_player.no+1))
                            print('Current cash: ${}'.format(trading_player.cash))
                            print('\nPlayer {} offers:'.format(current_player.no+1))
                            for prop in traded_items:
                                if prop in current_player.owned_props:
                                    print('{} - {}'.format(prop, self.board[prop].name))
                                elif prop == 41:
                                    if self.get_out_of_jail_free_chance == current_player.no:
                                        print('41 - Get Out Of Jail Free Card - Chance')
                                elif prop == 42:
                                    if self.get_out_of_jail_free_chest == current_player.no:
                                        print('42 - Get Out Of Jail Free Card - Community Chest')
                            if cash_exchange > 0:
                                print('Cash: ${}'.format(cash_exchange))
                            print('In exchange for:')
                            for prop in traded_items:
                                if prop in trading_player.owned_props:
                                    print('{} - {}'.format(prop, self.board[prop].name))
                                elif prop == 41:
                                    if self.get_out_of_jail_free_chance == trading_player.no:
                                        print('41 - Get Out Of Jail Free Card - Chance')
                                elif prop == 42:
                                    if self.get_out_of_jail_free_chest == trading_player.no:
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
                                        if self.get_out_of_jail_free_chance == current_player.no:
                                            current_player.get_out_of_jail_free_chance = False
                                            trading_player.get_out_of_jail_free_chance = True
                                            self.get_out_of_jail_free_chance = trading_player.no
                                        elif self.get_out_of_jail_free_chance == trading_player.no:
                                            current_player.get_out_of_jail_free_chance = True
                                            trading_player.get_out_of_jail_free_chance = False
                                            self.get_out_of_jail_free_chance = current_player.no
                                    elif prop == 42:
                                        if self.get_out_of_jail_free_chest == current_player.no:
                                            current_player.get_out_of_jail_free_chest = False
                                            trading_player.get_out_of_jail_free_chest = True
                                            self.get_out_of_jail_free_chest = trading_player.no
                                        elif self.get_out_of_jail_free_chest == trading_player.no:
                                            current_player.get_out_of_jail_free_chest = True
                                            trading_player.get_out_of_jail_free_chest = False
                                            self.get_out_of_jail_free_chest = current_player.no
                                    else:
                                        if prop in current_player.owned_props:
                                            current_player.owned_props.remove(prop)
                                            trading_player.owned_props.append(prop)
                                            trading_player.owned_props.sort()
                                            self.board[prop].owner = trading_player.no
                                        elif prop in trading_player.owned_props:
                                            trading_player.owned_props.remove(prop)
                                            current_player.owned_props.append(prop)
                                            current_player.owned_props.sort()
                                            self.board[prop].owner = current_player.no
                                            
                                current_player.cash -= cash_exchange
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
    
            elif opt == '3':
                current_player.build_houses(self.houses,self.hotels,self.house_limited)
                self.houses = self.total_houses
                self.hotels = self.total_hotels
                for prop in self.board:
                    if isinstance(self.board[prop], Land):
                        if self.board[prop].houses == 5:
                            self.hotels -= 1
                        else:
                            self.houses -= self.board[prop].houses
                clear()
    
            elif opt == '4':
                current_player.mortgage_properties()
                clear()
    
            elif opt == '5':
                print('\nYou have declared bankruptcy and left the game')
                current_player.bankrupt = True
                for prop in current_player.owned_props:
                    self.board[prop].owner = None
                    self.board[prop].mortgaged = False
                    if isinstance(self.board[prop], Land):
                        self.board[prop].houses = 0
                if self.get_out_of_jail_free_chance == current_player.no:
                    self.get_out_of_jail_free_chance = None
                if self.get_out_of_jail_free_chest == current_player.no:
                    self.get_out_of_jail_free_chest = None
                input('')
                clear()
                    
        # End game if all bankrupt
        if all([player.bankrupt for player in self.players]):
            print('\nAll players bankrupt. Game ended.\n\nPress Enter to exit')
            input('')
            clear()
            self.running = False