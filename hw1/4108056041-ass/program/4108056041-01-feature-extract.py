import cv2
import numpy as np
import os
import csv

# target
entries = os.listdir('../target')
for entry in entries:
    img_tar = cv2.imread("../target/" + entry)
    list_tar = []
    for i in range(2, -1, -1):
        list_tar.append(round(img_tar[:, :, i].flatten().mean(), 2))
        list_tar.append(round(img_tar[:, :, i].flatten().std(), 2))

    #print(entry.replace(".png", ""))
    new_entry = entry.replace(".png", "")

    with open("../feature/"+new_entry+"_dec.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list_tar)

    # print(list_tar)

# source
entries = os.listdir('../source')
for entry in entries:
    img_sour = cv2.imread("../source/" + entry)
    list_sour = []
    for i in range(2, -1, -1):
        list_sour.append(round(img_sour[:, :, i].flatten().mean(), 2))
        list_sour.append(round(img_sour[:, :, i].flatten().std(), 2))

    #print(entry.replace(".png", ""))
    new_entry = entry.replace(".png", "")

    with open("../feature/"+new_entry+"_dec.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list_sour)

    # print(list_sour)
