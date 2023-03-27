import os

from .base import console_size, Timer
from .audio import playa, preplaya


def replay(
    video: str, audio: str, player: str,
    not_clear: bool = False,
    debug: bool = False
) -> None:
    video = os.path.abspath(video)
    open(video, 'r').close()
    audio, player = preplaya(audio, player)
    if debug:
        print(audio, player)

    s = open(video, 'r').read().split('\n\n')
    x, y, clk = s[0].split()
    x = int(x)
    y = int(y)
    if not debug:
        console_size(x, y+1)
    clk = float(clk) / 1000.0

    print('[%d:%d %.2lfHz replay]' % (x, y, 1.0/clk))

    if not_clear:
        def clear():
            return

        def rewind():
            return print()
    else:
        from .base import clear, rewind

    timer = Timer(clk)

    print('BEGINNING...', flush=True)
    timer.slp()
    if audio:
        playa(audio)
        timer.slp(0.01)
    if debug:
        timer.slp(5)
    rewind()
    clear()
    timer.bg()

    for i in s[1:]:
        rewind()
        print(i, end='', flush=True)
        timer.wait()
