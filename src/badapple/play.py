import os
import cv2
import numpy as np
from multiprocessing import Process

from .util import get_func, Timer, Font
from .audio import preplaya, p_playa
from .replay import replay


def get_buffer(
    fnt: Font, img: np.ndarray,
    x: int, y: int,
    contrast: bool = False,
):
    img = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (x, y))
    # ndarray(shape=(y, x), dtype=np.uint8)

    if contrast:
        max_pixel = np.max(img)
        min_pixel = np.min(img)
        if max_pixel == min_pixel:
            if max_pixel >= 128:
                img = np.full((y, x), 0xff, dtype=np.uint8)
            else:
                img = np.zeros((y, x), dtype=np.uint8)
        else:
            max_min = max_pixel - min_pixel
            img = (((img.astype(dtype=np.uint16) - min_pixel) * 0xff +
                    max_min // 2) // max_min).astype(dtype=np.uint8)

    buffer = ''
    for j in range(y//2):
        for k in range(x):
            buffer += fnt.get(img[j*2, k], img[j*2+1, k])
        buffer += '\n'

    return buffer


def play(
    p_list: list[Process],
    video: str, output: str,
    font: str, audio: str, player: str,
    x: int, y: int, fps: int,
    need_clear: bool = True, check_player: bool = True,
    contrast: bool = False, preload: bool = False,
    debug: bool = False
) -> None:
    if video.endswith('.badapple'):
        return replay(
            p_list,
            video, audio, player,
            need_clear, check_player,
            debug
        )

    video = os.path.abspath(video)
    open(video, 'rb').close()
    audio, player = preplaya(audio, player, video, check_player=check_player)
    if debug:
        print(audio, player)

    x = int(x)
    y = int(y)
    y += y & 1

    capture = cv2.VideoCapture(video)
    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    width = int(width + 0.5)
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    height = int(height + 0.5)
    nb_frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    nb_frames = int(nb_frames + 0.5)
    rate = capture.get(cv2.CAP_PROP_FPS)
    duration = nb_frames / rate

    mo = max(int(0.5 + rate / fps), 1)
    clk = mo / rate

    print('[%d:%d %.2lfHz] -> [%d:%d %.2lfHz] %.3lfs' %
          (width, height, rate, x, y, rate / mo, duration), flush=True)
    # [1444:1080 29.97Hz] -> [76:54 9.99Hz] 232.065s

    rewind, clear, console_size = get_func(need_clear)
    fnt = Font(font)

    if output or preload:
        if not output:
            output = video + '.badapple'
        output = os.path.abspath(output)

        with open(output, 'w') as fp:
            fp.write('%d %d %d\n\n' % (x, y, int(clk*1000+0.5)))
            fp.flush()

            for i in range(nb_frames):
                succ, img = capture.read()
                if not succ:
                    raise Exception(i)
                if i % mo:
                    continue
                buffer = get_buffer(fnt, img, x, y, contrast)

                fp.write(buffer + '\n')
                fp.flush()

    else:
        timer = Timer(clk)
        print('BEGINNING...', flush=True)
        timer.slp()
        if audio:
            p = p_playa(audio, player)
            p_list.append(p)
            timer.slp(0.1)
        if debug:
            timer.slp(5)
        rewind()
        clear()
        if not debug:
            console_size(x, y//2+1)
            rewind()
            clear()
        timer.bg()

        for i in range(nb_frames):
            succ, img = capture.read()
            if not succ:
                raise Exception(i)
            if i % mo:
                continue
            buffer = get_buffer(fnt, img, x, y, contrast)

            rewind()
            print(buffer, end='', flush=True)
            timer.wait()
