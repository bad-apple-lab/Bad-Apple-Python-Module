import os
import time
import shlex
import subprocess
import multiprocessing
from abc import ABCMeta, abstractmethod


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
__MPG123 = 'mpg123'  # mp3
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
player_class = dict()


def realias(player: str) -> str:
    return player_realias.get(player, player)


def is_player(player: str) -> bool:
    return realias(player) in __PLAYERS_AND_AUTO


def get_names() -> list:
    return __PLAYERS_AND_AUTO.copy()


class Player(metaclass=ABCMeta):
    def __init__(self, audio: str, clk: float = 0.1) -> None:
        self.audio = audio
        self.clk = clk

    @abstractmethod
    def is_available(self) -> bool:
        return False

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def run(self) -> int:
        self.start()
        self.wait()

    @abstractmethod
    def is_alive(self) -> bool:
        return self.process.is_alive()

    @abstractmethod
    def terminate(self) -> int:
        if not self.is_alive():
            return 0
        self.process.terminate()
        time.sleep(self.clk)
        if not self.is_alive():
            return 0
        self.process.kill()
        return 1

    def kill(self) -> int:
        return self.terminate()

    def wait(self, s: float = -1.) -> int:
        try:
            if s < 0:
                while self.is_alive():
                    time.sleep(self.clk)
            else:
                t = time.time()
                while time.time()-t < s and self.is_alive():
                    time.sleep(self.clk)
        except KeyboardInterrupt:
            pass
        finally:
            return self.terminate()


def get_player(player: str, audio: str, clk: float = 0.1) -> Player:
    assert is_player(player)
    player = realias(player)
    return player_class[player](audio, clk)


def get_available_player(
    player: str,
    audio: str,
    clk: float = 0.1,
    err: bool = False,
) -> None | Player:
    if not is_player(player):
        if err:
            raise ValueError('%s is not a player' % player)
        else:
            return None
    ans = get_player(player, audio)
    if not ans.is_available():
        if err:
            raise ValueError('Player %s is not available' % player)
        else:
            return None
    return ans


def get_availables() -> list:
    return [i for i in __PLAYERS_AND_AUTO if get_player(i, '').is_available()]


