import os

from .util import get_info

with_anyplayer = True

try:
    import anyplayer
except ImportError:
    with_anyplayer = False


def help_audio() -> None:
    if not with_anyplayer:
        print('Please `pip install anyplayer` to play audio', flush=True)
        return

    from anyplayer import get_names, get_availables
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


def get_player(audio: str, player: str, video: str = None):
    if not audio:
        if not player:
            return None
        if video is None:
            raise FileNotFoundError(audio)
        audio = video

    audio = os.path.abspath(audio)
    open(audio, 'rb').close()

    from anyplayer import get_available_player
    return get_available_player(player, audio, err=True)
