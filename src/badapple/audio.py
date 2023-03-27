import os
import threading

# __FFPLAY = 'ffplay'
__PLAYSOUND = 'playsound'

__NONE = 'none'
# __ALL = 'all'
__ALL_LIST = [__PLAYSOUND]

'''
'qwq' is bad str
'ffplay' unavailable
'' get none
'''


def available(player: str) -> bool:
    if player not in __ALL_LIST:
        return False
    if player == __PLAYSOUND:
        try:
            import playsound
        except ImportError:
            return False
        return True


def get_available() -> str:
    for player in __ALL_LIST:
        if available(player):
            return player
    return __NONE


def preplaya(audio: str, player: str, video: str = None) -> tuple:
    if audio:
        audio = os.path.abspath(audio)
        if not player:
            player = get_available()
            if player == __NONE:
                raise ValueError('No available audio player')
    else:
        if not player:
            return '', ''
        if video is None:
            raise FileNotFoundError(audio)
        audio = video
        if player not in __ALL_LIST:
            raise ValueError(player)
        if not available(player):
            raise ImportError(player)
    open(audio, 'rb').close()
    return audio, player


def playa(audio: str):
    from playsound import playsound
    audio = audio.replace('\\', '/')
    _t = threading.Thread(target=playsound, args=(audio,), daemon=True)
    _t.start()
    return _t
