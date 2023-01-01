# This module manages and runs the overall game

from property_data import BOARD, Land
from player_functions import Player

import os
from random import randint
from colorit import init_colorit, color

clear = lambda: os.system('cls')

init_colorit()

class Game:
    def __init__(self):
        pass
    
    def main(self):
        clear()
        # Game running function
        print('Python Monopoly\nVersion December 31, 2022\nby Ray Ng (done by myself)\n\nPress Enter to start')
        input('')
        clear()
        self.start()
    
    def start(self):
        # Start the game (initialize Game settings with user input)
        while True:
            opt = input('Enter number of players: ')
            try:
                self.no_of_players = int(opt)
                clear()
                break
            except ValueError:
                print('\nInvalid input. Must be a number')
                input('')
                clear()

        while True:
            opt = input('Enter starting cash or leave blank for default (Default is $1500): ')
            try:
                if opt == '':
                    start_cash = 1500
                else:
                    start_cash = int(opt)
                clear()
                break
            except ValueError:
                print('\nPlease enter a valid input. Must be a number or blank\n')
                input('')
                clear()

        while True:
            print('Play with limited houses?')
            print('0 - No')
            print('1 - Yes')
            opt = input('>>> ')

            if opt == '0':
                self.house_limited = False
                clear()
                break
            elif opt == '1':
                self.house_limited = True
                clear()
                break
            else:
                print('\nPlease enter a valid input. Must be a number or blank\n')
                input('')
                clear()
                continue

        # Initialize game variables
        self.running = True # Shows game is running and can play the next turn

        self.players = []

        for p in range(self.no_of_players):
            player = Player(p,cash=start_cash)
            player.game = self
            self.players.append(player)
        
        self.board = BOARD
        self.get_out_of_jail_free_chance = None # Is the Get Out of Jail Free (Chance) card owned by a player? If yes, player number (0-based), if no, None
        self.get_out_of_jail_free_chest = None # Is the Get Out of Jail Free (Community Chest) card owned by a player?
        
        if self.house_limited == True:
            self.total_houses = 32
            self.total_hotels = 12
        elif self.house_limited == False:
            self.total_houses = float('inf')
            self.total_hotels = float('inf')
            
        self.houses = self.total_houses # Houses in bank
        self.hotels = self.total_hotels # Hotels in bank
        
        self.turn = randint(0,self.no_of_players-1) # Start with a random player, indicate whose turn it is
        print('Player {} starts. Press Enter to continue'.format(self.turn+1))
        input('')
        clear()

        self.run_game()
    
    def run_game(self):
        while self.running == True:
            self.run_turn()
            # End game if all bankrupt
            if all([player.bankrupt for player in self.players]):
                print('\nAll players bankrupt. Game ended.\n\nPress Enter to exit')
                input('')
                clear()
                self.running = False

    def run_turn(self):
        # Run each turn
        
        self.players[self.turn].run_turn()

    def end(self):
        print('\nAll players bankrupt. Game ended.\n\nPress Enter to exit')
        input('')
        clear()
        self.running = False