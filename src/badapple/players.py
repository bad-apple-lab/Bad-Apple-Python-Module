import os
import time
import shlex
import subprocess
from typing import Callable


def which(program: str) -> str:
    if os.name == "nt" and not program.lower().endswith(".exe"):
        program += ".EXE"

    envdir_list = [os.curdir] + os.environ["PATH"].split(os.pathsep)

    for envdir in envdir_list:
        program_path = os.path.join(envdir, program)
        if os.path.isfile(program_path) and os.access(program_path, os.X_OK):
            return program_path


__FFPLAY = 'ffplay'  # all
__AVPLAY = 'avplay'  # all
__MPV = 'mpv'
__VLC = 'vlc'
__MPG123 = 'mpg123' # mp3
__CMUS = 'cmus'
__SIMPLEAUDIO = 'simpleaudio'  # wav
__PYAUDIO = 'pyaudio'  # wav
__PLAYSOUND = 'playsound'  # mp3+wav not_win
__PYDUB = 'pydub'  # simpleaudio-pyaudio-avplay-ffplay

__AUTO = 'auto'

__PLAYERS = [
    __FFPLAY,
    __AVPLAY,
    __MPV,
    __VLC,
    __MPG123,
    __CMUS,
    __SIMPLEAUDIO,
    __PYAUDIO,
    __PLAYSOUND,
    __PYDUB,
]

__PLAYERS_AND_AUTO = [__AUTO, ] + __PLAYERS.copy()

ALIAS = {
    __AUTO: [None, '', 'default'],
    __FFPLAY: ['ffmpeg',],
    __AVPLAY: list(),
    __MPV: list(),
    __VLC: ['cvlc',],
    __MPG123: list(),
    __CMUS: list(),
    __SIMPLEAUDIO: list(),
    __PYAUDIO: list(),
    __PLAYSOUND: list(),
    __PYDUB: list(),
}

player_realias = {j: i for i in ALIAS for j in ALIAS[i]}
player_check = dict()
player_play = dict()


def reg_check(player: str) -> Callable[[Callable[[], bool]], Callable[[], bool]]:
    def __get_f(f: Callable[[], bool]) -> Callable[[], bool]:
        if player not in __PLAYERS_AND_AUTO:
            raise ValueError(player)
        if player in player_check:
            raise ValueError(player)
        player_check[player] = f
        return f
    return __get_f


def reg_play(player: str) -> Callable[[Callable[[], bool]], Callable[[], bool]]:
    def __get_f(f: Callable[[str], None]) -> Callable[[str], None]:
        if player not in __PLAYERS_AND_AUTO:
            raise ValueError(player)
        if player in player_play:
            raise ValueError(player)
        player_play[player] = f
        return f
    return __get_f


@reg_check(__FFPLAY)
def check_ffplay() -> bool:
    if which('ffplay'):
        return True
    else:
        return False


@reg_play(__FFPLAY)
def play_ffplay(audio: str) -> None:
    subprocess.call(
        shlex.split('ffplay -nodisp -autoexit -hide_banner "%s"' % audio),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


@reg_check(__AVPLAY)
def check_avplay() -> bool:
    if which('avplay'):
        return True
    else:
        return False


@reg_play(__AVPLAY)
def play_avplay(audio: str) -> None:
    subprocess.call(
        shlex.split('avplay -nodisp -autoexit -hide_banner "%s"' % audio),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


@reg_check(__MPV)
def check_mpv() -> bool:
    if which('mpv'):
        return True
    else:
        return False


@reg_play(__MPV)
def play_mpv(audio: str) -> None:
    subprocess.call(
        shlex.split('mpv --no-video "%s"' % audio),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


@reg_check(__VLC)
def check_vlc() -> bool:
    if which('cvlc'):
        return True
    else:
        return False


@reg_play(__VLC)
def play_vlc(audio: str) -> None:
    subprocess.call(
        shlex.split('cvlc "%s"' % audio),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


@reg_check(__MPG123)
def check_mpg123() -> bool:
    if which('mpg123'):
        return True
    else:
        return False


@reg_play(__MPG123)
def play_mpg123(audio: str) -> None:
    subprocess.call(
        shlex.split('mpg123 "%s"' % audio),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


@reg_check(__CMUS)
def check_cmus() -> bool:
    if which('cmus'):
        return True
    else:
        return False


@reg_play(__CMUS)
def play_cmus(audio: str) -> None:
    subprocess.call(
        shlex.split('cmus-remote -f "%s"' % audio),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


@reg_check(__SIMPLEAUDIO)
def check_simpleaudio() -> bool:
    try:
        import simpleaudio
    except ImportError:
        return False
    return True


@reg_play(__SIMPLEAUDIO)
def play_simpleaudio(audio: str) -> None:
    import simpleaudio
    wave_obj = simpleaudio.WaveObject.from_wave_file(audio)
    play_obj = wave_obj.play()
    try:
        play_obj.wait_done()
    except KeyboardInterrupt:
        pass
    finally:
        play_obj.stop()


@reg_check(__PYAUDIO)
def check_pyaudio() -> bool:
    try:
        import pyaudio
    except ImportError:
        return False
    return True


@reg_play(__PYAUDIO)
def play_pyaudio(audio: str) -> None:
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


@reg_check(__PLAYSOUND)
def check_playsound() -> bool:
    try:
        import playsound
    except ImportError:
        return False
    return True


@reg_play(__PLAYSOUND)
def play_playsound(audio: str) -> None:
    from playsound import playsound
    playsound(audio)


@reg_check(__PYDUB)
def check_playsound() -> bool:
    try:
        import pydub
    except ImportError:
        return False
    return True


@reg_play(__PYDUB)
def play_playsound(audio: str) -> None:
    from pydub import AudioSegment, playback
    playback.play(AudioSegment.from_file(audio))


@reg_check(__AUTO)
def check_auto() -> bool:
    return True

@reg_play(__AUTO)
def play_auto(audio: str) -> None:
    for i in __PLAYERS:
        a = time.time()
        try:
            player_play[i](audio)
            return
        except KeyboardInterrupt:
            return
        except Exception as e:
            if time.time()-a > 1.:
                raise e


def realias(player: str) -> str:
    return player_realias.get(player, player)


def is_player(player: str) -> bool:
    return realias(player) in __PLAYERS_AND_AUTO


def is_available(player: str) -> bool:
    return player_check.get(realias(player), lambda:False)()

def get_players() -> list:
    return __PLAYERS_AND_AUTO.copy()

def get_availables() -> list:
    return [i for i in __PLAYERS_AND_AUTO if is_available(i)]


def playa(audio: str, player: str) -> None:
    player_play[realias(player)](audio)


if __name__ == '__main__':
    for i in __PLAYERS_AND_AUTO:
        assert i in ALIAS
        assert i in player_check
        assert i in player_play
    assert len(__PLAYERS_AND_AUTO) == len(ALIAS)
    assert len(__PLAYERS_AND_AUTO) == len(player_check)
    assert len(__PLAYERS_AND_AUTO) == len(player_play)

