import cv2
import numpy as np
import os
import random
import math

a, b = 1, 1
M = np.array([[1, a],
              [b, a*b+1]])
G = 100


def enc(sou_img):

    h, w, c = list[i].shape
    pixels = h * w
    print(pixels)

    transfer = []

    haha = [1, 1]
    hehe = np.dot(M, haha)
    hehe[0] = hehe[0] % pixels
    hehe[1] = hehe[1] % pixels

    print(hehe)

    # for i in range(G):
    #     for j in range(h):
    #         for k in range(w):
    #             x = 0

    transfer = transfer.reshape(h, w)


if __name__ == "__main__":

    # initial variables
    dir_sou = "source"
    dir_encryp = "encryp/"
    dir_decryp = "decryp/"
    list = []
    list_name = []

    # read pic in test file
    entries = os.listdir(dir_sou)

    for entry in entries:

        img = cv2.imread(dir_sou + "/" + entry)

        list.append(img)
        list_name.append(entry.replace(".png", ""))

    # EAT enc
    for i in range(9):

        print(i)
        print(list_name[i])
        h, w, c = list[i].shape
        #pixels = h * w
        # print(pixels)
        enc(list[i])

    print("\n")
    print(M)
