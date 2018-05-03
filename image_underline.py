import cv2
import pytesseract
import numpy as np
from PIL import Image
from adminfile import writefileappend
import os

def diffImage(image1, image2,path, miliseg):
    global idx
    # load two images
    diff1 = cv2.imread(image1)
    diff2 = cv2.imread(image2)

    # calculate the absolute difference of the two images
    diff_total = cv2.absdiff(diff1, diff2)

    # Search the countours
    imagen_gris = cv2.cvtColor(diff_total, cv2.COLOR_BGR2GRAY)
    _, contours, hierarchy = cv2.findContours(imagen_gris, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #create a mask
    mask = np.full((diff1.shape[0], diff1.shape[1]), 0, dtype=np.uint8)  # mask is only
    #mask.fill(255,)


    # look akmeach one of the contours and, if it is not noise, we draw its Bounding Box on the original image
    for c in contours:
        if cv2.contourArea(c) >= 200:
            posicion_x, posicion_y, ancho, alto = cv2.boundingRect(c)  # save the dimensions of the Bounding Box
            cv2.rectangle(mask, (posicion_x, posicion_y), (posicion_x + ancho, posicion_y + alto), (255,255,255),-1)  # Draw the bounding box
            # get first masked value (foreground)
            img = cv2.bitwise_and(diff1, diff1, mask=mask)
            cropped = img[posicion_y:posicion_y + alto, posicion_x:posicion_x + ancho]

            text = textImage(cropped)

            strData = miliseg + "," + image1 + "," + str(text)
            #processed_image_path = path + "processed_image.txt"
            processed_image_path = os.path.join(path, "processed_image.txt")

            writefileappend(processed_image_path, strData)
            cv2.imshow("l", cropped)
            cv2.waitKey(0)




    '''

    img = Image.fromarray(img)
    diffFile= path+ "diff"+ str(idx)+".png"
    img.save(diffFile)
    idx+=1

    white = allPixelWhite(img)
    whiteFile = path + "white" + str(idx) + ".png"
    img.save(whiteFile)
    text = textImage(white)

    strData = miliseg + "," + image1 + "," + text.strip('\n')
    processed_image_path = path + "processed_image.txt"

    writefileappend(processed_image_path, strData)
    strData = ""

    '''
    #return img


def processImage(img):
    #read
    img = cv2.imread('blanca.png')

    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)
    cv2.waitKey(0)


    # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
    #cv2.imshow("thresh", thresh)
    #cv2.waitKey(0)
    ret1, thresh1 = cv2.threshold(thresh, 180, 255, cv2.THRESH_BINARY)
    #cv2.imshow("th1", thresh1)
    #cv2.waitKey(0)
    thresh_color = cv2.cvtColor(thresh1, cv2.COLOR_GRAY2BGR)

    #cv2.imshow("thresh color", thresh_color)
    #cv2.waitKey(0)

    #vcr = cv2.subtract(255, thresh)
    # change reverse color
    finishImg = cv2.bitwise_not(thresh)
    #cv2.imshow("viceversa", finishImg)
    #cv2.waitKey(0)

    finishImg = Image.fromarray(finishImg)

    finishImg.save("blanca1.png")
    return finishImg


def textImage(img):
    result = pytesseract.image_to_string(img, lang ="eng+esp")
    print (result)
   #return (result)

