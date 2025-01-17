import sys
import time
import numpy as np

t_bgr_f = 0.
t_bgr_mo = 0.
t_bgr_add = 0.
t_rgb_f = 0.
t_rgb_mo = 0.
t_rgb_mot = 0.
t_rgb_add = 0.
t_flat_bgr_f = 0.
t_flat_bgr_mo = 0.
t_flat_bgr_add = 0.
t_flat_rgb_f = 0.
t_flat_rgb_mo = 0.
t_flat_rgb_mot = 0.
t_flat_rgb_add = 0.

t_ibgr = 0.
t_irgb = 0.
t_flat_ibgr = 0.
t_flat_irgb = 0.

y, x = 96, 54
n_pixels = x * y

for epoch in range(4096):
    img = np.random.randint(0, 256, (x, y, 3), dtype=np.uint8)

    for __ in range(8):
        # # flat bgr f-string
        # t0 = time.time()
        # img_flat_bgr_f = img.reshape(-1, 3)
        # color_seqs = [
        #     f'\x1b[48;2;{r};{g};{b}m ' for b, g, r in img_flat_bgr_f
        # ]
        # s_flat_bgr_f = '\x1b[0m\n'.join([
        #     ''.join(color_seqs[i:i+y]) for i in range(0, len(color_seqs), y)
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_flat_bgr_f += t1 - t0

        # # flat bgr modulo
        # t0 = time.time()
        # img_flat_bgr_mo = img.reshape(-1, 3)
        # color_seqs = [
        #     '\x1b[48;2;%d;%d;%dm ' % (r, g, b) for b, g, r in img_flat_bgr_mo
        # ]
        # s_flat_bgr_mo = '\x1b[0m\n'.join([
        #     ''.join(color_seqs[i:i+y]) for i in range(0, len(color_seqs), y)
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_flat_bgr_mo += t1 - t0

        # # flat ibgr modulo
        # t0 = time.time()
        # img_flat_ibgr = img.reshape(-1, 3)
        # color_seqs = [
        #     '\x1b[48;2;%d;%d;%dm ' % (
        #         img_flat_ibgr[i, 2], img_flat_ibgr[i, 1], img_flat_ibgr[i, 0]
        #     ) for i in range(n_pixels)
        # ]
        # s_flat_ibgr = '\x1b[0m\n'.join([
        #     ''.join(color_seqs[i:i+y]) for i in range(0, len(color_seqs), y)
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_flat_ibgr += t1 - t0

        # # flat bgr add
        # t0 = time.time()
        # img_flat_bgr_add = img.reshape(-1, 3)
        # color_seqs = [
        #     '\x1b[48;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm '
        #         for b, g, r in img_flat_bgr_add
        # ]
        # s_flat_bgr_add = '\x1b[0m\n'.join([
        #     ''.join(color_seqs[i:i+y]) for i in range(0, len(color_seqs), y)
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_flat_bgr_add += t1 - t0

        # # flat rgb f-string
        # t0 = time.time()
        # img_flat_rgb_f = img.reshape(-1, 3)[:, ::-1]
        # color_seqs = [
        #     f'\x1b[48;2;{r};{g};{b}m ' for r, g, b in img_flat_rgb_f
        # ]
        # s_flat_rgb_f = '\x1b[0m\n'.join([
        #     ''.join(color_seqs[i:i+y]) for i in range(0, len(color_seqs), y)
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_flat_rgb_f += t1 - t0

        # # flat rgb modulo
        # t0 = time.time()
        # img_flat_rgb_mo = img.reshape(-1, 3)[:, ::-1]
        # color_seqs = [
        #     '\x1b[48;2;%d;%d;%dm ' % (r, g, b) for r, g, b in img_flat_rgb_mo
        # ]
        # s_flat_rgb_mo = '\x1b[0m\n'.join([
        #     ''.join(color_seqs[i:i+y]) for i in range(0, len(color_seqs), y)
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_flat_rgb_mo += t1 - t0

        # # flat irgb modulogb
        # t0 = time.time()
        # img_flat_irgb = img.reshape(-1, 3)[:, ::-1]
        # color_seqs = [
        #     '\x1b[48;2;%d;%d;%dm ' % (
        #         img_flat_irgb[i, 0], img_flat_irgb[i, 1], img_flat_irgb[i, 2]
        #     ) for i in range(n_pixels)
        # ]
        # s_flat_irgb = '\x1b[0m\n'.join([
        #     ''.join(color_seqs[i:i+y]) for i in range(0, len(color_seqs), y)
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_flat_irgb += t1 - t0

        # # flat rgb modulo tuple
        # t0 = time.time()
        # img_flat_rgb_mot = img.reshape(-1, 3)[:, ::-1]
        # color_seqs = [
        #     '\x1b[48;2;%d;%d;%dm ' % tuple(rgb) for rgb in img_flat_rgb_mot
        # ]
        # s_flat_rgb_mot = '\x1b[0m\n'.join([
        #     ''.join(color_seqs[i:i+y]) for i in range(0, len(color_seqs), y)
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_flat_rgb_mot += t1 - t0

        # # flat rgb add
        # t0 = time.time()
        # img_flat_rgb_add = img.reshape(-1, 3)[:, ::-1]
        # color_seqs = [
        #     '\x1b[48;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm '
        #         for r, g, b in img_flat_rgb_add
        # ]
        # s_flat_rgb_add = '\x1b[0m\n'.join([
        #     ''.join(color_seqs[i:i+y]) for i in range(0, len(color_seqs), y)
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_flat_rgb_add += t1 - t0

        # # bgr f-string
        # t0 = time.time()
        # s_bgr_f = '\x1b[0m\n'.join([
        #     ''.join([
        #         f'\x1b[48;2;{r};{g};{b}m ' for b, g, r in row
        #     ]) for row in img
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_bgr_f += t1 - t0

        # # bgr modulo
        # t0 = time.time()
        # s_bgr_mo = '\x1b[0m\n'.join([
        #     ''.join([
        #         '\x1b[48;2;%d;%d;%dm ' % (r, g, b) for b, g, r in row
        #     ]) for row in img
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_bgr_mo += t1 - t0

        # ibgr modulo
        t0 = time.time()
        s_ibgr = '\x1b[0m\n'.join([
            ''.join([
                '\x1b[48;2;%d;%d;%dm ' % (
                    row[i, 2], row[i, 1], row[i, 0]
                ) for i in range(y)
            ]) for row in img
        ]) + '\x1b[0m'
        t1 = time.time()
        t_ibgr += t1 - t0

        # # bgr add
        # t0 = time.time()
        # s_bgr_add = '\x1b[0m\n'.join([
        #     ''.join([
        #         '\x1b[48;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm '
        #             for b, g, r in row
        #     ]) for row in img
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_bgr_add += t1 - t0

        # # rgb f-string
        # t0 = time.time()
        # img_rgb_f = img[:, :, ::-1]
        # s_rgb_f = '\x1b[0m\n'.join([
        #     ''.join([
        #         f'\x1b[48;2;{r};{g};{b}m ' for r, g, b in row
        #     ]) for row in img_rgb_f
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_rgb_f += t1 - t0

        # # rgb modulo
        # t0 = time.time()
        # img_rgb_mo = img[:, :, ::-1]
        # s_rgb_mo = '\x1b[0m\n'.join([
        #     ''.join([
        #         '\x1b[48;2;%d;%d;%dm ' % (r, g, b) for r, g, b in row
        #     ]) for row in img_rgb_mo
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_rgb_mo += t1 - t0

        # irgb modulo
        t0 = time.time()
        img_irgb = img[:, :, ::-1]
        s_irgb = '\x1b[0m\n'.join([
            ''.join([
                '\x1b[48;2;%d;%d;%dm ' % (
                    row[i, 0], row[i, 1], row[i, 2]
                ) for i in range(y)
            ]) for row in img_irgb
        ]) + '\x1b[0m'
        t1 = time.time()
        t_irgb += t1 - t0

        # # rgb modulo tuple
        # t0 = time.time()
        # img_rgb_mot = img[:, :, ::-1]
        # s_rgb_mot = '\x1b[0m\n'.join([
        #     ''.join([
        #         '\x1b[48;2;%d;%d;%dm ' % tuple(rgb) for rgb in row
        #     ]) for row in img_rgb_mot
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_rgb_mot += t1 - t0

        # # rgb add
        # t0 = time.time()
        # img_rgb_add = img[:, :, ::-1]
        # s_rgb_add = '\x1b[0m\n'.join([
        #     ''.join([
        #         '\x1b[48;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm '
        #             for r, g, b in row
        #     ]) for row in img_rgb_add
        # ]) + '\x1b[0m'
        # t1 = time.time()
        # t_rgb_add += t1 - t0

        # assert s_bgr_f == s_rgb_f == s_flat_bgr_f == s_flat_rgb_f
        # assert s_bgr_mo == s_rgb_mo == s_flat_bgr_mo == s_flat_rgb_mo
        # assert s_rgb_mot == s_flat_rgb_mot
        # assert s_bgr_add == s_rgb_add == s_flat_bgr_add == s_flat_rgb_add
        # assert s_rgb_f == s_rgb_mo == s_rgb_mot == s_rgb_add
        assert s_ibgr == s_irgb
        # assert s_flat_ibgr == s_flat_irgb == s_ibgr == s_irgb
        # assert s_bgr_mo == s_ibgr

