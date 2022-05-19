# This module stores the data and functions for the board and properties

from colorit import init_colorit, color, background
init_colorit()

class Square:
    def __init__(self,name):
        self.name = name
        
class Property(Square):
    def __init__(self,name,price,mortgage):
        super().__init__(name)
        self.price = price
        self.mortgage = mortgage
        self.owner = None
        self.mortgaged = False
        
    def mortgage_prop(self):
        # Mortgage or unmortgage a property
        if self.mortgaged == False:
            print('You mortgaged {} for ${}'.format(self.name,self.mortgage))
            self.mortgaged = True
        elif self.mortgaged == True:
            # Unmortgage cost is 10% more than mortgage value
            unmortgage_value = int(self.mortgage*1.1)
            print('You unmortgaged {} for ${}'.format(self.name,unmortgage_value))
            self.mortgaged = False

class Land(Property):
    def __init__(self,name,color,price,rents,house_price,mortgage):
        super().__init__(name,price,mortgage)
        self.color = color
        self.rents = rents
        self.mortgage = mortgage
        self.house_price = house_price
        self.houses = 0
        
    def full_set(self):
        return LAND_COLORS[self.color]
    
    def full_set_owned(self):
        # Test if player owns all properties in the same set as current
        for prop in LAND_COLORS[self.color]:
            if prop.owner != self.owner:
                return False
        return True
    
    def get_rent(self):
        if self.houses == 0 and self.full_set_owned() == True:
            return self.rents[0] * 2
        else:
            return self.rents[self.houses]
    
    def __str__(self):
        if self.mortgaged == False:
            card_print = color(background('{name}'.format(name=self.name), BG_COLORS[self.color]),FG_COLORS[self.color]) + \
"""
Price              : ${price}

Rent               : ${rent}
Rent with 1 House  : ${rent1}
Rent with 2 Houses : ${rent2}
Rent with 3 Houses : ${rent3}
Rent with 4 Houses : ${rent4}
Rent with Hotel    : ${renthotel}
Mortgage Value     : ${mortgage}

Houses cost ${house} each
Hotels, ${house}, plus 4 houses

If a player owns all the lots of any Color-Group,
the rent is doubled on unimproved lots in that group"""\
            .format(price=self.price, mortgage=self.mortgage,\
            rent=self.rents[0], rent1=self.rents[1], rent2=self.rents[2],\
            rent3=self.rents[3], rent4=self.rents[4], renthotel=self.rents[5],\
            house=self.house_price)
    
            return card_print
        
        elif self.mortgaged == True:
            card_print = \
"""{name}
Mortgaged for ${mortgage}

Card must be turned this side up if property is mortgaged"""\
            .format(name=self.name, mortgage=self.mortgage)
            
            return card_print
        
class Railroad(Property):
    def __init__(self,name):
        super().__init__(name,200,100)
        
    def get_rent(self):
        railroads_owned = 0
        for railroad in RAILROADS:
            if railroad.owner == self.owner:
                railroads_owned += 1
        
        if railroads_owned == 1:
            return 25
        elif railroads_owned == 2:
            return 50
        elif railroads_owned == 3:
            return 100
        elif railroads_owned == 4:
            return 200
        
    def __str__(self):
        if self.mortgaged == False:
            card_print = color(background('{name}'.format(name=self.name), (255,255,255)),(0,0,0)) + \
"""
Price                : ${price}
Rent                 : $25
If 2 Railroads owned : $50
If 3 Railroads owned : $100
If 4 Railroads owned : $200
Mortgage Value       : ${mortgage}"""\
            .format(price=self.price, mortgage=self.mortgage)
    
            return card_print
        
        elif self.mortgaged == True:
            card_print = \
"""{name}
Mortgaged for ${mortgage}

Card must be turned this side up if property is mortgaged"""\
            .format(name=self.name, mortgage=self.mortgage)
            
            return card_print
        
class Utility(Property):
    def __init__(self,name):
        super().__init__(name,150,75)
    
    def rent_factor(self):
        utilities_owned = 0
        for utility in UTILITIES:
            if utility.owner == self.owner:
                utilities_owned += 1
        
        if utilities_owned == 1:
            return 4
        elif utilities_owned == 2:
            return 10
    
    def __str__(self):
        if self.mortgaged == False:
            card_print = color(background('{name}'.format(name=self.name), (192,192,192)),(0,0,0)) + \
"""
Price          : ${price}

If one utility is owned, rent is 4 times
amount shown on dice.

If both utilities are owned, rent is 10 times
amount shown on dice.

Mortgage Value : ${mortgage}"""\
            .format(price=self.price, mortgage=self.mortgage)
    
            return card_print
        
        elif self.mortgaged == True:
            card_print = \
"""{name}
Mortgaged for ${mortgage}

Card must be turned this side up if property is mortgaged"""\
            .format(name=self.name, mortgage=self.mortgage)
            
            return card_print

RAILROADS = [Railroad('Reading Railroad'),
             Railroad('Pennsylvania Railroad'),
             Railroad('B&O Railroad'),
             Railroad('Short Line')]

