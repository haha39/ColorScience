import cv2
import numpy as np
import os
import csv
import math

# from scipy.stats import chi2_contingency
# import matplotlib.pyplot as plt


def cor(img):

    size = 512*512

    list1 = list(range(0, size))

    list_choice = np.random.choice(a=list1, size=8000, replace=False)

    # find four coorelation : x, y_hor, y_ver, y_dia
    xi = []
    y_hor = []
    y_ver = []
    y_dia = []

    for i in range(8000):

        x = math.floor(list_choice[0] / 512)
        y = list_choice[i] % 512

        xi.append(img[x][y])

        # y horizontal
        if y != 511:
            y_hor.append(img[x][y+1])
        else:
            y_hor.append(img[x][y-1])
        # y vertical
        if x != 511:
            y_ver.append(img[x+1][y])
        else:
            y_ver.append(img[x-1][y])
        # y diagonal
        if x != 511 and y != 511:
            y_dia.append(img[x+1][y+1])
        else:
            y_dia.append(img[x-1][y-1])

    # calculate pearson's coefficients

    # step 1
    x_mean = np.mean(xi)
    y_hor_mean = np.mean(y_hor)
    y_ver_mean = np.mean(y_ver)
    y_dia_mean = np.mean(y_dia)

    cov_hor, cov_ver, cov_dia = 0.0, 0.0, 0.0
    var_x_hor, var_x_ver, var_x_dia = 0.0, 0.0, 0.0
    var_y_hor, var_y_ver, var_y_dia = 0.0, 0.0, 0.0

    for i in range(8000):

        # horizontal
        cov_hor += (xi[i] - x_mean)*(y_hor[i] - y_hor_mean)
        var_x_hor += ((xi[i] - x_mean) ** 2)
        var_y_hor += ((y_hor[i] - y_hor_mean) ** 2)

        # vertical
        cov_ver += (xi[i] - x_mean)*(y_ver[i] - y_ver_mean)
        var_x_ver += ((xi[i] - x_mean) ** 2)
        var_y_ver += ((y_ver[i] - y_ver_mean) ** 2)

        # diagonal
        cov_dia += (xi[i] - x_mean)*(y_dia[i] - y_dia_mean)
        var_x_dia += ((xi[i] - x_mean) ** 2)
        var_y_dia += ((y_dia[i] - y_dia_mean) ** 2)

    # step 2
    r_hor = cov_hor / ((math.sqrt(var_x_hor))*(math.sqrt(var_y_hor)))
    r_ver = cov_ver / ((math.sqrt(var_x_ver))*(math.sqrt(var_y_ver)))
    r_dia = cov_dia / ((math.sqrt(var_x_dia))*(math.sqrt(var_y_dia)))

    return (r_hor, r_ver, r_dia)


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
    res_sou = []
    res_enc = []

    for i in range(9):

        print(i)
        print(list_sou_name[i])
        print(list_enc_name[i])

        res_sou.append(cor(list_sou[i]))
        res_enc.append(cor(list_enc[i]))

    # create csv file
    path = "statis/COR_res.csv"

    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["COR", "", "Plain", "", "", "",
                        "", "", "", "", "", "Cipher"])
        writer.writerow(["Sample", "8000", "Red", "", "", "Green", "", "",
                        "Blue", "", "",  "Red", "", "", "Green", "", "", "Blue", "", ""])
        writer.writerow(["Image", "Type", "horizontal", "vertical", "diagonal", "horizontal", "vertical", "diagonal", "horizontal", "vertical",
                        "diagonal", "horizontal", "vertical", "diagonal", "horizontal", "vertical", "diagonal", "horizontal", "vertical", "diagonal"])

        for i in range(9):
            writer.writerow(
                [list_sou_name[i], "gray", res_sou[i][0], res_sou[i][1], res_sou[i][2], "", "", "",
                 "", "", "", res_enc[i][0], res_enc[i][1], res_enc[i][2]])
