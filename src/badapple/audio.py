import os

from .util import get_info
from anyplayer import get_names, get_availables, get_available_player, Player


def help_audio() -> None:
    players = get_names()
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


def get_player(
    audio: str,
    player: str,
    video: str = None,
) -> Player:
    if not audio:
        if not player:
            return None
        if video is None:
            raise FileNotFoundError(audio)
        audio = video

    audio = os.path.abspath(audio)
    open(audio, 'rb').close()

    return get_available_player(player, audio, err=True)
