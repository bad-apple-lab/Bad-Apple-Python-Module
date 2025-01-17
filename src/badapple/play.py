import os
import time
import numpy as np
import cv2

from .util import get_func
from .audio import get_player
from .replay import replay
from .color import get_buffer


def play(
    p_list: list,
    video_pth: str, output_pth: str,
    x: int, y: int, fps: int,
    audio_pth: str, player: str,
    color: str, message: str, font_pth: str,
    need_clear: bool = True, contrast: bool = False, preload: bool = False,
    debug: bool = False, jump: int = 0
) -> None:
    if video_pth.endswith('.badapple'):
        return replay(
            p_list,
            video_pth, audio_pth, player,
            message, need_clear, debug
        )

    video_pth = os.path.abspath(video_pth)
    open(video_pth, 'rb').close()
    p = get_player(audio_pth, player, video_pth)

    capture = cv2.VideoCapture(video_pth)
    ori_x = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    ori_x = int(ori_x + 0.5)
    ori_y = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    ori_y = int(ori_y + 0.5)
    nb_frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    nb_frames = int(nb_frames + 0.5)
    ori_fps = capture.get(cv2.CAP_PROP_FPS)
    if ori_fps < 0.1:
        raise ValueError("The frame rate is %s!" % str(ori_fps))
    duration = nb_frames / ori_fps

    if jump >= nb_frames:
        return

    n_frames_get_1 = max(int(0.5 + ori_fps / fps), 1)
    clk = n_frames_get_1 / ori_fps

    terminal_x, terminal_y = os.get_terminal_size()  # columns, lines
    terminal_y = (terminal_y-1)*2

    x = int(x)
    y = int(y)

    if x > 0:
        if y > 0:
            # x = x
            # y = y
            pass
        else:
            # x = x
            y = int(ori_y*x/ori_x + 0.5)
    else:
        if y > 0:
            x = int(ori_x*y/ori_y + 0.5)
            # y = y
        else:
            x = min(terminal_x, int(ori_x*terminal_y/ori_y + 0.5))
            y = min(terminal_y, int(ori_y*terminal_x/ori_x + 0.5))

    if y % 2:
        if y == terminal_y+1:
            y = terminal_y
        else:
            y += 1

    rewind, clear, console_resize = get_func(need_clear)
    fontmap = np.array(
        [[ord(j) for j in i] for i in open(font_pth, 'r').read().split('\n')],
        dtype=np.uint8
    )

    print('[%d:%d %.2lfHz] -%s-> [%d:%d %.2lfHz] %.3lfs/%dms%s %s' % (
        ori_x, ori_y, ori_fps,
        p.name if p else '',
        x, y, ori_fps / n_frames_get_1,
        duration, clk*1000+0.5,
        ' [debug]' if debug else '',
        message
    ), flush=True)
    # [1444:1080 29.97Hz] -ffplay-> [72:54 9.99Hz] 232.065s

    if output_pth or preload:
        if not output_pth:
            output_pth = video_pth + '.badapple'
        output_pth = os.path.abspath(output_pth)

        with open(output_pth, 'w') as fp:
            fp.write('%d %d %d\n\n' % (x, y, int(clk*1000+0.5)))
            fp.flush()

            for i in range(jump):
                succ, img = capture.read()
                if not succ:
                    raise RuntimeError(i)

            for i in range(jump, nb_frames):
                succ, img = capture.read()
                if not succ:
                    raise RuntimeError(i)

                if i % n_frames_get_1:
                    continue
                buffer = get_buffer(
                    img, x, y, color, message,
                    fontmap, contrast
                )

                fp.write(buffer + '\n\n', flush=True)

    else:
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

        for i in range(jump):
            succ, img = capture.read()
            if not succ:
                raise RuntimeError(i)

        t0 = time.time()
        for i in range(jump, nb_frames):
            succ, img = capture.read()
            if not succ:
                raise RuntimeError(i)

            if i % n_frames_get_1:
                continue
            buffer = get_buffer(
                img, x, y, color, message,
                fontmap, contrast
            )

            rewind()
            # clear()
            print(buffer, flush=True)

            t1 = time.time()
            while t1 - t0 < clk:
                t1 = time.time()
            t0 = t1
