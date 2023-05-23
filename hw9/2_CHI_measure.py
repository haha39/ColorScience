import cv2
import numpy as np
import os
import csv
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt


def chi(img_sou, img_enc):

    # build histgram
    hist_sou = cv2.calcHist(
        [img_sou], [0], None, [256], [0, 256])
    cv2.normalize(hist_sou, hist_sou, alpha=0,
                  beta=1, norm_type=cv2.NORM_MINMAX)

    # build histgram
    hist_enc = cv2.calcHist(
        [img_enc], [0], None, [256], [0, 256])
    cv2.normalize(hist_enc, hist_enc, alpha=0,
                  beta=1, norm_type=cv2.NORM_MINMAX)

    # img_sou1 = img_sou.ravel()
    # (hist_sou, a2, a3) = plt.hist(img_sou1, 256, [0, 256])

    # img_enc1 = img_enc.ravel()
    # (hist_enc, a2, a3) = plt.hist(img_enc1, 256, [0, 256])

    # haha = 0.0
    # ei = 512*512/256

    # for i in range(256):

    #     tmp = hist_enc[i] - ei
    #     tmp = tmp ** 2
    #     tmp = tmp / ei
    #     haha += tmp

    output = cv2.compareHist(
        hist_sou, hist_enc, cv2.HISTCMP_CHISQR)

    print(output)
    # print(haha)

    return 0


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

    dir_encryp = "encryp"
    list_encryp = []
    list_encryp_name = []

    # read pic in encryp file
    entries = os.listdir(dir_encryp)

    for entry in entries:

        img = cv2.imread(dir_encryp + "/" + entry, cv2.IMREAD_GRAYSCALE)

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

        chi(list_sou[i], list_encryp[i])

        # res_sou.append(chi(list_sou[i]))
        # res_enc.append(chi(list_encryp[i]))
'''
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
'''
