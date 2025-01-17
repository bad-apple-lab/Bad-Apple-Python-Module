import sys
import time
import numpy as np

t_bgr = 0.
t_rgb = 0.
t_ibgr = 0.
t_irgb = 0.
t_ibgr_u8 = 0.
t_irgb_u8 = 0.
 
y, x = 96, 54
n_pixels = x * y
message = 'hell_word'
n_tile = n_pixels // len(message) + 1
m_str = message * n_tile
m_str = m_str[:n_pixels]
m_nd = np.tile(list(message), n_tile)[:n_pixels]
m_u8 = np.array(list(map(ord, m_str)), dtype=np.uint8)

for epoch in range(4096):
    img = np.random.randint(0, 256, (x, y, 3), dtype=np.uint8)
    for __ in range(8):
        # t0 = time.time()
        # img_bgr = img.reshape(-1, 3)
        # color_seqs = [
        #     '\x1b[38;2;%d;%d;%dm%s' % (
        #         r, g, b, c
        #     ) for (b, g, r), c in zip(img_bgr, m_nd)
        # ]
        # x_bgr = '\x1b[0m\n'.join([
        #     ''.join(color_seqs[i:i+y]) for i in range(0, n_pixels, y)
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_bgr += t1 - t0

        # t0 = time.time()
        # img_rgb = img.reshape(-1, 3)[:, ::-1]
        # color_seqs = [
        #     '\x1b[38;2;%d;%d;%dm%s' % (
        #         r, g, b, c
        #     ) for (r, g, b), c in zip(img_rgb, m_nd)
        # ]
        # x_rgb = '\x1b[0m\n'.join([
        #     ''.join(color_seqs[i:i+y]) for i in range(0, n_pixels, y)
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_rgb += t1 - t0

        t0 = time.time()
        img_ibgr = img.reshape(-1, 3)
        color_seqs = [
            '\x1b[38;2;%d;%d;%dm%s' % (
                img_ibgr[i, 2], img_ibgr[i, 1], img_ibgr[i, 0], m_nd[i]
            ) for i in range(n_pixels)
        ]
        x_ibgr = '\x1b[0m\n'.join([
            ''.join(color_seqs[i:i+y]) for i in range(0, n_pixels, y)
        ]) + '\x1b[0m'
        t1 = time.time()
        t_ibgr += t1 - t0

        t0 = time.time()
        img_ibgr_u8 = img.reshape(-1, 3)
        color_seqs = [
            '\x1b[38;2;%d;%d;%dm%s' % (
                img_ibgr_u8[i, 2], img_ibgr_u8[i, 1], img_ibgr_u8[i, 0], chr(m_u8[i])
            ) for i in range(n_pixels)
        ]
        x_ibgr_u8 = '\x1b[0m\n'.join([
            ''.join(color_seqs[i:i+y]) for i in range(0, n_pixels, y)
        ]) + '\x1b[0m'
        t1 = time.time()
        t_ibgr_u8 += t1 - t0

        t0 = time.time()
        img_irgb = img.reshape(-1, 3)[:, ::-1]
        color_seqs = [
            '\x1b[38;2;%d;%d;%dm%s' % (
                img_irgb[i, 0], img_irgb[i, 1], img_irgb[i, 2], m_nd[i]
            ) for i in range(n_pixels)
        ]
        x_irgb = '\x1b[0m\n'.join([
            ''.join(color_seqs[i:i+y]) for i in range(0, n_pixels, y)
        ]) + '\x1b[0m'
        t1 = time.time()
        t_irgb += t1 - t0

        t0 = time.time()
        img_irgb_u8 = img.reshape(-1, 3)[:, ::-1]
        color_seqs = [
            '\x1b[38;2;%d;%d;%dm%s' % (
                img_irgb_u8[i, 0], img_irgb_u8[i, 1], img_irgb_u8[i, 2], chr(m_u8[i])
            ) for i in range(n_pixels)
        ]
        x_irgb_u8 = '\x1b[0m\n'.join([
            ''.join(color_seqs[i:i+y]) for i in range(0, n_pixels, y)
        ]) + '\x1b[0m'
        t1 = time.time()
        t_irgb_u8 += t1 - t0

        # assert x_bgr == x_rgb == x_ibgr == x_irgb
        assert x_ibgr == x_irgb == x_ibgr_u8 == x_irgb_u8

# print('t_rgb:', t_rgb)
# print('t_bgr:', t_bgr)
print('t_irgb:', t_irgb)
print('t_ibgr:', t_ibgr)
print('t_irgb_u8:', t_irgb_u8)
print('t_ibgr_u8:', t_ibgr_u8)

# t_irgb: 89.48329663276672
# t_ibgr: 92.00105714797974
# t_irgb_u8: 77.12398552894592
# t_ibgr_u8: 76.40172123908997

# t_rgb: 28.045297622680664
# t_bgr: 28.101086616516113
# t_irgb: 22.81760549545288
# t_ibgr: 22.448665857315063
