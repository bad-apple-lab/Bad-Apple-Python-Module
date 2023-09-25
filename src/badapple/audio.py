import os
from multiprocessing import Process
from typing import Tuple

from .util import get_info
from .players import realias, playa
from .players import is_player, is_available, get_players, get_availables


def help_audio() -> None:
    players = get_players()
    availables = get_availables()
    s = 'usage: badapple --audio_player AUDIO_PLAYER [options] ... \n\n'
    s += get_info() + '\n\navailable AUDIO_PLAYER:\n'
    for i in players:
        s += '  ' + i
        s += ' '*(14-len(i))
        if i not in availables:
            s += 'un'
        s += 'available\n'
    print(s, end='', flush=True)


def preplaya(
    audio: str,
    player: str,
    video: str = None,
    check_player: bool = True
) -> Tuple[str, str]:
    if not audio:
        if not player:
            return '', ''
        if video is None:
            raise FileNotFoundError(audio)
        audio = video

    audio = os.path.abspath(audio)
    open(audio, 'rb').close()

    if not is_player(player):
        raise ValueError('%s is not a player' % player)
    player = realias(player)
    if check_player:
        if not is_available(player):
            raise ValueError('Player %s is not available' % player)

    return audio, player


def p_playa(audio: str, player: str) -> Process:
    p = Process(target=playa, args=(audio, player))
    p.start()
    return p