class ClPlayer(Player):
    def __init__(
        self,
        executable: str,
        args: str | list,
        audio: str,
        clk: float = 0.1
    ) -> None:
        self.executable = executable
        if isinstance(args, list):
            args = ' '.join(args)
        if args:
            args += ' '
        self.head = executable + ' ' + args + '"%s"'
        super().__init__(audio, clk)

    def is_available(self) -> None:
        if which(self.executable):
            return True
        else:
            return False

    def start(self) -> None:
        self.process = subprocess.Popen(
            shlex.split(self.head % self.audio),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def run(self) -> int:
        return super().run()

    def is_alive(self) -> bool:
        return self.process.poll() is None

    def terminate(self) -> int:
        return super().terminate()


class FFplayPlayer(ClPlayer):
    def __init__(self, audio: str, clk: float = 0.1) -> None:
        super().__init__(
            'ffplay',
            ['-nodisp', '-autoexit', '-hide_banner',],
            audio,
            clk
        )


player_class[__FFPLAY] = FFplayPlayer


class AVplayPlayer(ClPlayer):
    def __init__(self, audio: str, clk: float = 0.1) -> None:
        super().__init__(
            'avplay',
            ['-nodisp', '-autoexit', '-hide_banner',],
            audio,
            clk
        )


player_class[__AVPLAY] = AVplayPlayer


class MpvPlayer(ClPlayer):
    def __init__(self, audio: str, clk: float = 0.1) -> None:
        super().__init__('mpv', '--no-video', audio, clk)


player_class[__MPV] = MpvPlayer


class VlcPlayer(ClPlayer):
    def __init__(self, audio: str, clk: float = 0.1) -> None:
        super().__init__('cvlc', '', audio, clk)


player_class[__VLC] = VlcPlayer


class Mpg123Player(ClPlayer):
    def __init__(self, audio: str, clk: float = 0.1) -> None:
        super().__init__('mpg123', '', audio, clk)


player_class[__MPG123] = Mpg123Player


class CmusPlayer(ClPlayer):
    def __init__(self, audio: str, clk: float = 0.1) -> None:
        super().__init__('cmus-remote', '-f', audio, clk)


player_class[__CMUS] = CmusPlayer


class SimpleaudioPlayer(Player):
    def __init__(self, audio: str, clk: float = 0.1) -> None:
        super().__init__(audio, clk)

    def is_available(self) -> bool:
        try:
            import simpleaudio
        except ImportError:
            return False
        return True

    def start(self) -> None:
        import simpleaudio as sa
        self.process = sa.WaveObject.from_wave_file(self.audio).play()

    def run(self) -> int:
        return super().run()

    def is_alive(self) -> bool:
        return self.process.is_playing()

    def terminate(self) -> int:
        if self.is_alive():
            self.process.stop()
        return 0


player_class[__SIMPLEAUDIO] = SimpleaudioPlayer


class ProcessPlayer(Player):
    def __init__(self, audio: str, clk: float = 0.1) -> None:
        super().__init__(audio, clk)

    def start(self) -> None:
        self.process = multiprocessing.Process(target=self.run)
        self.process.start()

    def is_alive(self) -> bool:
        return super().is_alive()

    def terminate(self) -> int:
        return super().terminate()


class PyAudioPlayer(ProcessPlayer):
    def __init__(self, audio: str, clk: float = 0.1) -> None:
        super().__init__(audio, clk)

    def is_available(self) -> bool:
        try:
            import wave
            import pyaudio
        except ImportError:
            return False
        return True

    def run(self) -> int:
        import wave
        import pyaudio
        CHUNK = 1024
        with wave.open(self.audio, 'rb') as wf:
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


player_class[__PYAUDIO] = PyAudioPlayer


class PlaysoundPlayer(ProcessPlayer):
    def __init__(self, audio: str, clk: float = 0.1) -> None:
        super().__init__(audio, clk)

    def is_available(self) -> bool:
        try:
            import playsound
        except ImportError:
            return False
        return True

    def run(self) -> int:
        import playsound
        playsound.playsound(self.audio)


player_class[__PLAYSOUND] = PlaysoundPlayer


class PydubPlayer(ProcessPlayer):
    def __init__(self, audio: str, clk: float = 0.1) -> None:
        super().__init__(audio, clk)

    def is_available(self) -> bool:
        try:
            import pydub
        except ImportError:
            return False
        return True

    def run(self) -> int:
        from pydub import AudioSegment, playback
        playback.play(AudioSegment.from_file(self.audio))


player_class[__PYDUB] = PydubPlayer


class AutoPlayer(Player):
    def __init__(
        self,
        audio: str,
        max_wait: float = 0.5,
        clk: float = 0.1
    ) -> None:
        self.max_wait = max_wait
        super().__init__(audio, clk)

    def is_available(self) -> bool:
        return True

    def start(self) -> None:
        for i in player_class:
            self.process = get_player(i, self.audio, self.clk)
            try:
                if not self.process.is_available():
                    continue
                try:
                    self.process.start()
                except KeyboardInterrupt as e:
                    raise e
                except Exception as e:
                    self.process.terminate()
                t = time.time()
                while self.process.is_alive():
                    if time.time()-t > self.max_wait:
                        return
                    time.sleep(self.clk)
            except KeyboardInterrupt:
                self.process.terminate()
                return
            except Exception as e:
                self.process.terminate()
                raise e
        raise RuntimeError()

    def run(self) -> int:
        return super().run()

    def is_alive(self) -> bool:
        return super().is_alive()

    def terminate(self) -> int:
        return self.process.terminate()


player_class[__AUTO] = AutoPlayer


if __name__ == '__main__':
    for i in __PLAYERS_AND_AUTO:
        assert i in ALIAS
        assert i in player_class
    assert len(__PLAYERS_AND_AUTO) == len(ALIAS)
    assert len(__PLAYERS_AND_AUTO) == len(player_class)
