import sys
import time
import numpy as np
import cv2

t_gray_1st = 0.
t_resize_1st = 0.
_max_err = 0.

for epoch in range(4096):
    img = np.random.randint(0, 255, (1920, 1080, 3), dtype=np.uint8)

    for x, y in [(96, 54), (192, 108), (66, 44), (100, 100)]:
        for __ in range(8):
            t0 = time.time()
            _i = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # print(_i.shape)
            img2 = cv2.resize(_i, (x, y))
            # print(img2.shape)
            t1 = time.time()
            t_gray_1st += t1 - t0

            t0 = time.time()
            _i = cv2.resize(img, (x, y))
            # print(_i.shape)
            img3 = cv2.cvtColor(_i, cv2.COLOR_BGR2GRAY)
            # print(img3.shape)
            t1 = time.time()
            t_resize_1st += t1 - t0

            err = np.abs(
                img2.astype(np.int16)-img3.astype(np.int16)
            ).sum() / (x*y)
            assert 0. < err < .5
            _max_err = max(_max_err, err)

        for __ in range(8):
            t0 = time.time()
            _i = cv2.resize(img, (x, y))
            # print(_i.shape)
            img3 = cv2.cvtColor(_i, cv2.COLOR_BGR2GRAY)
            # print(img3.shape)
            t1 = time.time()
            t_resize_1st += t1 - t0

            t0 = time.time()
            _i = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # print(_i.shape)
            img2 = cv2.resize(_i, (x, y))
            # print(img2.shape)
            t1 = time.time()
            t_gray_1st += t1 - t0

            err = np.abs(
                img2.astype(np.int16)-img3.astype(np.int16)
            ).sum() / (x*y)
            assert 0. < err < .5
            _max_err = max(_max_err, err)

    if epoch % 256 == 0:
        print('epoch:', epoch, 'max_err:', _max_err)
        _max_err = 0.

print(t_gray_1st, t_resize_1st)
# 33.83021092414856 6.749794244766235
