import os
from multiprocessing import Process

from .util import get_func, Timer
from .audio import get_player


def replay(
    p_list: list[Process],
    video: str, audio: str, player: str,
    need_clear: bool = True, debug: bool = False
) -> None:
    video = os.path.abspath(video)
    open(video, 'r').close()
    p = get_player(audio, player)

    s = open(video, 'r').read().split('\n\n')
    x, y, clk = s[0].split()
    x = int(x)
    y = int(y)
    clk = float(clk) / 1000.0

    print('[%d:%d %.2lfHz replay]' % (x, y, 1.0/clk))

    rewind, clear, console_size = get_func(need_clear)

    timer = Timer(clk)
    print('BEGINNING...', flush=True)
    timer.slp()
    if p:
        p_list.append(p)
        p.start()
    if debug:
        timer.slp(5)
    rewind()
    clear()
    if not debug:
        console_size(x, y//2+1)
        rewind()
        clear()
    timer.bg()

    for i in s[1:]:
        rewind()
        print(i, flush=True)
        timer.wait()
