import os
import time


def console_size(x: int, y: int) -> int:
    order = 'mode con cols=%d lines=%d' % (x, y)
    return os.system(order)


def rewind() -> None:
    print('\x1b[256F', end='', flush=True)


def clear() -> None:
    print('\x1b[0J', end='', flush=True)


class Font:
    def __init__(self, font: str = '') -> None:
        if not font:
            font = os.path.join(os.path.dirname(__file__),
                                'consola_ascii_0_ff.data')
        self.M = open(font, 'r').read().split('\n')

    def get(self, x: int, y: int) -> str:
        return self.M[x][y]


class Timer:
    def __init__(self, clk: float) -> None:
        self.clk = clk

    def bg(self) -> None:
        self.t0 = time.time()

    def wait(self) -> None:
        t1 = time.time()
        while t1 - self.t0 < self.clk:
            t1 = time.time()
        self.t0 = t1

    def slp(self, s: int = 1) -> None:
        time.sleep(s)
