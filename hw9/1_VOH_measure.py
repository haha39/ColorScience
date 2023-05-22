import cv2
import numpy as np
import os
import csv


def voh(img):

    var_RBG = np.array([0.0, 0.0, 0.0])
    seq = [2, 1, 0]  # for sequence R G B

    for color in seq:

        # build histgram
        hist_img = cv2.calcHist(
            [img], [color], None, [256], [0, 256])
        cv2.normalize(hist_img, hist_img, alpha=0,
                      beta=1, norm_type=cv2.NORM_MINMAX)

        # calculate the var of histogram
        var = 0.0

        for i in range(256):
            for j in range(256):
                var += ((hist_img[i] - hist_img[j]) ** 2) / 2

        var = var / 256
        var = var / 256

        var_RBG[color] = var

    print(var_RBG)
    return var_RBG


def create_csv(result_sou, result_enc, sou_name):

    # dir_dis = "distance-" + dir_name + "/"
    path = "statis/VOH_res.csv"

    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["VOH", "", "Plain", "", "", "Cipher"])
        writer.writerow(["Image", "Type", "Red", "Green",
                        "Blue", "Red", "Green", "Blue"])

        writer.writerow(
            [sou_name, "color", result_sou[0], result_sou[1], result_sou[2],
             result_enc[0], result_enc[1], result_enc[2]])


if __name__ == "__main__":

    # read pic in source file
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

    # read pic in encryp file
    entries = os.listdir(dir_encryp)

    for entry in entries:

        img = cv2.imread(dir_encryp + "/" + entry)

        # get image
        list_encryp.append(img)
        # get name
        list_encryp_name.append(entry.replace(".png", ""))

    # calculate variance of histogram
    res_sou = []
    res_enc = []

    for i in range(9):

        print(i)
        print(list_sou_name[i])
        print(list_encryp_name[i])

        res_sou.append(voh(list_sou[i]))
        res_enc.append(voh(list_encryp[i]))

    # create enc img
    path = "statis/VOH_res.csv"

    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["VOH", "", "Plain", "", "", "Cipher"])
        writer.writerow(["Image", "Type", "Red", "Green",
                        "Blue", "Red", "Green", "Blue"])

        for i in range(9):
            writer.writerow(
                [list_sou_name[i], "color", res_sou[i][0], res_sou[i][1], res_sou[i][2],
                 res_enc[i][0], res_enc[i][1], res_enc[i][2]])
