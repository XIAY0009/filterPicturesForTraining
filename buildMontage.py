###############################################################################
#Author      : Yingyu 
#Date        : 24th August 2020
#Description : Tool to filter out images based on different classes and stores
#              images into the respective files
###############################################################################

from imutils import build_montages
from imutils import paths
import argparse
import random
import cv2
import os 

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
args = vars(ap.parse_args())

maskClick = [] 
faceClick = [] 
discardClick = [] 
naClick = [] 
rectClick = []
imageClick = []
eachImageWidth = 0
eachImageHeight = 0
namedWindow = "Image"

def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global rectClick
	if event == cv2.EVENT_LBUTTONDOWN:
		rectClick.append((x, y))

def mask(): 
    global rectClick, maskClick
    maskClick.extend(rectClick)
    print ("maskClick: ", maskClick)
def face(): 
    global rectClick, faceClick
    faceClick.extend(rectClick)
    print ("faceClick: ", faceClick)
def discard(): 
    global rectClick, discardClick
    discardClick.extend(rectClick)
    print ("discardClick: ", discardClick)
def na(): 
    global rectClick, naClick
    naClick.extend(rectClick)
    print ("naClick: ", naClick)

def switcherRectToType(argument):
    switcher = { 
            "mask":mask,
            "face":face, 
            "discard":discard, 
            "na":na
    }
    func = switcher.get(argument, lambda: "Invalid classification")
    func()

def createList(startIndex, endIndex): 
    return [item for item in range(startIndex, endIndex)]

def writeToFile(fileName, allImages, imageCounter, imageHop, eachImageWidth, eachImageHeight, displayColumn, displayRow, flag):
    if flag == 0: 
        file = open(fileName, "a+")
        for eachMask in maskClick:
            x = eachMask[0]//eachImageWidth
            y = eachMask[1]//eachImageHeight
            #Computes the position in the grid
            position = y * displayColumn + x
            print ("grid position: ", position)
            position += imageCounter * imageHop
            print ("total grid position: ", position)
            #Finds the right image 
            storeImage = allImages[position]
            print("image to be stored: ", storeImage)
            file.write("%s\n" % storeImage)
        file.close()
    elif flag == 1: 
        file = open(fileName, "a+")
        for eachFace in faceClick:
            x = eachFace[0]//eachImageWidth
            y = eachFace[1]//eachImageHeight
            #Computes the position in the grid
            position = y * displayColumn + x
            print ("grid position: ", position)
            position += imageCounter * imageHop
            print ("total grid position: ", position)
            #Finds the right image 
            storeImage = allImages[position]
            print("image to be stored: ", storeImage)
            file.write("%s\n" % storeImage)
        file.close()
    elif flag == 2: 
        file = open(fileName, "a+")
        for eachNa in naClick:
            x = eachNa[0]//eachImageWidth
            y = eachNa[1]//eachImageHeight
            #Computes the position in the grid
            position = y * displayColumn + x
            print ("grid position: ", position)
            position += imageCounter * imageHop
            print ("total grid position: ", position)
            #Finds the right image 
            storeImage = allImages[position]
            print("image to be stored: ", storeImage)
            file.write("%s\n" % storeImage)
        file.close()
    elif flag == 3: 
        file = open(fileName, "a+")
        for eachDiscard in discardClick:
            x = eachDiscard[0]//eachImageWidth
            y = eachDiscard[1]//eachImageHeight
            #Computes the position in the grid
            position = y * displayColumn + x
            print ("grid position: ", position)
            position += imageCounter * imageHop
            print ("total grid position: ", position)
            #Finds the right image 
            storeImage = allImages[position]
            print("image to be stored: ", storeImage)
            file.write("%s\n" % storeImage)
        file.close()
    elif flag == 4: 
        file = open(fileName, "a+")
        #Finds out all the index that should be stored in this photo 
        startSave = imageCounter * imageHop
        endSave = (imageCounter+1)*imageHop
        if (endSave > len(allImages)): 
            endSave = len(allImages)
        print ("imageHop: ", imageHop)
        allIndexForImage = createList(startSave, endSave)
        print ("allIndexForImage: ", allIndexForImage)
        for noSave in imageClick:
            x = noSave[0]//eachImageWidth
            y = noSave[1]//eachImageHeight
            #Computes the position in the grid
            position = y * displayColumn + x
            print ("grid position: ", position)
            position += imageCounter * imageHop
            print ("total grid position: ", position)
            allIndexForImage.remove(position)
        for eachSave in allIndexForImage: 
            #Finds the right image 
            storeImage = allImages[eachSave]
            print("image to be stored for the default: ", storeImage)
            file.write("%s\n" % storeImage)
        file.close()


