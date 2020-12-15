import cv2 as cv
import numpy as np

def trouver_coins(contour):

    ymin = 10000
    xmin = 10000
    ymax = 0
    xmax = 0

    coins = [[0 for i in range(2)]] * 4


    for point in contour:

        #print(point[[0][0]])

        point_x=point[[0][0]][0]
        point_y=point[[0][0]][1]
        if point_x <= xmin:
            xmin = point_x
            coins[0] = [point_x, point_y]
        if point_x >xmax:
            xmax =point_x
            coins[1] = [point_x, point_y]
        if point_y <= ymin:
            ymin = point_y
            coins[2] = [point_x, point_y]
        if point_y >ymax:
            ymax = point_y
            coins[3] = [point_x, point_y]
    print(coins)
    return coins