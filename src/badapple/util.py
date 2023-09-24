import os
import time
from typing import Tuple, Callable


def console_size(x: int, y: int) -> int:
    order = 'mode con cols=%d lines=%d' % (x, y)
    return os.system(order)


def rewind() -> None:
    print('\x1b[256F', end='', flush=True)


def clear() -> None:
    print('\x1b[0J', end='', flush=True)


def func_pass() -> None:
    pass


def get_func(need_clear: bool = True) -> Tuple[Callable, Callable, Callable]:
    if need_clear:
        return rewind, clear, console_size
    else:
        return print, func_pass, func_pass


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


def which(program: str) -> str:
    if os.name == "nt" and not program.lower().endswith(".exe"):
        program += ".EXE"

    envdir_list = [os.curdir] + os.environ["PATH"].split(os.pathsep)

    for envdir in envdir_list:
        program_path = os.path.join(envdir, program)
        if os.path.isfile(program_path) and os.access(program_path, os.X_OK):
            return program_path
