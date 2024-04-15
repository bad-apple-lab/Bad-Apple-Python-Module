import os
import platform


def get_info() -> str:
    from . import VERSION
    return 'BadApple-Python-%s-%s-%s' % (
        platform.system(),
        platform.machine(),
        VERSION
    )


def console_size(x: int, y: int) -> int:
    order = 'mode con cols=%d lines=%d' % (x, y)
    return os.system(order)


def rewind() -> None:
    print('\x1b[256F', end='', flush=True)


def clear() -> None:
    print('\x1b[0J', end='', flush=True)


def func_pass() -> None:
    pass


def get_func(need_clear: bool = True):
    if need_clear:
        return rewind, clear, console_size
    else:
        return print, func_pass, func_pass
