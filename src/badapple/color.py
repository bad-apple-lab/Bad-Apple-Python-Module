import cv2
import numpy as np

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
    try:
        import x256offline
        COLOR_LIST += COLOR_X256_LIST
    except ImportError:
        pass


def get_buffer(
    img: np.ndarray, x: int, y: int, color: str, message: str,
    fontmap: list, contrast: bool
) -> str:
    if color not in COLOR_LIST:
        raise ValueError('%s is not a supported color type' % color)

    buffer = ''

    if color == COLOR_ASCII:
        img = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (x, y))
        # np.ndarray(shape=(y, x), dtype=np.uint8)
        # x*y subpixel == x*y/2 pixel == x*y/2 char

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

        for j in range(y//2):
            for k in range(x):
                buffer += fontmap[img[j*2, k]][img[j*2+1, k]]
            buffer += '\n'

        return buffer

    elif color == COLOR_RGB24:
        y = y // 2
        img = cv2.resize(img, (x, y))
        # np.ndarray(shape=(y, x, 3), dtype=np.uint8)
        # x*y subpixel == x*y pixel == x*y char
        for j in range(y):
            for k in range(x):
                buffer += '\x1b[48;2;%d;%d;%dm ' % tuple(img[j, k][-1::-1])
            buffer += '\x1b[0m\n'

    elif color in COLOR_X256_LIST:
        import x256offline as x256
        y = y // 2
        img = cv2.resize(img, (x, y))
        weighted = color in  [COLOR_X256W, COLOR_X232W]
        n_color = 232 if color in [COLOR_X232E, COLOR_X232W] else 256
        for j in range(y):
            for k in range(x):
                tuple(img[j, k][-1::-1])
                buffer += '\x1b[48;5;%dm ' % x256.from_rgb(
                    img[j, k, 2], img[j, k, 1], img[j, k, 0],
                    weighted, n_color
                )
            buffer += '\x1b[0m\n'

    elif color == COLOR_HALFWIDTH:
        y = y // 2
        img = cv2.resize(img, (x, y))
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
        m = message * (x*y//len(message)+1)
        mi = 0
        for j in range(y):
            for k in range(x):
                buffer += '\x1b[38;2;%d;%d;%dm' % tuple(img[j, k][-1::-1])
                buffer += m[mi]
                mi += 1
            buffer += '\x1b[0m\n'

    return buffer
