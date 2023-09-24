import os
import time
import shlex
import subprocess
import multiprocessing
from typing import Tuple, Callable
from .util import which

__FFPLAY = 'ffplay'  # all
__AVPLAY = 'avplay'  # all
# __PYDUB = 'pydub'  # simpleaudio-pyaudio-avplay-ffplay
__SIMPLEAUDIO = 'simpleaudio'  # wav
__PYAUDIO = 'pyaudio'  # wav
__PLAYSOUND = 'playsound'  # mp3+wav not_win
__AUTO = 'auto'  # for i in PLAYERS

PLAYERS = [
    __FFPLAY,
    __AVPLAY,
    # __PYDUB,
    __SIMPLEAUDIO,
    __PYAUDIO,
    __PLAYSOUND,
]


def help_audio() -> None:
    get_availables()
    pass


def available(player: str) -> str:
    if player == __AUTO:
        return player

    if player not in PLAYERS:
        return ''

    if player == __FFPLAY:
        if which('ffplay'):
            return player
        else:
            return ''

    if player == __AVPLAY:
        if which('avplay'):
            return player
        else:
            return ''

    if player == __SIMPLEAUDIO:
        try:
            import simpleaudio
        except ImportError:
            return ''
        return player

    if player == __PYAUDIO:
        try:
            import pyaudio
        except ImportError:
            return ''
        return player

    if player == __PLAYSOUND:
        try:
            import playsound
        except ImportError:
            return ''
        return player


def get_availables() -> list:
    return [i for i in PLAYERS if available(i)]


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

    if player == __AUTO or not player:
        return audio, __AUTO

    if player not in PLAYERS:
        raise ValueError('Player %s is not in players' % player)
    if check_player:
        if not available(player):
            raise ValueError('Player %s is not available' % player)

    return audio, player


def f_ffplay(audio: str) -> None:
    subprocess.call(
        shlex.split('ffplay -nodisp -autoexit -hide_banner "%s"' % audio),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def f_avplay(audio: str) -> None:
    subprocess.call(
        shlex.split('avplay -nodisp -autoexit -hide_banner "%s"' % audio),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def f_simpleaudio(audio: str) -> None:
    import simpleaudio
    wave_obj = simpleaudio.WaveObject.from_wave_file(audio)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    play_obj.stop()


def f_pyaudio(audio: str) -> None:
    import wave
    import pyaudio
    CHUNK = 1024
    with wave.open(audio, 'rb') as wf:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )
        data = wf.readframes(CHUNK)
        while len(data):
            stream.write(data)
            data = wf.readframes(CHUNK)
        stream.close()
        p.terminate()


def f_playsound(audio: str) -> None:
    from playsound import playsound
    playsound(audio)


def f_auto(audio: str) -> None:
    for i in PLAYERS:
        a = time.time()
        try:
            f_playa(audio, i)
            return
        except KeyboardInterrupt:
            return
        except Exception:
            if time.time()-a > 1.:
                raise RuntimeError(i)


def f_playa(audio: str, player: str) -> None:
    if player == __AUTO:
        return f_auto(audio)
    if player == __SIMPLEAUDIO:
        return f_simpleaudio(audio)
    if player == __PYAUDIO:
        return f_pyaudio(audio)
    if player == __FFPLAY:
        return f_ffplay(audio)
    if player == __AVPLAY:
        return f_avplay(audio)
    if player == __PLAYSOUND:
        return f_playsound(audio)
    raise ValueError(player)


def p_playa(audio: str, player: str) -> None:
    p = multiprocessing.Process(target=f_playa, args=(audio, player))
    p.start()
    return p
