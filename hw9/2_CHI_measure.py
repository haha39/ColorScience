import cv2
import numpy as np
import os
import csv
from scipy.stats import chi2_contingency


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

    output = cv2.compareHist(
        hist_sou, hist_enc, cv2.HISTCMP_CHISQR)

    # print(output)

    return output


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

    # calculate chi-square test of histogram
    result = []

    for i in range(9):

        print(i)
        print(list_sou_name[i])
        print(list_enc_name[i])

        result.append(chi(list_sou[i], list_enc[i]))

    # create csv file
    path = "statis/CHI_res.csv"

    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["CHI", "", "Plain", "", "", "", "", "Cipher"])
        writer.writerow(["Image", "Type", "Red", "Green",
                        "Blue", "alpha", "chi value", "Red", "Green", "Blue"])

        for i in range(9):
            writer.writerow(
                [list_sou_name[i], "gray", "", "", "",
                 "0.05", "293.248", result[i]])
