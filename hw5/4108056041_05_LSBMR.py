import cv2
import numpy as np
import os
import random
import math

RATIO = 0.2


def lsb(num):
    return bin(num)[-1]


def func(n1, n2):
    return (lsb(math.floor(n1 / 2) + n2))


def rand(num):
    random.seed(200)
    rnd = random.randint(0, 1)

    if rnd == 0:
        if num != 0:
            num -= 1
        else:
            num += 1
    else:
        if num != 255:
            num += 1
        else:
            num -= 1

    return num


def lsbmr(secret_mes, cover_img):

    print(cover_img.shape)
    h, w, c = cover_img.shape

    (b, g, r) = cv2.split(cover_img)
    print(b.shape)
    b = b.flatten()
    g = g.flatten()
    r = r.flatten()

    list_color = (b, g, r)

    # print("len")
    # print(len(secret_mes))
    # print(round(RATIO * len(secret_mes), 0))

    mes_len = int(RATIO * len(secret_mes))

    for color in list_color:
        for i in range(0, mes_len, 2):
            if secret_mes[i] == lsb(color[i]):
                if secret_mes[i+1] != func(color[i], color[i+1]):
                    color[i+1] = rand(color[i+1])
                else:
                    color[i+1] = color[i+1]
                color[i] = color[i]
            else:
                if secret_mes[i+1] == func(color[i]-1, color[i+1]):
                    color[i] = color[i] - 1
                else:
                    color[i] = color[i] + 1
                color[i+1] = color[i+1]

    b = b.reshape(h, w)
    g = g.reshape(h, w)
    r = r.reshape(h, w)
    print(b.shape)

    transfer = cv2.merge([b, g, r])

    return transfer


if __name__ == "__main__":

    # initial variables
    dir_cover = "cover"
    dir_stego = "stego"
    list = []
    list_name = []

    # read pic in test file
    entries = os.listdir(dir_cover)

    for entry in entries:
        img = cv2.imread(dir_cover + "/" + entry)
        print(entry.replace(".png", ""))

        list.append(img)
        list_name.append(entry.replace(".png", ""))

    # embedding message with LSBMR
    for i in range(9):
        print(i+1)

        # create secret message
        random.seed(100)
        h, w, c = list[i].shape
        mes_len = h * w
        secret_mes = np.full(mes_len, random.randint(0, 1))

        # LSBMR
        lsbmr(secret_mes, list[i])

        # create lsbmr img
