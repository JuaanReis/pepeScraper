from datetime import datetime
import random

CHRISTMAS_COLORS = [
    "\033[31m",  
    "\033[32m",  
    "\033[34m",  
    "\033[92m",  
    "\033[36m",  
]

_color_index = 0

def is_christmas():
    today = datetime.now()
    return today.month == 12 and today.day == 25

random.shuffle(CHRISTMAS_COLORS) 

def next_christmas_color():
    global _color_index
    if _color_index == len(CHRISTMAS_COLORS):
        random.shuffle(CHRISTMAS_COLORS) 
        _color_index = 0 
    color = CHRISTMAS_COLORS[_color_index]
    _color_index += 1
    return color
