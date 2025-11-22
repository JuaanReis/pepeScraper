""" 
    A function that disables colors according to the "color" flag in config.py.

    **Author:** JuaanReis       
    **Date:** 21-11-2025        
    **Last modification:** -      
    **E-mail:** teixeiradosreisjuan@gmail.com       
    **Version:** 1.1.6            

    **Example:**        
    ```python
        from colorama import Fore
        from src.utils.color import colorize
    
        print(colorize("OK!", Fore.RED))
    ```
"""

from colorama import Style
from config import color, color_ansi

def colorize(text: str, color_code: str) -> str:
    if not color:  
        return text
    elif color_ansi != "":
        return f"{color_ansi}{text}\033[0m"
    return f"{color_code}{text}{Style.RESET_ALL}"
