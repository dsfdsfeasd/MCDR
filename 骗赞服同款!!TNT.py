from random import random
from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'mifeng',
    'version': '1.0.0',
    'name': 'Mifeng',
    'description': 'A simple plugin for MCDReforge',
    'author': 'Bing',
    'link': '',
}

@new_thread(PLUGIN_METADATA['name'])
def on_info(server, info):
    if info.content == '!!TNT':
        if random() < 0.6:
            server.execute(f'kill <player>')
            server.execute(f'execute at {info.player} run summon minecraft:firework_rocket ~ ~ ~')
        else:
            server.execute(f'kill {info.player}')
            x, y, z = server.get_player_coordinate(info.player)
            server.say(f'{info.player} died at ({x}, {y}, {z})')

def on_load(server, old_module):
    server.register_help_message('!!TNT', PLUGIN_METADATA['description'])
    server.register_info_command('!!TNT', on_info)