# print('bgr_f:', t_bgr_f)
# print('bgr_mo:', t_bgr_mo)
# print('bgr_add:', t_bgr_add)
# print('rgb_f:', t_rgb_f)
# print('rgb_mo:', t_rgb_mo)
# print('rgb_mot:', t_rgb_mot)
# print('rgb_add:', t_rgb_add)
# print('flat_bgr_f:', t_flat_bgr_f)
# print('flat_bgr_mo:', t_flat_bgr_mo)
# print('flat_bgr_add:', t_flat_bgr_add)
# print('flat_rgb_f:', t_flat_rgb_f)
# print('flat_rgb_mo:', t_flat_rgb_mo)
# print('flat_rgb_mot:', t_flat_rgb_mot)
# print('flat_rgb_add:', t_flat_rgb_add)

print('ibgr:', t_ibgr)
print('irgb:', t_irgb)
# print('flat_ibgr:', t_flat_ibgr)
# print('flat_irgb:', t_flat_irgb)

# ibgr: 59.912708044052124
# irgb: 59.90151786804199

# ibgr: 59.704137325286865
# irgb: 59.66081619262695
# flat_ibgr: 63.27284097671509
# flat_irgb: 63.6477735042572

# bgr_mo: 23.205034732818604
# rgb_mo: 23.194499015808105
# flat_bgr_mo: 22.882583141326904
# flat_rgb_mo: 22.788300037384033
# ibgr: 15.164149522781372
# irgb: 15.055457830429077
# flat_ibgr: 15.601244688034058
# flat_irgb: 15.577321529388428

