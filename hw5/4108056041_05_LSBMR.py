import cv2
import numpy as np
import os
import random
import math

RATIO = 0.20


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

    h, w, c = cover_img.shape

    (b, g, r) = cv2.split(cover_img)
    b = b.flatten()
    g = g.flatten()
    r = r.flatten()
    list_color = (b, g, r)

    mes_len = int(RATIO * len(secret_mes))

    for color in list_color:
        for i in range(0, mes_len, 2):

            if str(secret_mes[i]) == lsb(color[i]):
                if str(secret_mes[i+1]) != func(color[i], color[i+1]):
                    color[i+1] = rand(color[i+1])
                else:
                    color[i+1] = color[i+1]
                color[i] = color[i]
            else:
                if str(secret_mes[i+1]) == func(color[i]-1, color[i+1]):
                    color[i] = color[i] - 1
                else:
                    color[i] = color[i] + 1
                color[i+1] = color[i+1]

    b = b.reshape(h, w)
    g = g.reshape(h, w)
    r = r.reshape(h, w)

    transfer = cv2.merge([b, g, r])

    return transfer


def check(secret_mes, embedding_img):

    (b, g, r) = cv2.split(embedding_img)
    b = b.flatten()
    g = g.flatten()
    r = r.flatten()
    list_color = (b, g, r)

    mes_len = int(RATIO * len(secret_mes))

    for color in list_color:
        for i in range(0, mes_len, 2):
            if str(secret_mes[i]) != lsb(color[i]):
                print("error! try again")
            elif str(secret_mes[i+1]) != func(color[i], color[i+1]):
                print("ko no dio da!!")


if __name__ == "__main__":

    # initial variables
    dir_cover = "cover"
    dir_stego = "stego/"
    list = []
    list_name = []

    # read pic in test file
    entries = os.listdir(dir_cover)

    for entry in entries:
        img = cv2.imread(dir_cover + "/" + entry)

        list.append(img)
        list_name.append(entry.replace(".png", ""))

    # embedding message with LSBMR
    for i in range(9):

        # create secret message
        random.seed(100)
        h, w, c = list[i].shape
        mes_len = h * w
        secret_mes = np.full(mes_len, random.randint(0, 1))
        '''
        random.seed(100)
        secret_mes = [random.randint(0,1) for _ in range(int(mesg_size))]
        '''

        # LSBMR
        embedding_img = lsbmr(secret_mes, list[i])

        # check
        check(secret_mes, embedding_img)

        # create lsbmr img
        path_name = dir_stego + list_name[i] + '_stego_' + str(RATIO) + ".png"
        cv2.imwrite(path_name, embedding_img)
