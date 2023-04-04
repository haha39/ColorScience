import cv2
import numpy as np
import os
import random

RATIO = 0.2


def lsbmr(secret_message):
    x = 9


if __name__ == "__main__":

    # initial variables
    dir_awc1 = "test"
    list = []

    # create secret message
    random.seed(1000)
    secret_message = bin(random.randint(0, 1000))
    print(secret_message)

    # read pic in test file
    entries = os.listdir(dir_awc1)

    for entry in entries:
        img_tar = cv2.imread(dir_awc1 + "/" + entry)
        print(entry)

        list.append(img_tar)

    # embedding message with LSBMR
    for i in range(9):
        print(i+1)
