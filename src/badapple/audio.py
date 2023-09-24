import os
from multiprocessing import Process
from typing import Tuple

from .players import realias, is_player, is_available, get_availables, playa

def help_audio() -> None:
    get_availables()
    pass


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
