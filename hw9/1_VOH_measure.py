import cv2
import numpy as np
import os


def voh(img):

    var_BGR = []

    for color in range(3):

        # build histgram
        hist_img = cv2.calcHist(
            [img], [color], None, [256], [0, 256])
        cv2.normalize(hist_img, hist_img, alpha=0,
                      beta=1, norm_type=cv2.NORM_MINMAX)

        # calculate the var of histogram
        var = 0

        for i in range(256):
            for j in range(256):
                var = ((hist_img[i] - hist_img[j]) ** 2) / 2

        var = var / 256
        var = var / 256

        var_BGR.append(var)

    return var_BGR


if __name__ == "__main__":

    dir_sou = "source"
    list_sou = []
    list_sou_name = []

    # read pic in source file
    entries = os.listdir(dir_sou)

    for entry in entries:

        img = cv2.imread(dir_sou + "/" + entry)

        # get image
        list_sou.append(img)
        # get name
        list_sou_name.append(entry.replace(".png", ""))

    dir_encryp = "encryp"
    list_encryp = []
    list_encryp_name = []

    # read pic in source file
    entries = os.listdir(dir_encryp)

    for entry in entries:

        img = cv2.imread(dir_encryp + "/" + entry)

        # get image
        list_encryp.append(img)
        # get name
        list_encryp_name.append(entry.replace(".png", ""))

    # calculate variance of histogram
    for i in range(9):

        print(i)
        print(list_sou_name[i])
        print(list_encryp_name)

        result_sou = voh(list_sou[i])
        result_enc = voh(list_encryp[i])

        csv要的是rgb喔

        # # create enc img
        # path_name = dir_encryp + list_name[i] + "_enc.png"
        # cv2.imwrite(path_name, result_img)
