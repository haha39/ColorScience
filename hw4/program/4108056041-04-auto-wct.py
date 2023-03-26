import cv2
import numpy as np
import os
import csv


def color_transfer(source, target, diff, preserve_paper=True):

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

    # weight
    w += 0.01 * diff

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
    transfer = transfer.astype("uint8")
    # transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

    # return the color transferred image
    return transfer


def image_stats(image):

    (b, g, r) = cv2.split(image)
    (bMean, bStd) = (b.mean(), b.std())
    (gMean, gStd) = (g.mean(), g.std())
    (rMean, rStd) = (r.mean(), r.std())

    return (bMean, bStd, gMean, gStd, rMean, rStd)


def hist_dist(source, target, i):
    # build histgram
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    # hue varies from 0 to 179, saturation from 0 to 255
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges  # concat lists
    # Use the 0-th and 1-st channels
    # channels = [0, 1, 2]

    list_haha
    color = ('blue', 'green', 'red')
    # Correlation distance
    for i, col in enumerate(color):
        for weight in range(101):
            # build img_trans
            img_trans = color_transfer(source, target, weight)

            hist_transfer = cv2.calcHist(
                [img_trans], [i], None, histSize, ranges, accumulate=False)
            cv2.normalize(hist_transfer, hist_transfer, alpha=0,
                          beta=1, norm_type=cv2.NORM_MINMAX)

            hist_source = cv2.calcHist(
                [source], [i], None, histSize, ranges, accumulate=False)
            cv2.normalize(hist_source, hist_source, alpha=0,
                          beta=1, norm_type=cv2.NORM_MINMAX)

            hist_target = cv2.calcHist(
                [target], [i], None, histSize, ranges, accumulate=False)
            cv2.normalize(hist_target, hist_target, alpha=0,
                          beta=1, norm_type=cv2.NORM_MINMAX)

            trans_sou = cv2.compareHist(
                hist_transfer, hist_source, cv2.HISTCMP_CORREL)
            trans_tar = cv2.compareHist(
                hist_transfer, hist_target, cv2.HISTCMP_CORREL)
            diff = abs(trans_sou - trans_tar)

            # write in excel file
            ###########################################################excel_W("Correlation Distance", col, weight, trans_sou, trans_tar, diff, i)


def excel_W(fun_name, color, weight, trans_sou, trans_tar, diff, i):
    dir_dis1 = "distance-XXX/"
    dir_path = dir_dis1 + "res-0" + i + "-" + color + ".csv"

    with open(dir_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fun_name)
        writer.writerow(["NO", "Weight", "D(S, Iw)", "D(T, Iw)", "Difference"])


if __name__ == "__main__":
    dir_awc1 = "awctresult-XXX"
    dir_dis1 = "distance-XXX/"

    entries = os.listdir(dir_awc1)

    list = []

    for entry in entries:
        img_tar = cv2.imread(dir_awc1 + "/" + entry)
        print(entry)

        list.append(img_tar)

    for i in range(6):
        a = 1
        # #color transfer
        # img_trans = color_transfer(list[i], list[i+6]dfdfdfdsdfdsfdsfdsfd)
        # #histgram difference
        # img_res = hist_dist(list[i], list[i+6], img_transsdfdsfdsfdsfdsfsdff)

        # path_name = dir_awc1 + "/res-0" + str(i+1) + ".png"

        # cv2.imwrite(path_name, img_res)
