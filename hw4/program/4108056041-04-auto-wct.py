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
    (b, g, r) = cv2.split(source)

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


def hist_dist(source, target, i_th):
    # build histgram

    # h_bins = 50
    # s_bins = 60
    # histSize = [h_bins, s_bins]
    # # hue varies from 0 to 179, saturation from 0 to 255
    # h_ranges = [0, 180]
    # s_ranges = [0, 256]
    # ranges = h_ranges + s_ranges  # concat lists

    # Correlation distance
    color = ("blue", "green", "red")

    hist_com = (cv2.HISTCMP_CORREL, cv2.HISTCMP_CHISQR,
                cv2.HISTCMP_INTERSECT, cv2.HISTCMP_BHATTACHARYYA)

    fun_name = ["Correlation Distance", "Chi-Square Distance",
                "Intersection Distance", "Bhattacharyya Distance"]

    dir_name = ["COR", "CHS", "INS", "BHA"]

    list_best_wei = []

    for j, method in enumerate(hist_com):

        for i, col in enumerate(color):

            list_trans_sou = []
            list_trans_tar = []
            list_diff = []

            for weight in range(101):

                # build img_trans
                img_trans = color_transfer(source, target, weight)

                # build histgram
                hist_transfer = cv2.calcHist(
                    [img_trans], [i], None, [256], [0, 256])
                cv2.normalize(hist_transfer, hist_transfer, alpha=0,
                              beta=1, norm_type=cv2.NORM_MINMAX)

                hist_source = cv2.calcHist(
                    [source], [i], None, [256], [0, 256])
                cv2.normalize(hist_source, hist_source, alpha=0,
                              beta=1, norm_type=cv2.NORM_MINMAX)

                hist_target = cv2.calcHist(
                    [target], [i], None, [256], [0, 256])
                cv2.normalize(hist_target, hist_target, alpha=0,
                              beta=1, norm_type=cv2.NORM_MINMAX)

                # compare histgram
                trans_sou = cv2.compareHist(
                    hist_transfer, hist_source, method)
                trans_tar = cv2.compareHist(
                    hist_transfer, hist_target, method)
                # difference
                diff = abs(trans_sou - trans_tar)

                #append in list
                list_trans_sou.append(trans_sou)
                list_trans_tar.append(trans_tar)
                list_diff.append(diff)

            # write in excel file
            create_excel_csv(dir_name[j], fun_name[j], col, list_trans_sou,
                             list_trans_tar, list_diff, i_th)
            # find out the best weight
            list_best_wei.append(list_diff.index(min(list_diff)))

        # build wct img
        create_wctimg(source, target, dir_name[j], list_best_wei, i_th)


def create_excel_csv(dir_name, fun_name, color, trans_sou, trans_tar, diff, i_th):

    dir_dis = "distance-" + dir_name + "/"
    dir_path = dir_dis + "res-0" + str(i_th+1) + "-dist-" + color + ".csv"

    with open(dir_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([fun_name])
        writer.writerow(["NO", "Weight", "D(S, Iw)", "D(T, Iw)", "Difference"])

        for i in range(101):
            writer.writerow(
                [(i+1), (0.01*i), round(trans_sou[i], 6), round(trans_tar[i], 6), round(diff[i], 6)])


def create_wctimg(source, target, dir_name, list_best_wei, i_th):
    # convert source and target to "float32"
    source = source.astype("float32")
    target = target.astype("float32")

    # compute color statistics for the source and target images
    (bMeanSrc, bStdSrc, gMeanSrc, gStdSrc, rMeanSrc,
     rStdSrc) = np.round(image_stats(source), 2)
    (bMeanTar, bStdTar, gMeanTar, gStdTar, rMeanTar,
     rStdTar) = np.round(image_stats(target), 2)

    (b, g, r) = cv2.split(source)

    # weight
    w_blue = 0.00 + 0.01 * list_best_wei[0]
    w_green = 0.00 + 0.01 * list_best_wei[1]
    w_red = 0.00 + 0.01 * list_best_wei[2]

    # subtract the means from the target image
    b -= bMeanSrc
    g -= gMeanSrc
    r -= rMeanSrc

    # scale by the standard deviations using paper proposed factor
    b = ((w_blue * bStdTar + (1 - w_blue) * bStdSrc) / bStdSrc) * b
    g = ((w_green * gStdTar + (1 - w_green) * gStdSrc) / gStdSrc) * g
    r = ((w_red * rStdTar + (1 - w_red) * rStdSrc) / rStdSrc) * r

    # add in the source mean
    b += w_blue * bMeanTar + (1 - w_blue) * bMeanSrc
    g += w_green * gMeanTar + (1 - w_green) * gMeanSrc
    r += w_red * rMeanTar + (1 - w_red) * rMeanSrc

    # clip/scale the pixel intensities to [0, 255] if they fall
    # outside this range
    b = np.clip(b, 0, 255)
    g = np.clip(g, 0, 255)
    r = np.clip(r, 0, 255)

    # merge the channels together and convert back to the RGB color
    # space, being sure to utilize the 8-bit unsigned integer data
    # type
    wct_img = cv2.merge([b, g, r])
    wct_img = wct_img.astype("uint8")
    # transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

    # create wct img
    dir_awc = "awctresult-" + dir_name

    path_name = dir_awc + "/res-0" + str(i_th+1) + '-' + \
        str(w_blue) + '-' + str(w_green) + '-' + str(w_red) + ".png"
    cv2.imwrite(path_name, wct_img)


if __name__ == "__main__":
    dir_awc1 = "awctresult-COR"

    entries = os.listdir(dir_awc1)

    list = []

    for entry in entries:
        img_tar = cv2.imread(dir_awc1 + "/" + entry)
        print(entry)

        list.append(img_tar)

    for i in range(6):
        hist_dist(list[i], list[i+6], i)
        print(i+1)
