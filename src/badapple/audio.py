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


def get_player(audio_pth: str, player: str, video_pth: str = None):
    if not audio_pth:
        if not player:
            return None
        if video_pth is None:
            raise FileNotFoundError(audio_pth)
        audio_pth = video_pth

    audio_pth = os.path.abspath(audio_pth)
    open(audio_pth, 'rb').close()

    from anyplayer import get_available_player
    return get_available_player(player, audio_pth, err=True)
