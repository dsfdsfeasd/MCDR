from random import random
from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'TNT',
    'version': '1.0.0',
    'name': 'Mifeng',
    'description': '骗赞服同款!!TNT',
    'author': 'Bing',
    'link': '',
}

tnt_waiting_players = {}  # 存储等待输入玩家名字的玩家

@new_thread(PLUGIN_METADATA['name'])
def on_info(server, info):
    if info.content.startswith('!!player'):
        # 检查玩家权限等级
        if not server.get_permission_level(info.player) >= 3:
            server.tell(info.player, '权限不足！需要权限等级3以上才能使用该指令。')
            return

        # 解析指令参数
        args = info.content.split(' ')
        if len(args) != 3:
            server.say('用法: !!player <target_player> <new_player>')
            return
        
        # 获取目标玩家
        target_player = args[1]
        
        # 获取替换的玩家
        new_player = args[2]

        # 调用函数进行玩家替换操作
        replace_player(server, target_player, new_player)
    elif info.content == '!!TNT':
        if random() < 0.6:
            server.execute(f'kill <player>')
            server.execute(f'execute at {info.player} run summon minecraft:firework_rocket ~ ~ ~')
        else:
            server.execute(f'kill {info.player}')
            x, y, z = server.get_player_coordinate(info.player)
            server.say(f'{info.player} died at ({x}, {y}, {z})')
            tnt_waiting_players[info.player] = True  # 添加到等待输入玩家名字的列表
    elif info.content == 'say surprise':
        server.say('surprise')

def replace_player(server, target_player, new_player):
    # TODO: 在这里添加你自己的代码来实现具体的玩家替换操作
    # 下面的代码只是一个示例，实际操作需要替换为真正的玩家替换逻辑

    # 使用MCDR提供的replace_player()函数进行玩家替换
    success = server.replace_player(target_player, new_player)
    
    # 反馈结果
    if success:
        server.say(f'成功将玩家 {target_player} 替换为 {new_player}.')
    else:
        server.say(f'玩家替换失败.')

def on_player_chat(server, player, message):
    if player in tnt_waiting_players:
        del tnt_waiting_players[player]  # 从等待输入玩家名字的列表中删除该玩家
        server.say(f'{player} 被击杀了，被输入的玩家名字为：{message}')

def on_load(server, old_module):
    server.register_help_message('!!player', '替换玩家')
    server.register_help_message('!!TNT', PLUGIN_METADATA['description'])
    server.register_info_command('!!player', on_info, perm=3)
    server.register_info_command('!!TNT', on_info)
    server.register_event('player_chat', on_player_chat)
