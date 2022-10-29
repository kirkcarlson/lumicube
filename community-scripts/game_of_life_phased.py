# Run Conway's Game of Life (https://en.wikipedia.org/wiki/Conway's_Game_of_Life)
# based on the AbstractFoundry code
# modified by Kirk Carlson
#   phased transitions between generations
#   allow generations to proceed to annihilation, stability or oscillation
#      while emphasizing the end


#### IMPORTS ####
import random
import os

#### UNIT TEST FUNCTION ####
alive_top_vert = [(0,9), (0,10), (0,11), (7,9), (7,10), (7,11)]
alive_left_vert = [(0,1), (0,2), (0,3), (7,1), (7,2), (7,3)]
alive_right_hor = [(9,0), (10,0), (11,0), (9,7), (10,7), (11,7)]
alive_left_ne = [(7,7)]
alive_left_se = [(7,0)]
alive_left_sw = [(0,0)]
alive_left_nw = [(0,7)]
alive_right_ne = [(15,7)]
alive_right_se = [(15,0)]
alive_right_sw = [(8,0)]
alive_right_nw = [(8,7)]
alive_top_ne = [(7,15)]
alive_top_se = [(7,8)]
alive_top_sw = [(0,8)]
alive_top_nw = [(0,15)]
num_alive_tests = [
        # { alive_cells:[(x,y)...], x:int, y:int, wrap: bool, expect: int}
        { "alive_cells": alive_top_vert, "x":7, "y":8,  "wrap":False, "expect":1 },
        { "alive_cells": alive_top_vert, "x":7, "y":9,  "wrap":False, "expect":1 },
        { "alive_cells": alive_top_vert, "x":7, "y":10, "wrap":False, "expect":2 },
        { "alive_cells": alive_top_vert, "x":7, "y":11, "wrap":False, "expect":1 },
        { "alive_cells": alive_top_vert, "x":7, "y":12, "wrap":False, "expect":1 },
        { "alive_cells": alive_top_vert, "x":0, "y":8,  "wrap":False, "expect":1 },
        { "alive_cells": alive_top_vert, "x":0, "y":9,  "wrap":False, "expect":1 },
        { "alive_cells": alive_top_vert, "x":0, "y":10, "wrap":False, "expect":2 },
        { "alive_cells": alive_top_vert, "x":0, "y":11, "wrap":False, "expect":1 },
        { "alive_cells": alive_top_vert, "x":0, "y":12, "wrap":False, "expect":1 },

        { "alive_cells": alive_top_vert, "x":7, "y":8,  "wrap":True, "expect":1 },
        { "alive_cells": alive_top_vert, "x":7, "y":9,  "wrap":True, "expect":1 },
        { "alive_cells": alive_top_vert, "x":7, "y":10, "wrap":True, "expect":2 },
        { "alive_cells": alive_top_vert, "x":7, "y":11, "wrap":True, "expect":1 },
        { "alive_cells": alive_top_vert, "x":7, "y":12, "wrap":True, "expect":1 },
        { "alive_cells": alive_top_vert, "x":0, "y":8,  "wrap":True, "expect":1 },
        { "alive_cells": alive_top_vert, "x":0, "y":9,  "wrap":True, "expect":1 },
        { "alive_cells": alive_top_vert, "x":0, "y":10, "wrap":True, "expect":2 },
        { "alive_cells": alive_top_vert, "x":0, "y":11, "wrap":True, "expect":1 },
        { "alive_cells": alive_top_vert, "x":0, "y":12, "wrap":True, "expect":1 },

        { "alive_cells": alive_top_vert, "x":8,  "y":7, "wrap":True, "expect":1 },
        { "alive_cells": alive_top_vert, "x":9,  "y":7, "wrap":True, "expect":2 },
        { "alive_cells": alive_top_vert, "x":10, "y":7, "wrap":True, "expect":3 },
        { "alive_cells": alive_top_vert, "x":11, "y":7, "wrap":True, "expect":2 },
        { "alive_cells": alive_top_vert, "x":12, "y":7, "wrap":True, "expect":1 },
        { "alive_cells": alive_top_vert, "x":8,  "y":0, "wrap":True, "expect":1 },
        { "alive_cells": alive_top_vert, "x":9,  "y":0, "wrap":True, "expect":2 },
        { "alive_cells": alive_top_vert, "x":10, "y":0, "wrap":True, "expect":3 },
        { "alive_cells": alive_top_vert, "x":11, "y":0, "wrap":True, "expect":2 },
        { "alive_cells": alive_top_vert, "x":12, "y":0, "wrap":True, "expect":1 },

        { "alive_cells": alive_left_vert, "x":7, "y":0, "wrap":False, "expect":1 },
        { "alive_cells": alive_left_vert, "x":7, "y":1, "wrap":False, "expect":1 },
        { "alive_cells": alive_left_vert, "x":7, "y":2, "wrap":False, "expect":2 },
        { "alive_cells": alive_left_vert, "x":7, "y":3, "wrap":False, "expect":1 },
        { "alive_cells": alive_left_vert, "x":7, "y":4, "wrap":False, "expect":1 },
        { "alive_cells": alive_left_vert, "x":0, "y":0, "wrap":False, "expect":1 },
        { "alive_cells": alive_left_vert, "x":0, "y":1, "wrap":False, "expect":1 },
        { "alive_cells": alive_left_vert, "x":0, "y":2, "wrap":False, "expect":2 },
        { "alive_cells": alive_left_vert, "x":0, "y":3, "wrap":False, "expect":1 },
        { "alive_cells": alive_left_vert, "x":0, "y":4, "wrap":False, "expect":1 },

        { "alive_cells": alive_left_vert, "x":7, "y":0, "wrap":True, "expect":1 },
        { "alive_cells": alive_left_vert, "x":7, "y":1, "wrap":True, "expect":1 },
        { "alive_cells": alive_left_vert, "x":7, "y":2, "wrap":True, "expect":2 },
        { "alive_cells": alive_left_vert, "x":7, "y":3, "wrap":True, "expect":1 },
        { "alive_cells": alive_left_vert, "x":7, "y":4, "wrap":True, "expect":1 },
        { "alive_cells": alive_left_vert, "x":0, "y":0, "wrap":True, "expect":1 },
        { "alive_cells": alive_left_vert, "x":0, "y":1, "wrap":True, "expect":1 },
        { "alive_cells": alive_left_vert, "x":0, "y":2, "wrap":True, "expect":2 },
        { "alive_cells": alive_left_vert, "x":0, "y":3, "wrap":True, "expect":1 },
        { "alive_cells": alive_left_vert, "x":0, "y":4, "wrap":True, "expect":1 },

        { "alive_cells": alive_left_vert, "x":8,  "y":0, "wrap":True, "expect":1 },
        { "alive_cells": alive_left_vert, "x":8,  "y":1, "wrap":True, "expect":2 },
        { "alive_cells": alive_left_vert, "x":8,  "y":2, "wrap":True, "expect":3 },
        { "alive_cells": alive_left_vert, "x":8,  "y":3, "wrap":True, "expect":2 },
        { "alive_cells": alive_left_vert, "x":8,  "y":4, "wrap":True, "expect":1 },
        { "alive_cells": alive_left_vert, "x":15, "y":0, "wrap":True, "expect":1 },
        { "alive_cells": alive_left_vert, "x":15, "y":1, "wrap":True, "expect":2 },
        { "alive_cells": alive_left_vert, "x":15, "y":2, "wrap":True, "expect":3 },
        { "alive_cells": alive_left_vert, "x":15, "y":3, "wrap":True, "expect":2 },
        { "alive_cells": alive_left_vert, "x":15, "y":4, "wrap":True, "expect":1 },


        { "alive_cells": alive_right_hor, "x":8,  "y":0, "wrap":False, "expect":1 },
        { "alive_cells": alive_right_hor, "x":9,  "y":0, "wrap":False, "expect":1 },
        { "alive_cells": alive_right_hor, "x":10, "y":0, "wrap":False, "expect":2 },
        { "alive_cells": alive_right_hor, "x":11, "y":0, "wrap":False, "expect":1 },
        { "alive_cells": alive_right_hor, "x":12, "y":0, "wrap":False, "expect":1 },
        { "alive_cells": alive_right_hor, "x":8,  "y":7, "wrap":False, "expect":1 },
        { "alive_cells": alive_right_hor, "x":9,  "y":7, "wrap":False, "expect":1 },
        { "alive_cells": alive_right_hor, "x":10, "y":7, "wrap":False, "expect":2 },
        { "alive_cells": alive_right_hor, "x":11, "y":7, "wrap":False, "expect":1 },
        { "alive_cells": alive_right_hor, "x":12, "y":7, "wrap":False, "expect":1 },

        { "alive_cells": alive_right_hor, "x":8,  "y":0, "wrap":True, "expect":1 },
        { "alive_cells": alive_right_hor, "x":9,  "y":0, "wrap":True, "expect":1 },
        { "alive_cells": alive_right_hor, "x":10, "y":0, "wrap":True, "expect":2 },
        { "alive_cells": alive_right_hor, "x":11, "y":0, "wrap":True, "expect":1 },
        { "alive_cells": alive_right_hor, "x":12, "y":0, "wrap":True, "expect":1 },
        { "alive_cells": alive_right_hor, "x":8,  "y":7, "wrap":True, "expect":1 },
        { "alive_cells": alive_right_hor, "x":9,  "y":7, "wrap":True, "expect":1 },
        { "alive_cells": alive_right_hor, "x":10, "y":7, "wrap":True, "expect":2 },
        { "alive_cells": alive_right_hor, "x":11, "y":7, "wrap":True, "expect":1 },
        { "alive_cells": alive_right_hor, "x":12, "y":7, "wrap":True, "expect":1 },

        { "alive_cells": alive_right_hor, "x":7,  "y":8,  "wrap":True, "expect":1 },
        { "alive_cells": alive_right_hor, "x":7,  "y":9,  "wrap":True, "expect":2 },
        { "alive_cells": alive_right_hor, "x":7,  "y":10, "wrap":True, "expect":3 },
        { "alive_cells": alive_right_hor, "x":7,  "y":11, "wrap":True, "expect":2 },
        { "alive_cells": alive_right_hor, "x":7,  "y":12, "wrap":True, "expect":1 },
        { "alive_cells": alive_right_hor, "x":0,  "y":8,  "wrap":True, "expect":1 },
        { "alive_cells": alive_right_hor, "x":0,  "y":9,  "wrap":True, "expect":2 },
        { "alive_cells": alive_right_hor, "x":0,  "y":10, "wrap":True, "expect":3 },
        { "alive_cells": alive_right_hor, "x":0,  "y":11, "wrap":True, "expect":2 },
        { "alive_cells": alive_right_hor, "x":0,  "y":12, "wrap":True, "expect":1 },

        { "alive_cells": alive_left_ne, "x":0,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_ne, "x":0,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_ne, "x":0,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_ne, "x":0,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_left_ne, "x":7,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_ne, "x":7,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_ne, "x":7,  "y":8,  "wrap":False, "expect":1 },
        { "alive_cells": alive_left_ne, "x":7,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_left_ne, "x":8,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_ne, "x":8,  "y":7,  "wrap":False, "expect":1 },
        { "alive_cells": alive_left_ne, "x":15, "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_ne, "x":15, "y":7,  "wrap":False, "expect":0 },

        { "alive_cells": alive_left_ne, "x":0,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_ne, "x":0,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_ne, "x":0,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_ne, "x":0,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_left_ne, "x":7,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_ne, "x":7,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_ne, "x":7,  "y":8,  "wrap":True, "expect":1 },
        { "alive_cells": alive_left_ne, "x":7,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_left_ne, "x":8,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_ne, "x":8,  "y":7,  "wrap":True, "expect":1 },
        { "alive_cells": alive_left_ne, "x":15, "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_ne, "x":15, "y":7,  "wrap":True, "expect":0 },

        { "alive_cells": alive_left_se, "x":0,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_se, "x":0,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_se, "x":0,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_left_se, "x":7,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_se, "x":7,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_se, "x":7,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_se, "x":7,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_left_se, "x":8,  "y":0,  "wrap":False, "expect":1 },
        { "alive_cells": alive_left_se, "x":8,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_se, "x":15, "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_se, "x":15, "y":7,  "wrap":False, "expect":0 },

        { "alive_cells": alive_left_se, "x":0,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_se, "x":0,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_se, "x":0,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_left_se, "x":7,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_se, "x":7,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_se, "x":7,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_se, "x":7,  "y":15, "wrap":True, "expect":1 },
        { "alive_cells": alive_left_se, "x":8,  "y":0,  "wrap":True, "expect":1 },
        { "alive_cells": alive_left_se, "x":8,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_se, "x":15, "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_se, "x":15, "y":7,  "wrap":True, "expect":0 },

        { "alive_cells": alive_left_sw, "x":0,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_sw, "x":0,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_sw, "x":0,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_left_sw, "x":7,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_sw, "x":7,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_sw, "x":7,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_sw, "x":7,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_left_sw, "x":8,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_sw, "x":8,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_sw, "x":15, "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_sw, "x":15, "y":7,  "wrap":False, "expect":0 },

        { "alive_cells": alive_left_sw, "x":0,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_sw, "x":0,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_sw, "x":0,  "y":15, "wrap":True, "expect":1 },
        { "alive_cells": alive_left_sw, "x":7,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_sw, "x":7,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_sw, "x":7,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_sw, "x":7,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_left_sw, "x":8,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_sw, "x":8,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_sw, "x":15, "y":0,  "wrap":True, "expect":1 },
        { "alive_cells": alive_left_sw, "x":15, "y":7,  "wrap":True, "expect":0 },

        { "alive_cells": alive_left_nw, "x":0,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_nw, "x":0,  "y":8,  "wrap":False, "expect":1 },
        { "alive_cells": alive_left_nw, "x":0,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_left_nw, "x":7,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_nw, "x":7,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_nw, "x":7,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_nw, "x":7,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_left_nw, "x":8,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_nw, "x":8,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_nw, "x":15, "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_left_sw, "x":15, "y":7,  "wrap":False, "expect":0 },

        { "alive_cells": alive_left_nw, "x":0,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_nw, "x":0,  "y":8,  "wrap":True, "expect":1 },
        { "alive_cells": alive_left_nw, "x":0,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_left_nw, "x":7,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_nw, "x":7,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_nw, "x":7,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_nw, "x":7,  "y":15, "wrap":True, "expect":0 }, #175
        { "alive_cells": alive_left_nw, "x":8,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_nw, "x":8,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_nw, "x":15, "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_left_nw, "x":15, "y":7,  "wrap":True, "expect":1 },

        { "alive_cells": alive_right_ne, "x":0,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_ne, "x":0,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_ne, "x":0,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_ne, "x":0,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_right_ne, "x":7,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_ne, "x":7,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_ne, "x":7,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_ne, "x":7,  "y":15, "wrap":False, "expect":1 }, #187
        { "alive_cells": alive_right_ne, "x":8,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_ne, "x":8,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_ne, "x":15, "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_ne, "x":15, "y":7,  "wrap":False, "expect":0 },

        { "alive_cells": alive_right_ne, "x":0,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_ne, "x":0,  "y":7,  "wrap":True, "expect":1 },
        { "alive_cells": alive_right_ne, "x":0,  "y":8,  "wrap":True, "expect":1 }, #194
        { "alive_cells": alive_right_ne, "x":0,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_right_ne, "x":7,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_ne, "x":7,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_ne, "x":7,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_ne, "x":7,  "y":15, "wrap":True, "expect":1 }, #199
        { "alive_cells": alive_right_ne, "x":8,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_ne, "x":8,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_ne, "x":15, "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_ne, "x":15, "y":7,  "wrap":True, "expect":0 },

        { "alive_cells": alive_right_se, "x":0,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_se, "x":0,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_se, "x":0,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_se, "x":0,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_right_se, "x":7,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_se, "x":7,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_se, "x":7,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_se, "x":7,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_right_se, "x":8,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_se, "x":8,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_se, "x":15, "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_se, "x":15, "y":7,  "wrap":False, "expect":0 },

        { "alive_cells": alive_right_se, "x":0,  "y":0,  "wrap":True, "expect":1 },
        { "alive_cells": alive_right_se, "x":0,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_se, "x":0,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_se, "x":0,  "y":15, "wrap":True, "expect":1 },
        { "alive_cells": alive_right_se, "x":7,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_se, "x":7,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_se, "x":7,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_se, "x":7,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_right_se, "x":8,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_se, "x":8,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_se, "x":15, "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_se, "x":15, "y":7,  "wrap":True, "expect":0 },

        { "alive_cells": alive_right_sw, "x":0,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_sw, "x":0,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_sw, "x":0,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_sw, "x":0,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_right_sw, "x":7,  "y":0,  "wrap":False, "expect":1 },
        { "alive_cells": alive_right_sw, "x":7,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_sw, "x":7,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_sw, "x":7,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_right_sw, "x":8,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_sw, "x":8,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_sw, "x":15, "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_sw, "x":15, "y":7,  "wrap":False, "expect":0 },

        { "alive_cells": alive_right_sw, "x":0,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_sw, "x":0,  "y":7,  "wrap":True, "expect":1 },
        { "alive_cells": alive_right_sw, "x":0,  "y":8,  "wrap":True, "expect":1 }, #242
        { "alive_cells": alive_right_sw, "x":0,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_right_sw, "x":7,  "y":0,  "wrap":True, "expect":1 },
        { "alive_cells": alive_right_sw, "x":7,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_sw, "x":7,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_sw, "x":7,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_right_sw, "x":8,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_sw, "x":8,  "y":7,  "wrap":True, "expect":0 },

        { "alive_cells": alive_right_nw, "x":0,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_nw, "x":0,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_nw, "x":0,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_nw, "x":0,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_right_nw, "x":7,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_nw, "x":7,  "y":7,  "wrap":False, "expect":1 }, #255
        { "alive_cells": alive_right_nw, "x":7,  "y":8,  "wrap":False, "expect":1 }, #256
        { "alive_cells": alive_right_nw, "x":7,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_right_nw, "x":8,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_nw, "x":8,  "y":7,  "wrap":False, "expect":0 }, #259
        { "alive_cells": alive_right_nw, "x":15, "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_right_nw, "x":15, "y":7,  "wrap":False, "expect":0 },

        { "alive_cells": alive_right_nw, "x":0,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_nw, "x":0,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_nw, "x":0,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_nw, "x":0,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_right_nw, "x":7,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_nw, "x":7,  "y":7,  "wrap":True, "expect":1 },
        { "alive_cells": alive_right_nw, "x":7,  "y":8,  "wrap":True, "expect":1 },
        { "alive_cells": alive_right_nw, "x":7,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_right_nw, "x":8,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_nw, "x":8,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_nw, "x":15, "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_right_nw, "x":15, "y":7,  "wrap":True, "expect":0 },

        { "alive_cells": alive_top_ne, "x":0,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_ne, "x":0,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_ne, "x":0,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_ne, "x":0,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_top_ne, "x":7,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_ne, "x":7,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_ne, "x":7,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_ne, "x":7,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_top_ne, "x":8,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_ne, "x":8,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_ne, "x":15, "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_ne, "x":15, "y":7,  "wrap":False, "expect":1 },

        { "alive_cells": alive_top_ne, "x":0,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_ne, "x":0,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_ne, "x":0,  "y":8,  "wrap":True, "expect":0 }, #288
        { "alive_cells": alive_top_ne, "x":0,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_top_ne, "x":7,  "y":0,  "wrap":True, "expect":1 },
        { "alive_cells": alive_top_ne, "x":7,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_ne, "x":7,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_ne, "x":7,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_top_ne, "x":8,  "y":0,  "wrap":True, "expect":1 }, #294
        { "alive_cells": alive_top_ne, "x":8,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_ne, "x":15, "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_ne, "x":15, "y":7,  "wrap":True, "expect":1 },

        { "alive_cells": alive_top_se, "x":0,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_se, "x":0,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_se, "x":0,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_se, "x":0,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_top_se, "x":7,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_se, "x":7,  "y":7,  "wrap":False, "expect":1 }, #303
        { "alive_cells": alive_top_se, "x":7,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_se, "x":7,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_top_se, "x":8,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_se, "x":8,  "y":7,  "wrap":False, "expect":1 },
        { "alive_cells": alive_top_se, "x":15, "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_se, "x":15, "y":7,  "wrap":False, "expect":0 },

        { "alive_cells": alive_top_se, "x":0,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_se, "x":0,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_se, "x":0,  "y":8,  "wrap":True, "expect":0 }, #312
        { "alive_cells": alive_top_se, "x":0,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_top_se, "x":7,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_se, "x":7,  "y":7,  "wrap":True, "expect":1 },
        { "alive_cells": alive_top_se, "x":7,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_se, "x":7,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_top_se, "x":8,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_se, "x":8,  "y":7,  "wrap":True, "expect":1 },
        { "alive_cells": alive_top_se, "x":15, "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_se, "x":15, "y":7,  "wrap":True, "expect":0 },

        { "alive_cells": alive_top_sw, "x":0,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_sw, "x":0,  "y":7,  "wrap":False, "expect":1 },
        { "alive_cells": alive_top_sw, "x":0,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_sw, "x":0,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_top_sw, "x":7,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_sw, "x":7,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_sw, "x":7,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_sw, "x":7,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_top_sw, "x":8,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_sw, "x":8,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_sw, "x":15, "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_sw, "x":15, "y":7,  "wrap":False, "expect":0 },

        { "alive_cells": alive_top_sw, "x":0,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_sw, "x":0,  "y":7,  "wrap":True, "expect":1 },
        { "alive_cells": alive_top_sw, "x":0,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_sw, "x":0,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_top_sw, "x":7,  "y":0,  "wrap":True, "expect":1 }, #338
        { "alive_cells": alive_top_sw, "x":7,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_sw, "x":7,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_sw, "x":7,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_top_sw, "x":8,  "y":0,  "wrap":True, "expect":1 },
        { "alive_cells": alive_top_sw, "x":8,  "y":7,  "wrap":True, "expect":0 },

        { "alive_cells": alive_top_nw, "x":0,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_nw, "x":0,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_nw, "x":0,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_nw, "x":0,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_top_nw, "x":7,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_nw, "x":7,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_nw, "x":7,  "y":8,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_nw, "x":7,  "y":15, "wrap":False, "expect":0 },
        { "alive_cells": alive_top_nw, "x":8,  "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_nw, "x":8,  "y":7,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_nw, "x":15, "y":0,  "wrap":False, "expect":0 },
        { "alive_cells": alive_top_nw, "x":15, "y":7,  "wrap":False, "expect":0 },

        { "alive_cells": alive_top_nw, "x":0,  "y":0,  "wrap":True, "expect":1 }, #356
        { "alive_cells": alive_top_nw, "x":0,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_nw, "x":0,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_nw, "x":0,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_top_nw, "x":7,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_nw, "x":7,  "y":8,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_nw, "x":7,  "y":15, "wrap":True, "expect":0 },
        { "alive_cells": alive_top_nw, "x":8,  "y":0,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_nw, "x":8,  "y":7,  "wrap":True, "expect":0 },
        { "alive_cells": alive_top_nw, "x":15, "y":0,  "wrap":True, "expect":1 },
        { "alive_cells": alive_top_nw, "x":15, "y":7,  "wrap":True, "expect":0 },

        ]

def test_num_alive_neighbours ():
    global alive_cells
    failures = 0
    #loop through a bunch of tests
    for num, test in enumerate( num_alive_tests):
        alive_cells = test[ "alive_cells"]
        count = num_alive_neighbours (test[ "x"], test[ "y"], test[ "wrap"])
        #report if returned value not what was expected
        if count != test[ "expect"]:
            print ("Test %s failed, got %s, expected %s with x:%s y:%s wrap:%s" %
                    ( num, count, test["expect"],  test["x"], test["y"], test["wrap"] ))
            failures += 1
    if failures == 0:
        print ("Passed all tests")
    else:
        print ("Failed %s tests" % failures)

#### FUNCTIONS ####

# determine the number of alive neighbors
def num_alive_neighbours(x, y, wrap):
    num_neighbours = 0
    tried = [(x,y)] # non-null to prevent wrap back to itself
    for x2 in [x-1, x, x+1]:
        for y2 in [y-1, y, y+1]:

            if (x2, y2) != (x, y):
                neighbour = (x2, y2)
                # Account for 3D nature of panels
                if wrap:
                    if x2 == -1:
                        if y2 < 8:
                            neighbour = (15, y2)
                        else:
                            neighbour = (y2, 0)
                    elif x2 == 8 and y2 >= 8:
                        neighbour = (y2, 7)
                    elif x2 == 16:
                        neighbour = (0, y2)
                    elif y2 == -1:
                        if x2 < 8:
                            neighbour = (x2, 15)
                        else:
                            neighbour = (0, x2)
                    elif y2 == 8 and x2 >= 8:
                            neighbour = (7, x2)
                    elif y2 == 16:
                        neighbour = (x2, 0)
                else:
                    if x2 == 8 and y2 >= 8:
                        neighbour = (y2, 7)
                    elif y2 == 8 and x2 >= 8:
                        neighbour = (7, x2)
                if False: #debug == True
                    print("num: x:%s, y:%s, x2:%s y2:%s neighbour:%s %s tried:%s" %
                            (x, y, x2, y2, neighbour, neighbour in alive_cells, tried) )
                if neighbour not in tried: # don't try same neighbor twice
                    tried.append (neighbour)
                    if neighbour in alive_cells:
                        num_neighbours += 1
    return num_neighbours


# determine if two lists are equivalent
def is_list_equal( list1, list2):
    if len( list1) != len( list2):
        return False
    for item in list1:
        if item not in list2:
            return False
    return True


# convert list of live cell xy pairs to a string
def alive_to_str( alives):
    string = ":" # start character
    checksum = 0
    for y in range (16):
        row = 0
        for x in range (16):
            if x<8 or y<8:
                if (x, y) in alives:
                    row |= 1 << x
        if y<8:
            string += "%04X-" % row
        else:
            string += "%02X-" % row
        checksum += (row & 0xFF) + ((row >>8) & 0xFF) # sum over bytes
    string += ("%02X" % (-checksum & 0xFF))
    return string


# get hex chars from string
hexchars = "01123456789abcdefABCDEF"

def get_hex_chars( string, index):
    scan_index = index
    while string [scan_index] in hexchars:
        scan_index += 1
        if scan_index > len( string):
            return (string, -1) # not found
    if scan_index == index:
        return (string, -1) # not found
    else:
        return( string[index:scan_index], scan_index + 1)


# convert string to an array of alive cells xy pairs
def str_to_alive( string):
    alives = []
    checksum = 0
    # scan to start character
    inx = string.index(':')
    if inx < 0:
        return alives # null at this point
    inx += 1
    if inx < len( string):
        for y in range (16):
            hex_string, inx = get_hex_chars(string, inx)
            if inx > 0:
                row = int( hex_string, 16)
                checksum = checksum + (row & 0xFF) + ((row >> 8) & 0xFF)
                for x in range (16):
                    if row & 1 << x:
                        alives.append( (x, y))
            else:
                print ("***Encoding error in hex string %s" % string)
                return []
        check = string [inx: inx+2]
        if (checksum + int( check, 16)) & 0xFF != 0:
            print ("***checksum error in hex string %s, got %s" % (string, checksum))
            return []
    return alives


# find last occurance of character in string
def rindex( string, search, start=None):
    if start is None:
        start = len( string) - 1
    for i in xrange(start, -1, -1):
        if string[i] == search:
            return i
    return -1


#### CONFIGURATION CONSTANTS ####            string += "%04X-" % row

starting_live_ratio = 0.4
guard_hue = 0.1 # portion of full circle
color_option = 1 # 0 dead is black, 1 dead is complimentary
allowed_loops = 3
maximum_generations = 500
base_saturation = 1
base_luminance = 0.5
wrap = True
record_seed = True
record_end = True
record_file = "recordings" # name of file to save to, null to not save
playback_file = "playback" # name of file containing playback strings

#### CONSTANTS ####
num_transitions = 5 # between state
num_phases = 2 * num_transitions
dead = 0
alive = num_transitions
dying = alive + 1
spark = dead + 1

#### MAIN LOOP ####
# VARIABLES
test_num_alive_neighbours () # run unit tests first
base_hue = 0
num_generations = 0
num_cells_start = 0
num_cells_left = 0
period = 0
past_period = 0
loop_count = 0

# optionally open playback file
if playback_file != "" and os.path.exists( playback_file):
    in_file = open( playback_file, "r")
    is_reading = True
else:
    is_reading = False

while True:
    # loop initialization
    if period > 0: # actually a holdover from the last pass
        if num_cells_left == 0:
            cause = "annihilation"
        elif period == 1:
            cause = "stability"
        else:
            cause = "oscillating period %s" % period
        if record_file != "":
            with open( record_file, 'a') as recording:
                recording.write("end: %s\n" % alive_to_str( alive_cells))
                recording.write("generations:%s, start:%s end:%s, cause: %s\n" %
                    ( num_generations, num_cells_start, num_cells_left, cause) )
        if record_end:
            print ("end: %s" % alive_to_str( alive_cells))
        print ("hue: %4.2f generations: %3s, start/end: %3s/%2s, cause: %s" %
                ( base_hue, num_generations, num_cells_start, num_cells_left, cause) )
    base_hue = (base_hue + guard_hue + ( 1 - 2 * guard_hue) * random.random() ) % 1
    if color_option == 1: # dead is complimentary
        phaseColors = [ hsv_colour( (base_hue+0.5)%1, base_saturation, 0.5 * base_luminance), # dead
                        hsv_colour( (base_hue+0.6)%1, base_saturation, 0.6 * base_luminance), # spark
                        hsv_colour( (base_hue+0.7)%1, base_saturation, 0.7 * base_luminance),
                        hsv_colour( (base_hue+0.8)%1, base_saturation, 0.8 * base_luminance),
                        hsv_colour( (base_hue+0.9)%1, base_saturation, 0.9 * base_luminance),

                        hsv_colour( (base_hue+0.0)%1, base_saturation, 1   * base_luminance), # alive
                        hsv_colour( (base_hue+0.1)%1, base_saturation, 0.9 * base_luminance), # dying
                        hsv_colour( (base_hue+0.2)%1, base_saturation, 0.8 * base_luminance),
                        hsv_colour( (base_hue+0.3)%1, base_saturation, 0.7 * base_luminance),
                        hsv_colour( (base_hue+0.4)%1, base_saturation, 0.6 * base_luminance)
                    ]
    else:
        phaseColors = [ hsv_colour( base_hue, base_saturation, 0   * base_luminance), # dead
                        hsv_colour( base_hue, base_saturation, 0.2 * base_luminance), # spark
                        hsv_colour( base_hue, base_saturation, 0.4 * base_luminance),
                        hsv_colour( base_hue, base_saturation, 0.6 * base_luminance),
                        hsv_colour( base_hue, base_saturation, 0.8 * base_luminance),

                        hsv_colour( base_hue, base_saturation, 1   * base_luminance), # alive
                        hsv_colour( base_hue, base_saturation, 0.8 * base_luminance), # dying
                        hsv_colour( base_hue, base_saturation, 0.6 * base_luminance),
                        hsv_colour( base_hue, base_saturation, 0.4 * base_luminance),
                        hsv_colour( base_hue, base_saturation, 0.2 * base_luminance)
                    ]


    # seed the starting cells and build current_phases list of lists
    alive_cells = []
    current_phases = []
    if is_reading:
        is_getting_line = True
        is_reading = False # assume failure unless get a good line
        while is_getting_line:
            string = in_file.readline()
            if string == "": # End Of File
                is_getting_line = False
            else:
                if string[:7] == "seed: :":
                    alive_cells = str_to_alive( string[6:])
                    if len( alive_cells) > 0:
                        for x in range( 16):
                            column = []
                            for y in range( 16):
                                if (x < 8 or y < 8) and (x,y) in alive_cells:
                                    column.append( spark)
                                else:
                                    column.append( dead)
                            current_phases.append( column)
                        is_getting_line = False # got the line, move on
                        is_reading = True # still reading the file
    if not is_reading: # normal method and fallback
        for x in range( 16):
            column = []
            for y in range( 16):
                if (x < 8 or y < 8) and random.random() < starting_live_ratio:
                    alive_cells.append( (x,y))
                    column.append( spark)
                else:
                    column.append( dead)
            current_phases.append( column)
    num_cells_start = len( alive_cells)
    if record_file != "":
        with open( record_file, 'a') as recording:
            recording.write("seed: %s\n" % alive_to_str( alive_cells))
    if record_seed:
        print ("seed: %s" % alive_to_str( alive_cells))
    if True: # debug is true
        dummy =  alive_to_str( alive_cells)
        dummy = str_to_alive( dummy)
        if not is_list_equal( alive_cells, dummy):
            print( "*** alive_to_str/str_to_alive conversion is not equal")
            print( alive_to_str( dummy))

    num_generations = 0
    past_alives = []
    is_looping = False
    loop_count = 0
    past_period = 0
    fail_safe_count = maximum_generations
    while not is_looping:

        # transition from current phase to final phase of current state
        leds = {}
        for t in range ( num_transitions):
            for x in range( 16):
                for y in range( 16):
                    if x < 8 or y < 8:
                        phase = 0
                        phase = current_phases[ x][ y]
                        leds[ x,y] = phaseColors [ phase]
                        if phase != dead and phase != alive:
                            current_phases[ x][ y] = (phase + 1) % num_phases
            display.set_leds( leds)
            time.sleep( 0.2)

        # determine if pattern is looping (too much)
        for count, past_alive_cells in enumerate( past_alives):
            if is_list_equal( alive_cells, past_alive_cells): # seen this before?
                period = len( past_alives) - count
                if past_period == 0:
                    past_period = period
                    loop_count = 1
                elif period == past_period:
                    loop_count += 1
                    if loop_count >= allowed_loops:
                        is_looping = True # now we've seen enough
        if len( past_alives) == 0 or past_period == 0: # first pass or no loop detected
            past_alives.append( alive_cells)
            num_generations += 1

        # determine the state and phase for the next generation
        next_cells = []
        for x in range( 16):
            for y in range( 16):
                if x < 8 or y < 8:
                    is_alive = (x, y) in alive_cells
                    neighbours = num_alive_neighbours(x, y, wrap)

                    if is_alive:
                        if ( neighbours == 2 or neighbours == 3):
                            next_cells.append( ( x, y))
                            phase = alive
                        else:
                            phase = dying
                    elif neighbours == 3:
                        phase = spark
                        next_cells.append( ( x,y))
                    else: # dead
                        phase = dead
                    current_phases[ x][y] = phase

        num_cells_left = len( alive_cells)
        alive_cells = next_cells

        # stop VERY long non-repeating patterns
        fail_safe_count -= 1
        if fail_safe_count <= 0:
            print ("Fail safe triggered")
            is_looping = True