# bgr_mo: 23.181134939193726
# rgb_mo: 23.205081701278687
# flat_bgr_mo: 22.881837129592896
# flat_rgb_mo: 22.801182508468628
# ibgr: 15.035505294799805
# irgb: 15.042108297348022
# flat_ibgr: 15.592838525772095
# flat_irgb: 15.579696655273438

# bgr_mo: 23.232539415359497
# rgb_mo: 23.20311450958252
# flat_bgr_mo: 22.9338059425354
# flat_rgb_mo: 22.876354455947876

# bgr_mo: 23.34119725227356
# rgb_mo: 23.3236141204834
# flat_bgr_mo: 22.98596715927124
# flat_rgb_mo: 22.894139289855957

# bgr_f: 6.899893760681152
# bgr_mo: 5.8551270961761475
# rgb_f: 6.9095423221588135
# rgb_mo: 5.860572338104248
# rgb_mot: 6.161131858825684
# flat_bgr_f: 6.789405345916748
# flat_bgr_mo: 5.691295862197876
# flat_rgb_f: 6.765195846557617
# flat_rgb_mo: 5.719106912612915
# flat_rgb_mot: 5.945274353027344

# bgr_f: 6.860884189605713
# bgr_mo: 5.9187092781066895
# bgr_add: 6.482117414474487
# rgb_f: 6.855340480804443
# rgb_mo: 5.910832166671753
# rgb_mot: 6.272697687149048
# rgb_add: 6.522624969482422
# flat_bgr_f: 7.0467000007629395
# flat_bgr_mo: 5.909013986587524
# flat_bgr_add: 6.467011213302612
# flat_rgb_f: 6.93628454208374
# flat_rgb_mo: 5.876383066177368
# flat_rgb_mot: 6.209405183792114
# flat_rgb_add: 6.436383485794067
