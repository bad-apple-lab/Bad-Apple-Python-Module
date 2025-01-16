import time
import numpy as np

font_pth = '../src/badapple/consola_ascii_0_ff.data'

fontmap_list = open(font_pth, 'r').read().split('\n')
fontmap_str = np.array([list(i) for i in fontmap_list])
fontmap_int = np.array(
    [[ord(j) for j in i] for i in fontmap_list],
    dtype=np.uint8
)

# t_list = 0.
t_str = 0.
t_int = 0.

for _ in range(4096):
    img = np.random.randint(0, 256, (96, 54), dtype=np.uint8)
    even_rows = img[::2, :]
    odd_rows = img[1::2, :]

    for __ in range(8):
        # t0 = time.time()
        # buffer = ''
        # for j in range(1024//2):
        #     for k in range(1024):
        #         buffer += fontmap_list[img[j*2, k]][img[j*2+1, k]]
        #     buffer += '\n'
        # t1 = time.time()
        # t_list += t1 - t0

        t0 = time.time()
        chars = fontmap_int[even_rows, odd_rows]
        s_int = '\n'.join(''.join(map(chr, row)) for row in chars) + '\n'
        t1 = time.time()
        t_int += t1 - t0

        t0 = time.time()
        chars = fontmap_str[even_rows, odd_rows]
        s_str = '\n'.join(''.join(row) for row in chars) + '\n'
        t1 = time.time()
        t_str += t1 - t0

        # assert s_str == s_int == buffer
        assert s_str == s_int

    for __ in range(8):
        # t0 = time.time()
        # buffer = ''
        # for j in range(1024//2):
        #     for k in range(1024):
        #         buffer += fontmap_list[img[j*2, k]][img[j*2+1, k]]
        #     buffer += '\n'
        # t1 = time.time()
        # t_list += t1 - t0

        t0 = time.time()
        chars = fontmap_str[even_rows, odd_rows]
        s_str = '\n'.join(''.join(row) for row in chars) + '\n'
        t1 = time.time()
        t_str += t1 - t0

        t0 = time.time()
        chars = fontmap_int[even_rows, odd_rows]
        s_int = '\n'.join(''.join(map(chr, row)) for row in chars) + '\n'
        t1 = time.time()
        t_int += t1 - t0

        # assert s_str == s_int == buffer
        assert s_str == s_int

# print(t_list)
# 18.97425127029419
# 0.2764561176300049 0.13903474807739258

print(t_str, t_int)
# 26.038525581359863 15.008537769317627
