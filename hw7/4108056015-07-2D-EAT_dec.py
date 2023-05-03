import numpy as np
import cv2
import os
import random

# argument setting
a = 1
b = 1

# number of round setting
G = 100

def rev_eat(img_length):

    x, y = np.meshgrid(range(img_length), range(img_length), indexing='ij')

    x_prime = ( x - a*y ) % img_length
    y_prime = ( (a*b+1)*y - b*x ) % img_length

    return x_prime, y_prime


def img_fit(img, img_name, img_length):

    decrypt_img = img
    x_prime, y_prime = rev_eat(img_length)

    for i in range(G):
        decrypt_img = decrypt_img[x_prime, y_prime]

    dir = "decryp"
    path_name = dir + "/" + img_name + "_dec.png"
    cv2.imwrite(path_name, decrypt_img)

if __name__ == "__main__":

    images = os.listdir('encryp')
    img = []

    # reading img
    for image in images:
        target = cv2.imread('encryp/' + image)
        img.append(target)

    # mapping
    for i in range(9):
        length = img[i].shape[0]
        img_fit(img[i], images[i].replace("_enc.png",""), length)
        print("%d complete"%(i+1))

