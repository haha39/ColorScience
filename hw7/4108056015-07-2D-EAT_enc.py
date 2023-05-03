import numpy as np
import cv2
import os
import random

# argument setting
a = 1
b = 1

# number of round setting
G = 100

def eat(img_length):

    x, y = np.meshgrid(range(img_length), range(img_length), indexing='ij')

    x_prime = ( (a*b+1)*x + a*y ) % img_length
    y_prime = ( b*x + y ) % img_length

    return x_prime, y_prime


def img_fit(img, img_name, img_length):

    encrypt_img = img
    x_prime, y_prime = eat(img_length)

    for i in range(G):
        encrypt_img = encrypt_img[x_prime, y_prime]

    dir = "encryp"
    path_name = dir + "/" + img_name + "_enc.png"
    cv2.imwrite(path_name, encrypt_img)

if __name__ == "__main__":

    images = os.listdir('source')
    img = []

    # reading img
    for image in images:
        target = cv2.imread('source/' + image)
        img.append(target)

    # mapping
    for i in range(9):
        length = img[i].shape[0]
        img_fit(img[i], images[i].replace(".png",""), length)
        print("%d complete"%(i+1))

