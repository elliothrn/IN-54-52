import cv2 as cv
import sys
import numpy as np
import imutils as imutils

class Train_ranks:
    """Structure to store information about train rank images."""

    def __init__(self):
        self.img = [] # Thresholded, sized rank image loaded from hard drive
        self.name = "Placeholder"

class Train_suits:
    """Structure to store information about train suit images."""

    def __init__(self):
        self.img = [] # Thresholded, sized suit image loaded from hard drive
        self.name = "Placeholder"

def load_ranks(filepath):
    """Loads rank images from directory specified by filepath. Stores
    them in a list of Train_ranks objects."""

    train_ranks = []
    i = 0

    for Rank in ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
                 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']:
        train_ranks.append(Train_ranks())
        train_ranks[i].name = Rank
        filename = Rank + '.jpg'
        train_ranks[i].img = cv.imread(filepath + filename, cv.IMREAD_GRAYSCALE)
        i = i + 1

    return train_ranks


def load_suits(filepath):
    """Loads suit images from directory specified by filepath. Stores
    them in a list of Train_suits objects."""

    train_suits = []
    i = 0

    for Suit in ['Spades', 'Diamonds', 'Clubs', 'Hearts']:
        train_suits.append(Train_suits())
        train_suits[i].name = Suit
        filename = Suit + '.jpg'
        train_suits[i].img = cv.imread(filepath + filename, cv.IMREAD_GRAYSCALE)
        i = i + 1

    return train_suits
def crop(c):
    cropped = [c[20:110, 0:70], c[110:180, 0:70]]
    return cropped

def reco_num(c,i):
    numeros=load_ranks('Card_Imgs/')
    gray = cv.cvtColor(c, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    bin, in_bin = cv.threshold(blurred, 128, 255, cv.THRESH_BINARY_INV)
    c=in_bin
    c= cv.resize(c,(70,125))
    i=str(i)
    cv.imwrite('Resize'+i+'.jpg',c)
    best_rank_match_diff = 1000000
    # Difference the query card rank image from each of the train rank images,
    # and store the result with the least difference
    for Trank in numeros:
        img=Trank.img
        diff_img = cv.absdiff(c,img)

        rank_diff = int(np.sum(diff_img) / 255)

        if rank_diff < best_rank_match_diff:
            best_rank_diff_img = diff_img
            best_rank_match_diff = rank_diff
            best_rank_name = Trank.name
    return best_rank_name

def reco_sym(c,i):
    symbols=load_suits('Card_Imgs/')
    gray = cv.cvtColor(c, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    bin, in_bin = cv.threshold(blurred, 128, 255, cv.THRESH_BINARY_INV)
    c=in_bin
    c=cv.resize(c,(70,100))
    i = str(i)
    cv.imwrite('ResizeSym' + i + '.jpg', c)
    best_suit_match_diff=1000000
    # Difference the query card rank image from each of the train rank images,
    # and store the result with the least difference
    for Tsuit in symbols:
        img=Tsuit.img
        diff_img = cv.absdiff(c,img)
        suit_diff = int(np.sum(diff_img) / 255)

        if suit_diff < best_suit_match_diff:
            best_suit_diff_img = diff_img
            best_suit_match_diff = suit_diff
            best_suit_name = Tsuit.name
    return best_suit_name
