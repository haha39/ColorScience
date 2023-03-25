import cv2
import numpy as np
import os


def color_transfer(target, source, preserve_paper=True):

    # convert the images from the RGB to L*ab* color space, being
    # sure to utilizing the floating point data type (note: OpenCV
    # expects floats to be 32-bit, so use that instead of 64-bit)
    # source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    # target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    # convert source and target to "float32"
    source = source.astype("float32")
    target = target.astype("float32")

    # compute color statistics for the source and target images
    (bMeanSrc, bStdSrc, gMeanSrc, gStdSrc, rMeanSrc,
     rStdSrc) = np.round(image_stats(source), 2)
    (bMeanTar, bStdTar, gMeanTar, gStdTar, rMeanTar,
     rStdTar) = np.round(image_stats(target), 2)

    # wct
    w = 0.00
    (b, g, r) = cv2.split(target)

    for i in range(101):

        # weight
        w += 0.01 * i

        # subtract the means from the target image
        b -= bMeanSrc
        g -= gMeanSrc
        r -= rMeanSrc

        if preserve_paper:
            # scale by the standard deviations using paper proposed factor
            b = ((w * bStdTar + (1 - w) * bStdSrc) / bStdSrc) * b
            g = ((w * gStdTar + (1 - w) * gStdSrc) / gStdSrc) * g
            r = ((w * rStdTar + (1 - w) * rStdSrc) / rStdSrc) * r
        # else:
        #     # scale by the standard deviations using reciprocal of paper proposed factor
        #     b = (bStdSrc / bStdTar) * b
        #     g = (gStdSrc / gStdTar) * g
        #     r = (rStdSrc / rStdTar) * r

        # add in the source mean
        b += w * bMeanTar + (1 - w) * bMeanSrc
        g += w * gMeanTar + (1 - w) * gMeanSrc
        r += w * rMeanTar + (1 - w) * rMeanSrc

    # clip/scale the pixel intensities to [0, 255] if they fall
    # outside this range
    b = np.clip(b, 0, 255)
    g = np.clip(g, 0, 255)
    r = np.clip(r, 0, 255)

    # merge the channels together and convert back to the RGB color
    # space, being sure to utilize the 8-bit unsigned integer data
    # type
    transfer = cv2.merge([b, g, r])
    # transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

    # return the color transferred image
    return transfer


def image_stats(image):

    (b, g, r) = cv2.split(image)
    (bMean, bStd) = (b.mean(), b.std())
    (gMean, gStd) = (g.mean(), g.std())
    (rMean, rStd) = (r.mean(), r.std())

    return (bMean, bStd, gMean, gStd, rMean, rStd)


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

        # cv2.imwrite(path_name, img_res)
