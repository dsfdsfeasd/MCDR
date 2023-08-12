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
            player_info = server.get_player_info(info.player)
            x, y, z = player_info.location.x, player_info.location.y, player_info.location.z
            server.say(f'{info.player} died at ({x}, {y}, {z})')
            tnt_waiting_players[info.player] = True  # 添加到等待输入玩家名字的列表
    elif info.content == 'say surprise':
        server.say('surprise')


def replace_player(server, target_player, new_player):
    # 获取目标玩家的数据
    target_data = server.execute(f"data get entity {target_player}")

    # 将目标玩家的数据合并到新玩家身上
    server.execute(f"data merge entity {new_player} {target_data}")

    # 将新玩家传送到目标玩家所在位置
    server.execute(f"execute as {target_player} at @s run tp {new_player} ~ ~ ~")

    # 反馈结果
    server.say(f'成功将玩家 {target_player} 替换为 {new_player}.')


def on_player_chat(server, player, message):
    if player in tnt_waiting_players:
        del tnt_waiting_players[player]  # 从等待输入玩家名字的列表中删除该玩家
        server.say(f'{player} 被击杀了，被输入的玩家名字为：{message}')


def on_load(server, old_module):
    server.register_help_message('!!player', '替换玩家')
    server.register_help_message('!!TNT', PLUGIN_METADATA['description'])
    server.register_command(
        CommandInfo('!!player', '替换玩家', usage='!!player <target_player> <new_player>', perm=3, handler=on_info))
    server.register_command(CommandInfo('!!TNT', PLUGIN_METADATA['description'], handler=on_info))
    server.register_event('player_chat', on_player_chat)
