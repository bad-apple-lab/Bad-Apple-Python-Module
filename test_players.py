import time
from src.badapple.players import get_player
from src.badapple.builtin_files import BA_BA, BA_MP4,BA_MP3, BA_WAV, ba_get


def test(p: str, a: str) -> None:
    a = ba_get(a)
    print(p, a)
    player = get_player(p, a)
    print('is_available', player.is_available())
    if not player.is_available():
        return
    player.start()
    print('started')
    print('is_alive', player.is_alive())
    try:
        for i in range(6):
            time.sleep(0.5)
            print(i+1, 'is_alive', player.is_alive())
    except KeyboardInterrupt:
        pass
    finally:
        print('before is_alive', player.is_alive())
        player.terminate()
        print('after is_alive', player.is_alive())
    print('end')


__FFPLAY = 'ffplay'  # all
__AVPLAY = 'avplay'  # all
__MPV = 'mpv'
__VLC = 'vlc'
__MPG123 = 'mpg123'  # mp3
__CMUS = 'cmus'
__SIMPLEAUDIO = 'simpleaudio'  # wav
__PYAUDIO = 'pyaudio'  # wav
__PLAYSOUND = 'playsound'  # mp3+wav not_win
__PYDUB = 'pydub'  # simpleaudio-pyaudio-avplay-ffplay

__AUTO = 'auto'

test(__AUTO, BA_WAV)
