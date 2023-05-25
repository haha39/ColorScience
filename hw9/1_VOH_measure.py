import cv2
import numpy as np
import os
import csv


def voh(img):

    # build histgram
    hist_img = cv2.calcHist(
        [img], [0], None, [256], [0, 256])

    # calculate the var of histogram
    var = 0.0

    for i in range(256):
        for j in range(256):
            var += ((hist_img[i][0] - hist_img[j][0]) ** 2) / 2

    var = var / 256
    var = var / 256

    # print(var)
    # print(np.var(hist_img))

    return var


if __name__ == "__main__":

    # read pic in source file
    dir_sou = "source"
    list_sou = []
    list_sou_name = []

    # read pic in source file
    entries = os.listdir(dir_sou)

    for entry in entries:

        img = cv2.imread(dir_sou + "/" + entry, cv2.IMREAD_GRAYSCALE)

        # get image
        list_sou.append(img)
        # get name
        list_sou_name.append(entry.replace(".png", ""))

    # read pic in encryp file
    dir_enc = "encryp"
    list_enc = []
    list_enc_name = []

    entries = os.listdir(dir_enc)

    for entry in entries:

        img = cv2.imread(dir_enc + "/" + entry, cv2.IMREAD_GRAYSCALE)

        # get image
        list_enc.append(img)
        # get name
        list_enc_name.append(entry.replace(".png", ""))

    # calculate variance of histogram
    res_sou = []
    res_enc = []

    for i in range(9):

        print(i)
        print(list_sou_name[i])
        print(list_enc_name[i])

        res_sou.append(voh(list_sou[i]))
        res_enc.append(voh(list_enc[i]))

    # create csv file
    path = "statis/VOH_res.csv"

    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["VOH", "", "Plain", "", "", "Cipher"])
        writer.writerow(["Image", "Type", "Red", "Green",
                        "Blue", "Red", "Green", "Blue"])

        for i in range(9):
            writer.writerow(
                [list_sou_name[i], "gray", res_sou[i], "", "",
                 res_enc[i]])
