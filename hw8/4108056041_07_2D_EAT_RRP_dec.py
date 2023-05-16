import cv2
import numpy as np
import os
import random


a, b = 1, 1
M = np.array([[a*b+1, -a],
              [-b, 1]])
G = 100


def RRP(pixel):

    # step1 : turn dec itno bin
    bin_pix = format(pixel, "b")
    l = len(bin_pix)
    j = 0

    list_bin = np.zeros(8)

    for i in range(8-l, 8, 1):

        list_bin[i] = bin_pix[j]
        j += 1

    # step2 : shuffle
    pos = [0, 1, 2, 3, 4, 5, 6, 7]

    random.seed(100)
    for i in range(8):
        pos[i] = pos[i] % 100

    shuffle_pos = random.sample(pos, k=8)

    trans_trans_bin = np.empty(8)

    for i in range(8):
        trans_trans_bin[shuffle_pos[i]] = list_bin[i]

    # steo3 : orginal bin to dec
    trans_trans_pix = 0

    for i in range(8):
        trans_trans_pix += trans_trans_bin[i] * (2**(pos[7-i]))

    trans_trans_pix = int(trans_trans_pix)

    return trans_trans_pix


def cal_coordinate(sou_img):    # calcuate the corrdinate of 9 512*512 picture

    # prepare
    h, w = sou_img.shape
    pixels = h

    this_img = []

    for i in range(h):
        list1 = []

        for j in range(w):
            list1.append([i, j])

        this_img.append(list1)

    new_img = []

    for i in range(h):
        list1 = []

        for j in range(w):
            list1.append([i, j])

        new_img.append(list1)

    # EAT function
    for j in range(h):
        for k in range(w):

            new_coordinate = [j, k]

            for i in range(G):

                new_coordinate = np.dot(M, new_coordinate)
                new_coordinate[0] = new_coordinate[0] % pixels
                new_coordinate[1] = new_coordinate[1] % pixels

            new_img[new_coordinate[0]][new_coordinate[1]] = this_img[j][k]

    for a in range(h):
        for b in range(w):
            this_img[a][b] = new_img[a][b]

    # the final coordinate after G times EAT function
    return this_img


def dec(sou_img, transfer):  # to create the encrypt imgage

    trans_img = []

    for j in range(512):
        list1 = []

        for k in range(512):

            list1.append(RRP(sou_img[transfer[j][k][0]][transfer[j][k][1]]))
            # print(i)
            # print(transfer[j][k][0])

        trans_img.append(list1)

    res_img = np.asarray(trans_img)

    return res_img


if __name__ == "__main__":

    # initial variables
    dir_sou = "source"
    dir_encryp = "encryp"
    dir_decryp = "decryp/"
    list = []
    list_name = []

    # read pic in encrpy file
    entries = os.listdir(dir_encryp)

    for entry in entries:

        img = cv2.imread(dir_encryp + "/" + entry, cv2.IMREAD_GRAYSCALE)

        # get image
        list.append(img)
        # get name
        list_name.append(entry.replace("_enc.png", ""))

    # calcuate the coordinate first
    transfer = cal_coordinate(list[0])

    # EAT dec
    for i in range(9):

        print(i)
        print(list_name[i])

        result_img = enc(list[i], transfer)

        # create enc img
        path_name = dir_decryp + list_name[i] + "_dec.png"
        cv2.imwrite(path_name, result_img)
