import os
import json

def load_json_file(file_name):
    file_path = os.path.join('assets/cfg/', file_name)
    with open(file_path, 'r') as f:
        return json.load(f)

def load_window():
    return load_json_file('window.json')

def load_level_01():
    return load_json_file('level_01.json')

def load_level_02():
    return load_json_file('level_02.json')

def load_enemies():
    return load_json_file('enemies.json')

def load_player():
    return load_json_file('player.json')

def load_bullet():
    return load_json_file('bullet.json')

def load_explosion():
    return load_json_file('explosion.json')

def load_interface():
    return load_json_file('interface.json')

def load_starfield():
    return load_json_file('starfield.json')
