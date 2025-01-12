import os
import time

from .util import get_func
from .audio import get_player


def replay(
    p_list: list,
    video_pth: str, audio_pth: str, player: str,
    message: str, need_clear: bool = True, debug: bool = False
) -> None:
    video_pth = os.path.abspath(video_pth)
    open(video_pth, 'r').close()
    p = get_player(audio_pth, player)

    s = open(video_pth, 'r').read().split('\n\n')
    x, y, clk = s[0].split()
    x = int(x)
    y = int(y)
    clk = float(clk) / 1000.0

    print('[%d:%d %.2lfHz ] -%s-> [replay] %s' % (
        x, y, 1.0/clk, p.name if p else '', message
    ), flush=True)

    rewind, clear, console_resize = get_func(need_clear)

    # print('BEGINNING...', flush=True)
    time.sleep(1)
    if p:
        p_list.append(p)
        p.start()
    if debug:
        time.sleep(5)
    rewind()
    clear()
    if not debug:
        # console_resize(x, y//2+1)
        rewind()
        clear()

    t0 = time.time()
    for i in s[1:]:
        rewind()
        # clear()
        print(i, flush=True)

        t1 = time.time()
        while t1 - t0 < clk:
            t1 = time.time()
        t0 = t1
