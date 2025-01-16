import cv2
import numpy as np
import x256numpy

from .util import ansi_available

COLOR_ASCII = 'ascii'
COLOR_RGB24 = 'rgb24'
COLOR_HALFWIDTH = 'halfwidth'
COLOR_FULLWIDTH = 'fullwidth'
COLOR_X256E = 'x256e'
COLOR_X256W = 'x256w'
COLOR_X232E = 'x232e'
COLOR_X232W = 'x232w'

COLOR_LIST = [COLOR_ASCII]
COLOR_X256_LIST = [COLOR_X256E, COLOR_X256W, COLOR_X232E, COLOR_X232W]

if ansi_available():
    COLOR_LIST.append(COLOR_RGB24)
    COLOR_LIST.append(COLOR_HALFWIDTH)
    COLOR_LIST.append(COLOR_FULLWIDTH)
    COLOR_LIST += COLOR_X256_LIST


def get_buffer(
    img: np.ndarray, x: int, y: int, color: str, message: str,
    fontmap: np.ndarray, contrast: bool
) -> str:
    if color not in COLOR_LIST:
        raise ValueError('%s is not a supported color type' % color)

    buffer = ''

    if color == COLOR_ASCII:
        img = cv2.cvtColor(cv2.resize(img, (x, y)), cv2.COLOR_BGR2GRAY)
        # np.ndarray(shape=(y, x), dtype=np.uint8)
        # x*y pixel -> x*y/2 char

        if contrast:
            max_pixel = np.max(img)
            min_pixel = np.min(img)
            if max_pixel == min_pixel:
                # return '\n'.join([chr(fontmap[max_pixel, max_pixel])*x]*y)
                # img = np.full((y, x), max_pixel, dtype=np.uint8)
                if max_pixel >= 128:
                    return '\n'.join([chr(fontmap[0xff, 0xff])*x]*y)
                    # img = np.full_like(img, 0xff, dtype=np.uint8)
                else:
                    return '\n'.join([chr(fontmap[0, 0])*x]*y)
                    # img = np.zeros_like(img, dtype=np.uint8)
            else:
                max_min = max_pixel - min_pixel
                img = (((
                    img.astype(dtype=np.uint16) - min_pixel
                ) * 0xff + max_min // 2) // max_min).astype(dtype=np.uint8)

        # even_rows = img[::2, :]
        # odd_rows = img[1::2, :]
        chars = fontmap[img[::2, :], img[1::2, :]]

        return '\n'.join([''.join(map(chr, row)) for row in chars])

    elif color == COLOR_RGB24:
        y = y // 2
        img = cv2.resize(img, (x, y)).reshape(-1, 3)[:, ::-1]
        # np.ndarray(shape=(y/2, x, 3), dtype=np.uint8)
        # x*(y/2) pixel -> x*(y/2) char
        color_seqs = [
            '\x1b[48;2;%d;%d;%dm ' % (r, g, b) for r, g, b in img
        ]
        return '\x1b[0m\n'.join([
            ''.join(color_seqs[i:i+y]) for i in range(0, len(color_seqs), y)
        ]) + '\x1b[0m'

    elif color in COLOR_X256_LIST:
        y = y // 2
        img = cv2.resize(img, (x, y)).reshape(-1, 3)
        # np.ndarray(shape=(y/2, x, 3), dtype=np.uint8)
        # x*(y/2) pixel -> x*(y/2) char
        weighted = color in [COLOR_X256W, COLOR_X232W]
        n_color = 232 if color in [COLOR_X232E, COLOR_X232W] else 256
        ans = x256numpy.from_rgb(img[:, 2], img[:, 1], img[:, 0], weighted, n_color)
        color_seqs = [
            '\x1b[48;5;%dm ' % i for i in ans
        ]
        return '\x1b[0m\n'.join([
            ''.join(color_seqs[i:i+y]) for i in range(0, len(color_seqs), y)
        ]) + '\x1b[0m'

    elif color == COLOR_HALFWIDTH:
        y = y // 2
        img = cv2.resize(img, (x, y))
        # np.ndarray(shape=(y/2, x, 3), dtype=np.uint8)
        # x*(y/2) pixel -> x*(y/2) char
        m = message * (x*y//len(message)+1)
        mi = 0
        for j in range(y):
            for k in range(x):
                buffer += '\x1b[38;2;%d;%d;%dm' % tuple(img[j, k][-1::-1])
                buffer += m[mi]
                mi += 1
            buffer += '\x1b[0m\n'

    elif color == COLOR_FULLWIDTH:
        x = x // 2
        y = y // 2
        img = cv2.resize(img, (x, y))
        # np.ndarray(shape=(y/2, x/2, 3), dtype=np.uint8)
        # (x/2)*(y/2) pixel -> (x/2)*(y/2) char
        m = message * (x*y//len(message)+1)
        mi = 0
        for j in range(y):
            for k in range(x):
                buffer += '\x1b[38;2;%d;%d;%dm' % tuple(img[j, k][-1::-1])
                buffer += m[mi]
                mi += 1
            buffer += '\x1b[0m\n'

    return buffer
