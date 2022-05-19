# This module starts the game

from game import Game

house_limited = True

main_game = Game(house_limited=house_limited)

try:
    main_game.main()
except ModuleNotFoundError:
    print('Module colorit not found. Please install module before running')
    input()