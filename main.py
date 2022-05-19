# This module starts the game
try:
    from game import Game

    house_limited = True

    main_game = Game(house_limited=house_limited)
    
    main_game.main()
except ModuleNotFoundError:
    print('Module colorit not found. Please install module color-it before running')
    input()