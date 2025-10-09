"""
    function that returns data from config.json, use for global settings in functions.

    Author: JuaanReis
    Date: 28-08-2025
    Last modification: -
    E-mail: teixeiradosreisjuan@gmail.com   
    Version: 1.1.3b2

    Example:
        from utils.load_config import load_config_json

        DATA = load_config_json()
"""

from pathlib import Path
import json

def load_config_json():
    try:
        ROOT_DIR = Path(__file__).resolve().parent.parent  
        config_path = ROOT_DIR / 'config.json'
        with config_path.open('r', encoding='utf-8') as f:
            DATA = json.load(f)
            return DATA
    except FileNotFoundError as e:
       return None