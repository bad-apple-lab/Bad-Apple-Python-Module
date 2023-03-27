import os
import cv2
import numpy as np

from .base import console_size, Timer, Font
from .audio import playa, preplaya
from .replay import replay


def play(
    video: str, output: str,
    font: str, audio: str, player: str,
    x: int, y: int, fps: int,
    not_clear: bool = False, contrast: bool = False, preload: bool = False,
    debug: bool = False
) -> None:
    if video.endswith('.badapple'):
        return replay(video, audio, player, not_clear, debug)

    video = os.path.abspath(video)
    open(video, 'rb').close()
    audio, player = preplaya(audio, player, video)
    if debug:
        print(audio, player)

    x = int(x)
    y = int(y)
    y += y & 1
    if not debug:
        console_size(x, y//2+1)

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

    if not_clear:
        def clear():
            return

        def rewind():
            return print()
    else:
        from .base import clear, rewind

    timer = Timer(clk)
    fnt = Font(font)

    if output:
        output = os.path.abspath(output)
        preload = True
    elif preload:
        output = video + '.badapple'

    if preload:
        fp = open(output, 'w')
        fp.flush()
        fp.write('%d %d %d\n\n' % (x, y, int(clk*1000+0.5)))
    else:
        print('BEGINNING...', flush=True)
        timer.slp()
        if audio:
            playa(audio)
            timer.slp(0.1)
        if debug:
            timer.slp(5)
        rewind()
        clear()
        timer.bg()

    for i in range(nb_frames):
        succ, img = capture.read()
        if not succ:
            raise Exception(i)
        if i % mo:
            continue

        img = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (x, y))
        # numpy.ndarray(shape=(y, x), dtype=np.uint8)

        if contrast:
            max_pixel = np.max(img)
            min_pixel = np.min(img)
            if max_pixel == min_pixel:
                if max_pixel >= 128:
                    img = np.full((y, x), 0xff, dtype=np.uint8)
                else:
                    img = np.zeros((y, x), dtype=np.uint8)
            else:
                img = ((img.astype(dtype=np.uint16) - min_pixel) *
                       0xff // (max_pixel - min_pixel)).astype(dtype=np.uint8)

        buffer = ''
        for j in range(y//2):
            for k in range(x):
                buffer += fnt.get(img[j*2, k], img[j*2+1, k])
            buffer += '\n'

        if preload:
            fp.write(buffer + '\n')
            fp.flush()
            pass
        else:
            rewind()
            print(buffer, end='', flush=True)
            timer.wait()

    if preload:
        fp.close()
