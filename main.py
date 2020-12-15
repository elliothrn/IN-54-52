
import cv2 as cv
import sys


import imutils as imu
import detection

img = cv.imread(cv.samples.findFile("CartesTest.jpg"))
resized = imutils.resize(img, width=300)
ratio = img.shape[0] #/ float(resized.shape[0])
if img is None:
    sys.exit("Could not read the image.")
#cv.imshow("Display window", img)
k = cv.waitKey(0)

#Pour binariser/seuiller l'image d'entrée
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
blurred = cv.GaussianBlur(gray,(5,5),0)
bin, in_bin = cv.threshold(blurred,128,255,cv.THRESH_BINARY)
picture = cv.imwrite('bin.jpg',in_bin)
#contours
contours, hierarchy = cv.findContours(in_bin.copy(),cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
#contours = imutils.grab_contours(contours)
cv.drawContours(img, contours,-1, (0,255,0), 3)

# show the output image
cv.imshow("Image", picture)
cv.waitKey(0)
#cv.imshow("Display window", picture)
#if k == ord("s"):
 #   cv.imwrite("starry_night.png", img)
