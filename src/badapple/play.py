import os
import cv2

from .util import get_func, Timer, Font
from .audio import get_player
from .replay import replay
from .frame2str import get_buffer


def play(
    p_list: list,
    video: str, output: str,
    font: str, audio: str, player: str,
    x: int, y: int, fps: int, colorful: bool = False,
    need_clear: bool = True, contrast: bool = False, preload: bool = False,
    debug: bool = False
) -> None:
    if video.endswith('.badapple'):
        return replay(
            p_list,
            video, audio, player,
            need_clear, debug
        )

    video = os.path.abspath(video)
    open(video, 'rb').close()
    p = get_player(audio, player, video)

    capture = cv2.VideoCapture(video)
    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    width = int(width + 0.5)
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    height = int(height + 0.5)
    nb_frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    nb_frames = int(nb_frames + 0.5)
    rate = capture.get(cv2.CAP_PROP_FPS)
    if rate < 0.1:
        raise Exception("The frame rate is %s!" % str(rate))
    duration = nb_frames / rate

    mo = max(int(0.5 + rate / fps), 1)
    clk = mo / rate

    max_x, max_y = os.get_terminal_size()
    max_y = (max_y-1)*2

    x = int(x)
    y = int(y)

    if x > 0:
        if y > 0:
            # x = x
            # y = y
            pass
        else:
            # x = x
            y = int(height*x/width + 0.5)
    else:
        if y > 0:
            x = int(width*y/height + 0.5)
            # y = y
        else:
            x = min(max_x, int(width*max_y/height + 0.5))
            y = min(max_y, int(height*max_x/width + 0.5))

    if y % 2:
        if y == max_y+1:
            y = max_y
        else:
            y += 1

    print('[%d:%d %.2lfHz] -%s-> [%d:%d %.2lfHz] %.3lfs/%dms%s' % (
        width, height, rate,
        p.name if p else '',
        x, y, rate / mo,
        duration, clk*1000+0.5,
        ' [debug]' if debug else ''
    ), flush=True)
    # [1444:1080 29.97Hz] -ffplay-> [72:54 9.99Hz] 232.065s

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
                buffer = get_buffer(fnt, img, x, y, colorful, contrast)

                fp.write(buffer + '\n')
                fp.flush()

    else:
        timer = Timer(clk)
        # print('BEGINNING...', flush=True)
        timer.slp()
        if p:
            p_list.append(p)
            p.start()
        if debug:
            timer.slp(5)
        rewind()
        clear()
        if not debug:
            # console_size(x, y//2+1)
            rewind()
            clear()
        timer.bg()

        for i in range(nb_frames):
            succ, img = capture.read()
            if not succ:
                raise Exception(i)
            if i % mo:
                continue
            buffer = get_buffer(fnt, img, x, y, colorful, contrast)

            rewind()
            print(buffer, end='', flush=True)
            timer.wait()
