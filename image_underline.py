import cv2
import pytesseract
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from adminfile import writefileappend
import os
idCrop = 0


def diffImage(image1, image2,path, miliseg):
    global idCrop
    # load two images
    diff1 = cv2.imread(image1)
    diff2 = cv2.imread(image2)

    # calculate the absolute difference of the two images
    diff_total = cv2.absdiff(diff1, diff2)
    #cv2.imshow("diff", diff_total)
    #cv2.waitKey(0)

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
            r = cv2.rectangle(mask, (posicion_x, posicion_y), (posicion_x + ancho, posicion_y + alto), (255,255,255),-1)  # Draw the bounding box

            #cv2.imshow("rec_mask", r)
            #cv2.waitKey(0)
            # get first masked value (foreground)
            img = cv2.bitwise_and(diff1, diff1, mask=mask)

            #cv2.imshow("bitwise", img)
            #cv2.waitKey(0)
            cropped = img[posicion_y:posicion_y + alto, posicion_x:posicion_x + ancho]

            # PRUEBA DE TESSERACT
            #text = textImage(cropped)

            img = Image.fromarray(cropped)
            resize_crop = resize(img)
            text2 = textImage(resize_crop)

            cropName = "crop" + str(idCrop) + ".png"
            cropFile = os.path.join(path, cropName)
            img.save(cropFile)
            idCrop += 1

            strData = miliseg + "," + os.path.basename(image1) + "," + cropName + "," + text2.encode('utf-8') + "\n"
            #processed_image_path = path + "processed_image.txt"
            processed_log_path = os.path.join(path, "processed_image.txt")

            writefileappend(processed_log_path, strData)

            #cv2.imshow("l", cropped)
            #cv2.waitKey(0)


def resize(img):
    porcent = 2.0
    #img = Image.open(img)
    hpercent = int(float(porcent) * float(img.size[1]))
    wsize = int(float(img.size[0]) * float(porcent))
    #print(img.size[0],img.size[1])
    #print(wsize, hpercent)
    img = img.resize((wsize, hpercent), Image.ANTIALIAS)
    return img

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
    result = pytesseract.image_to_string(img, lang="eng+spa", boxes=False, config="--psm 3 --oem 2")
    print (result)
    return (result)

