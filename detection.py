import cv2 as cv
import ShapeDetector
import sys
import numpy as np

import imutils as imutils

import formes
import detect_coins
#import reconnaissance
from formes import crop

def detect(c, perimax):
    # initialize the shape name and approximate the contour
    shape = ""
    peri = cv.arcLength(c, True)
    if peri >= 0.5 * perimax:
        approx = cv.approxPolyDP(c, 0.04 * peri, True)

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        if len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv.boundingRect(approx)
            ar = w / float(h)

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "diamonds" if ar >= 0.95 and ar <= 1.05 else "carte"

            # return the name of the shape
    return shape


im = cv.imread(cv.samples.findFile("CartesTest.jpg"))

imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
contour_cartes = []
perimax = 0
i = 0
for c in contours:
    peri = cv.arcLength(c, True)
    if peri > perimax:
        perimax = peri
for c in contours:
    M = cv.moments(c)
    cX = int((M["m10"] / (M["m00"] + 1)))
    cY = int((M["m01"] / (M["m00"] + 1)))
    peri = cv.arcLength(c, True)
    if peri >= 0.6 * perimax:
        contour_cartes.append(c)

    shape = detect(c, perimax)

   # cv.putText(im, shape, (cX, cY), cv.FONT_HERSHEY_SIMPLEX,
    #           1, (0, 0, 255), 3)
    i += 1
#reconnaissance.reco(im, contour_cartes)
#cv.drawContours(im, contour_cartes, -1, (0, 255, 0), 3)
n = str(len(contour_cartes))

pts_dst = np.array([[0,1000],[500,0],[0,0],[500,1000]])
j =0
cartes=[]
for c in contour_cartes:
    t=str(j)
    coins = detect_coins.trouver_coins(c)
    intcoins = np.int0(coins)
    for i in intcoins:
        x, y = i.ravel()
       # cv.circle(im, (x, y), 10, 255, -1)
    h, status = cv.findHomography(np.float32(coins),pts_dst)
  #  tsf = cv.getPerspectiveTransform(coins,)
    im_dst = cv.warpPerspective(im,h,(500,1000))
    nomcarte='Carte'+t+'.jpg'
    cv.imwrite(nomcarte,im_dst)
    cartes.append(cv.imread(nomcarte))
    j+=1
i=0
numeros=[]
symbols=[]
for c in cartes:
    num=crop(c)[0]

    sym=crop(c)[1]
    numeros.append(formes.reco_num(num,i))
    symbols.append(formes.reco_sym(sym,i))
    print(numeros[i]+' of ' + symbols[i])
    i+=1
n = str(len(contour_cartes))
i=0
for c in contour_cartes:
    shape = (numeros[i]+' of ' + symbols[i])
    M = cv.moments(c)
    cX = int((M["m10"] / (M["m00"] + 1)))
    cY = int((M["m01"] / (M["m00"] + 1)))
    cv.putText(im, shape, (cX-150, cY), cv.FONT_HERSHEY_SIMPLEX,
               1, (200, 80, 0), 3)
    i+=1
cv.putText(im, 'Number of cards :' + n, (100, 100), cv.FONT_HERSHEY_SIMPLEX, 3, (200, 80, 0), 3)
cv.imwrite('Succes.jpg', im)
# cv.imshow("Image", im)
