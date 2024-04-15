import cv2
import numpy as np

from .util import ansi_available

COLOR_ASCII = 'ascii'
COLOR_RGB24 = 'rgb24'
COLOR_X256E = 'x256e'
COLOR_X256W = 'x256w'

COLOR_TYPE = [COLOR_ASCII]

if ansi_available():
    COLOR_TYPE.append(COLOR_RGB24)
    try:
        import x256offline
        COLOR_TYPE.append(COLOR_X256E)
        COLOR_TYPE.append(COLOR_X256W)
    except ImportError:
        pass


def get_buffer(
    img: np.ndarray, x: int, y: int, color: str,
    fontmap: list = list(), contrast: bool = False,
) -> str:
    if color not in COLOR_TYPE:
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
        img = cv2.resize(img, (x, y//2))
        # np.ndarray(shape=(y, x, 3), dtype=np.uint8)
        # x*y subpixel == x*y pixel == x*y char
        for j in range(y//2):
            for k in range(x):
                buffer += '\x1b[48;2;%d;%d;%dm ' % tuple(img[j, k][-1::-1])
            buffer += '\x1b[0m\n'

    elif color == COLOR_X256E:
        import x256offline as x256
        img = cv2.resize(img, (x, y//2))
        # np.ndarray(shape=(y, x, 3), dtype=np.uint8)
        # x*y subpixel == x*y pixel == x*y char
        for j in range(y//2):
            for k in range(x):
                tuple(img[j, k][-1::-1])
                buffer += '\x1b[48;5;%dm ' % x256.from_rgb(
                    img[j, k, 2],
                    img[j, k, 1],
                    img[j, k, 0],
                    False
                )
            buffer += '\x1b[0m\n'

    elif color == COLOR_X256W:
        import x256offline as x256
        img = cv2.resize(img, (x, y//2))
        # np.ndarray(shape=(y, x, 3), dtype=np.uint8)
        # x*y subpixel == x*y pixel == x*y char
        for j in range(y//2):
            for k in range(x):
                tuple(img[j, k][-1::-1])
                buffer += '\x1b[48;5;%dm ' % x256.from_rgb(
                    img[j, k, 2],
                    img[j, k, 1],
                    img[j, k, 0],
                    True
                )
            buffer += '\x1b[0m\n'

    return buffer
