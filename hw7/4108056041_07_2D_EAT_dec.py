import cv2
import numpy as np
import os
import random
import math

# public variable
a, b = 1, 1
M = np.array([[1, -a],
              [-b, a*b+1]])
G = 100


def dec():
    a = 0


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

    print(M)

    # EAT enc
    for i in range(9):

        print(i)
        print(list_name[i])
        h, w, c = list[i].shape
        pixel = h * w
        print(pixel)
