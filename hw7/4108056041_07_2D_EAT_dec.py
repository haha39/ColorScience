import cv2
import numpy as np
import os

a, b = 1, 1
M = np.array([[1, -a],
              [-b, a*b+1]])
G = 100


def cal_coordinate(sou_img):
    h, w, c = sou_img.shape
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

    for i in range(G):
        for j in range(h):
            for k in range(w):
                tmp_coordinate = [j, k]

                new_coordinate = np.dot(M, tmp_coordinate)
                new_coordinate[0] = new_coordinate[0] % pixels
                new_coordinate[1] = new_coordinate[1] % pixels

                new_img[new_coordinate[0]][new_coordinate[1]] = this_img[j][k]

    for a in range(2):
        for b in range(2):
            this_img[a][b] = new_img[a][b]

    return this_img


def enc(sou_img, transfer):
    res_img = sou_img

    for j in range(512):
        for k in range(512):
            res_img[j][k] = sou_img[transfer[j][k][0]][transfer[j][k][1]]

    return res_img


if __name__ == "__main__":

    # initial variables
    dir_sou = "source"
    dir_encryp = "encryp"
    dir_decryp = "decryp/"
    list = []
    list_name = []

    # read pic in test file
    entries = os.listdir(dir_encryp)

    for entry in entries:

        img = cv2.imread(dir_encryp + "/" + entry)

        list.append(img)
        list_name.append(entry.replace(".png", ""))

    transfer = cal_coordinate(list[0])

    # EAT enc
    for i in range(9):

        print(i)
        print(list_name[i])

        result_img = enc(list[i], transfer)

        # create enc img
        path_name = dir_decryp + list_name[i] + "_dec.png"
        cv2.imwrite(path_name, result_img)
