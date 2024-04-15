import cv2
import numpy as np


def get_buffer(
    img: np.ndarray, x: int, y: int, colorful: bool = False,
    fontmap: list = list(), contrast: bool = False,
) -> str:
    buffer = ''

    if colorful:
        img = cv2.resize(img, (x, y//2))
        # np.ndarray(shape=(y, x, 3), dtype=np.uint8)
        # x*y subpixel = x*y pixel = x*y char
        for j in range(y//2):
            for k in range(x):
                buffer += '\x1b[48;2;%d;%d;%dm ' % tuple(img[j, k][-1::-1])
            buffer += '\x1b[0m\n'
        return buffer

    img = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (x, y))
    # np.ndarray(shape=(y, x), dtype=np.uint8)
    # x*y subpixel = x*y/2 pixel = x*y/2 char

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
