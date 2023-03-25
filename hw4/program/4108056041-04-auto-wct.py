import cv2
import numpy as np
import os


def color_transfer(target, source, preserve_paper=True):

    # convert the images from the RGB to L*ab* color space, being
    # sure to utilizing the floating point data type (note: OpenCV
    # expects floats to be 32-bit, so use that instead of 64-bit)
    #source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    #target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    # convert source and target to "float32"
    source = source.astype("float32")
    target = target.astype("float32")

    # compute color statistics for the source and target images
    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc,
     bStdSrc) = np.round(image_stats(source), 2)
    (lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar,
     bStdTar) = np.round(image_stats(target), 2)

    # subtract the means from the target image
    (l, a, b) = cv2.split(target)
    l -= lMeanTar
    a -= aMeanTar
    b -= bMeanTar

    if preserve_paper:
        # scale by the standard deviations using paper proposed factor
        l = (lStdTar / lStdSrc) * l
        a = (aStdTar / aStdSrc) * a
        b = (bStdTar / bStdSrc) * b
    else:
        # scale by the standard deviations using reciprocal of paper proposed factor
        l = (lStdSrc / lStdTar) * l
        a = (aStdSrc / aStdTar) * a
        b = (bStdSrc / bStdTar) * b

    # add in the source mean
    l += lMeanSrc
    a += aMeanSrc
    b += bMeanSrc

    # clip/scale the pixel intensities to [0, 255] if they fall
    # outside this range
    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)

    # merge the channels together and convert back to the RGB color
    # space, being sure to utilize the 8-bit unsigned integer data
    # type
    transfer = cv2.merge([l, a, b])
    #transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

    # return the color transferred image
    return transfer


def image_stats(image):

    (l, a, b) = cv2.split(image)
    (lMean, lStd) = (l.mean(), l.std())
    (aMean, aStd) = (a.mean(), a.std())
    (bMean, bStd) = (b.mean(), b.std())

    return (lMean, lStd, aMean, aStd, bMean, bStd)


if __name__ == "__main__":
    dir_awc1 = "awctresult-XXX"
    dir_dis1 = "distance-XXX"

    entries = os.listdir(dir_awc1)

    list = []

    for entry in entries:
        img_tar = cv2.imread(dir_awc1 + "/" + entry)

        list.append(img_tar)

    for i in range(6):
        img_res = color_transfer(list[i], list[i+6])

        path_name = dir_awc1 + "/res-0" + str(i+1) + ".png"

        cv2.imwrite(path_name, img_res)
