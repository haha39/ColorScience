import cv2
import numpy as np
import os

if __name__ == "__main__":
    dir_awc1 = "test"

    entries = os.listdir(dir_awc1)

    list = []

    for entry in entries:
        img_tar = cv2.imread(dir_awc1 + "/" + entry)
        print(entry)

        list.append(img_tar)

    for i in range(9):
        print(i+1)