def saveFiles(allImages, imageCounter, imageHop, eachImageWidth, eachImageHeight, displayColumn, displayRow):
    global maskClick, faceClick, discardClick, naClick
    writeToFile("maskFile.txt", allImages, imageCounter, imageHop, eachImageWidth, eachImageHeight, displayColumn, displayRow, 0)
    writeToFile("faceFile.txt", allImages, imageCounter, imageHop, eachImageWidth, eachImageHeight, displayColumn, displayRow, 1)
    writeToFile("naFile.txt", allImages, imageCounter, imageHop, eachImageWidth, eachImageHeight, displayColumn, displayRow, 2)
    writeToFile("discardFile.txt", allImages, imageCounter, imageHop, eachImageWidth, eachImageHeight, displayColumn, displayRow, 3)
    #300820 Assuming that maskFile.txt is the default file to save images in 
    writeToFile("maskFile.txt", allImages, imageCounter, imageHop, eachImageWidth, eachImageHeight, displayColumn, displayRow, 4)

def drawOut(typeObject): 
    global rectClick, imageClick
    switcherRectToType(typeObject)
    imageClick.extend(rectClick)
    for eachPair in rectClick: 
       x = eachPair[0]
       y = eachPair[1]
       startingPointX = x//eachImageWidth * eachImageWidth + int(eachImageWidth/2)
       startingPointY = y//eachImageHeight * eachImageHeight + int(eachImageHeight/2)
       cv2.putText(montage,typeObject, (startingPointX, startingPointY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
       cv2.circle(montage, (startingPointX, startingPointY), 10, (0,0,255), -1)
       cv2.imshow("image", montage)
       rectClick = []

imagePaths = list(paths.list_images(args["images"]))
#check the number of images in the directory 
print ("# of files: ", len(imagePaths))

displayColumn = input("number of pictures to be display per row?")
displayRow = input ("number of rows of pictures?")
namedWindow = "Click f for face, click m for mask, click d for discard, click e for exception, click n for next"


images = []
# loop over the list of image paths
cv2.namedWindow(namedWindow)
cv2.setMouseCallback(namedWindow, click_and_crop)
for imagePath in imagePaths:
	# load the image and update the list of images
	image = cv2.imread(imagePath)
	images.append(image)

# construct the montages for the images
montages = build_montages(images, (128, 196), (displayColumn, displayRow))
eachImageWidth = 128
eachImageHeight = 196
imageCounter = -1
imageHop = displayColumn * displayRow

for montage in montages:
	rectClick = []
        maskClick = []
        faceClick = [] 
        naClick = [] 
        discardClick = []
        imageClick = []
        cv2.imshow(namedWindow, montage)
        imageCounter += 1
        while True: 
	    key = cv2.waitKey(0)
            if key == ord("f"):
                drawOut("face")
            elif key == ord("m"):
                drawOut("mask")
            elif key == ord("n"): 
                drawOut("na")
            elif key == ord("d"): 
                drawOut("discard")               
            
            elif key == 32: 
                saveFiles(imagePaths, imageCounter, imageHop, eachImageWidth, eachImageHeight, displayColumn, displayRow);
                break
