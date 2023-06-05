import numpy as np
import cv2 
import os
import random

def lsb(pixel):
    return pixel % 2

def slsb(pixel):
    # return second last significant bit
    return (pixel >> 1) % 2

def mesg_embedding(cover, img_name):

    # initializing
    stego_u, stego_v, stego_w = cover, cover, cover
    overflow, underflow = 0, 0

    # reading img info
    height = cover.shape[0]
    width = cover.shape[1]

    # creating secret mesg
    secret_bits = [random.randint(0,1) for _ in range(3)]

    print(secret_bits)

    # embedding
    for i in range(height):
        for j in range(width):

            v12 = slsb(stego_u[i][j]) ^ lsb(stego_u[i][j]) ^ lsb(stego_v[i][j])
            v23 = slsb(stego_v[i][j]) ^ lsb(stego_v[i][j]) ^ lsb(stego_w[i][j])
            v31 = slsb(stego_w[i][j]) ^ lsb(stego_w[i][j]) ^ lsb(stego_u[i][j])

            #   if v12 == secret_bits[0] and v23 == secret_bits[1] and v31 == secret_bits[2]:
            #       no change
            if v12 != secret_bits[0] and v23 == secret_bits[1] and v31 == secret_bits[2]:
                if lsb(stego_v[i][j]) == 0:
                    if stego_v[i][j] == 0:
                        underflow += 1
                    stego_v[i][j] -= 1
                else:
                    if stego_v[i][j] == 255:
                        overflow += 1
                    stego_v[i][j] += 1
            elif v12 == secret_bits[0] and v23 != secret_bits[1] and v31 == secret_bits[2]:
                if lsb(stego_w[i][j]) == 0:
                    if stego_w[i][j] == 0:
                        underflow += 1
                    stego_w[i][j] -= 1
                else:
                    if stego_w[i][j] == 255:
                        overflow += 1
                    stego_w[i][j] += 1
            elif v12 == secret_bits[0] and v23 == secret_bits[1] and v31 != secret_bits[2]:
                if lsb(stego_u[i][j]) == 0:
                    if stego_u[i][j] == 0:
                        underflow += 1
                    stego_u[i][j] -= 1
                else:
                    if stego_u[i][j] == 255:
                        overflow += 1
                    stego_u[i][j] += 1
            elif v12 != secret_bits[0] and v23 != secret_bits[1] and v31 == secret_bits[2]:
                if lsb(stego_v[i][j]) == 0:
                    if stego_v[i][j] == 255:
                        overflow += 1
                    stego_v[i][j] += 1
                else:
                    if stego_v[i][j] == 0:
                        underflow += 1
                    stego_v[i][j] -= 1
            elif v12 == secret_bits[0] and v23 != secret_bits[1] and v31 != secret_bits[2]:
                if lsb(stego_w[i][j]) == 0:
                    if stego_w[i][j] == 255:
                        overflow += 1
                    stego_w[i][j] += 1
                else:
                    if stego_w[i][j] == 0:
                        underflow += 1
                    stego_w[i][j] -= 1
            elif v12 != secret_bits[0] and v23 == secret_bits[1] and v31 != secret_bits[2]:
                if lsb(stego_u[i][j]) == 0:
                    if stego_u[i][j] == 255:
                        overflow += 1
                    stego_u[i][j] += 1
                else:
                    if stego_u[i][j] == 0:
                        underflow += 1
                    stego_u[i][j] -= 1
            elif v12 != secret_bits[0] and v23 != secret_bits[1] and v31 != secret_bits[2]:
                if lsb(stego_w[i][j]) == 0:
                    if stego_w[i][j] == 0:
                        underflow += 1
                    stego_w[i][j] -= 1
                else:
                    if stego_w[i][j] == 255:
                        overflow += 1
                    stego_w[i][j] += 1
                    
                if lsb(stego_u[i][j]) == 0:
                    if stego_u[i][j] == 255:
                        overflow += 1
                    stego_u[i][j] += 1
                else:
                    if stego_u[i][j] == 0:
                        underflow += 1
                    stego_u[i][j] -= 1    

    # mesg extracting & checking
    extract_bits = [1 for _ in range(3)]

    extract_bits[0] = slsb(stego_u[100][100]) ^ lsb(stego_u[100][100]) ^ lsb(stego_v[100][100])
    extract_bits[1] = slsb(stego_v[100][100]) ^ lsb(stego_v[100][100]) ^ lsb(stego_w[100][100])
    extract_bits[2] = slsb(stego_w[100][100]) ^ lsb(stego_w[100][100]) ^ lsb(stego_u[100][100])

    print(extract_bits)

    # overflow & underflow checking
    print(overflow, underflow)

    # creating stego img
    # dir = "stego"
    # path_name = dir + "/" + img_name + "_stego_u" + ".png"
    # cv2.imwrite(path_name, stego_u)
    # path_name = dir + "/" + img_name + "_stego_v" + ".png"
    # cv2.imwrite(path_name, stego_v)
    # path_name = dir + "/" + img_name + "_stego_w" + ".png"
    # cv2.imwrite(path_name, stego_w)

if __name__ == "__main__":

    random.seed(100)

    images = os.listdir('cover')
    img = []

    for image in images:
        target = cv2.imread('cover/' + image, cv2.IMREAD_GRAYSCALE)
        img.append(target)

    for i in range(9):
        mesg_embedding(img[i], images[i].replace(".png",""))
        print("%d complete"%(i+1))