UTILITIES = [Utility('Electric Company'),
             Utility('Water Works')]

LAND_COLORS = {'brown':     [Land('Mediterranean Avenue',   'brown',
                                   60,[ 2, 10, 30,  90, 160, 250], 50, 30),
                             Land('Baltic Avenue',          'brown',
                                   60,[ 4, 20, 60, 180, 320, 450], 50, 30)],
               'light blue':[Land('Oriental Avenue',        'light blue',
                                  100,[ 6, 30, 90, 270, 400, 550], 50, 50),
                             Land('Vermont Avenue',         'light blue',
                                  100,[ 6, 30, 90, 270, 400, 550], 50, 50),
                             Land('Connecticut Avenue',     'light blue',
                                  120,[ 8, 40,100, 300, 450, 600], 50, 60)],
               'pink':      [Land('St. Charles Place',      'pink',
                                  140,[10, 50,150, 450, 625, 750],100, 70),
                             Land('States Avenue',          'pink',
                                  140,[10, 50,150, 450, 625, 750],100, 70),
                             Land('Virginia Avenue',        'pink',
                                  160,[12, 60,180, 500, 700, 900],100, 80)],
               'orange':    [Land('St. James Place',        'orange',
                                  180,[14, 70,200, 550, 750, 950],100, 90),
                             Land('Tennessee Avenue',       'orange',
                                  180,[14, 70,200, 550, 750, 950],100, 90),
                             Land('New York Avenue',        'orange',
                                  200,[16, 80,220, 600, 800,1000],100,100)],
               'red':       [Land('Kentucky Avenue',        'red',
                                  220,[18, 90,250, 700, 875,1050],150,110),
                             Land('Indiana Avenue',         'red',
                                  220,[18, 90,250, 700, 875,1050],150,110),
                             Land('Illinois Avenue',        'red',
                                  240,[20,100,300, 750, 925,1100],150,120)],
               'yellow':    [Land('Atlantic Avenue',        'yellow',
                                  260,[22,110,330, 800, 975,1150],150,130),
                             Land('Ventnor Avenue',         'yellow',
                                  260,[22,110,330, 800, 975,1150],150,130),
                             Land('Marvin Gardens',         'yellow',
                                  280,[24,120,360, 850,1025,1200],150,140)],
               'green':     [Land('Pacific Avenue',         'green',
                                  300,[26,130,390, 900,1100,1275],200,150),
                             Land('North Carolina Avenue',  'green',
                                  300,[26,130,390, 900,1100,1275],200,150),
                             Land('Pennsylvania Avenue',    'green',
                                  320,[28,150,450,1000,1200,1400],200,160)],
               'blue':      [Land('Park Place',             'blue',
                                  350,[35,175,500,1100,1300,1500],200,175),
                             Land('Boardwalk',              'blue',
                                  400,[50,200,600,1400,1700,2000],200,200)]}

BOARD = {0: Square('Go'),
         1: LAND_COLORS['brown'][0],
         2: Square('Community Chest'),
         3: LAND_COLORS['brown'][1],
         4: Square('Income Tax'),
         5: RAILROADS[0],
         6: LAND_COLORS['light blue'][0],
         7: Square('Chance'),
         8: LAND_COLORS['light blue'][1],
         9: LAND_COLORS['light blue'][2],
         10: Square('Jail (Just Visiting)'),
         11: LAND_COLORS['pink'][0],
         12: UTILITIES[0],
         13: LAND_COLORS['pink'][1],
         14: LAND_COLORS['pink'][2],
         15: RAILROADS[1],
         16: LAND_COLORS['orange'][0],
         17: Square('Community Chest'),
         18: LAND_COLORS['orange'][1],
         19: LAND_COLORS['orange'][2],
         20: Square('Free Parking'),
         21: LAND_COLORS['red'][0],
         22: Square('Chance'),
         23: LAND_COLORS['red'][1],
         24: LAND_COLORS['red'][2],
         25: RAILROADS[2],
         26: LAND_COLORS['yellow'][0],
         27: LAND_COLORS['yellow'][1],
         28: UTILITIES[1],
         29: LAND_COLORS['yellow'][2],
         30: Square('Go To Jail'),
         31: LAND_COLORS['green'][0],
         32: LAND_COLORS['green'][1],
         33: Square('Community Chest'),
         34: LAND_COLORS['green'][2],
         35: RAILROADS[3],
         36: Square('Chance'),
         37: LAND_COLORS['blue'][0],
         38: Square('Luxury Tax'),
         39: LAND_COLORS['blue'][1]}

BG_COLORS = {'brown': (148,75,33),
             'light blue': (148,224,227),
             'pink': (232,14,156),
             'orange': (240,137,12),
             'red': (232,36,14),
             'yellow': (247,232,20),
             'green': (13,181,91),
             'blue': (6,105,186)}

FG_COLORS = {'brown': (255,255,255),
             'light blue': (0,0,0),
             'pink': (0,0,0),
             'orange': (0,0,0),
             'red': (255,255,255),
             'yellow': (0,0,0),
             'green': (255,255,255),
             'blue': (255,255,255)}