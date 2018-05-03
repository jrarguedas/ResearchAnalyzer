# -*- coding: utf-8 -*-

from loginfo import LogInfo
import os
import subprocess
import pyautogui
from image_underline import diffImage
import cv2
import numpy as np
from adminfile import *
import checkErrorLog
import os

path = os.getcwd() + "/logs_to_treat"
logsList = os.listdir(path)

listLogInfo = []

# Function that checks if there are folders or not in the address logs_to_treat
# Check the logs of each folder with the scriptchecker script
# For each folder generates a loginfo instance and creates a list
def loadClickInfo():
    for logfolder in logsList:
        processed_image_path = os.path.join(path, logfolder + "/processed_images/")
        createfolder(processed_image_path)
        click_images_path = os.path.join(path, logfolder+"/click_images/")
        click_images_files = [f for f in os.listdir(click_images_path) if f.endswith('.txt')]
        if click_images_files.__len__() >= 1:
            clickLogPath = os.path.join(click_images_path, click_images_files[0])
            #print (clickLogPath)
            clickLogPath = checkErrorLog.check_image_log(clickLogPath)
            #print(clickLogPath)
            logged_clicks,resolution = readClickLog(clickLogPath)
            processClickLog(logged_clicks,click_images_path,processed_image_path,resolution)
        else:
            print("Failed to locate the file click_images")
            print (click_images_path)
            exit()


def readClickLog(clicks_filename):
    f = open(clicks_filename, 'r')
    twoClicks = []
    line = f.readline()
    while line != '' and line != '\n':
        date, real_time, program_name, window_id, username, window_title, resolution, logged_clicks = line.split("|")
        logged_clicks = logged_clicks.split(" ")
        logged_clicks = logged_clicks[:-1]

        #print ("original",logged_clicks)
        #line = f.readline()

        tmp = []
        #print(len(logged_clicks))
        for click in logged_clicks:
            tmp.append(click)
            if len(tmp) == 2:
                twoClicks.append(tmp)
                #print("son dos")
                #print("twoclicks",tmp)
                tmp = []
        line = f.readline()
    #print twoClicks
    return (twoClicks,resolution)



def processClickLog(logged_clicks,clickImagesPath,processed_image_path,resolution):
    for i in logged_clicks:
        infoImage1 = i[0]
        infoImage2 = i[1]
        Xdown, Ydown, miliseg_down, click_down, image_down = infoImage1.split(",")
        Xup, Yup, miliseg_up, click_up, image_up = infoImage2.split(",")
        if (abs(int(Xdown) - int(Xup)) > 15):
            print("")
            print("se sospecha que subrayo")
            print(Xdown, Ydown, miliseg_down, click_down, image_down)
            print(Xup, Yup, miliseg_up, click_up, image_up)
            pathImageDown = os.path.join(clickImagesPath, image_down)
            pathImageUp = os.path.join(clickImagesPath, image_up)
            findCoordinates(Xdown,Ydown,pathImageDown,Xup,Yup,pathImageUp,resolution)
            im = diffImage(pathImageDown, pathImageUp, processed_image_path, miliseg_down)


# find the x, y coordinates inside the image and draw a circle
def findCoordinates(Xdown,Ydown,pathImageDown,Xup,Yup,pathImageUp,screensize):
    imgDown = cv2.imread(pathImageDown)
    imgUp = cv2.imread(pathImageUp)

    screensizeX, screensizeY = screensize.split("x")
    screensizeX = int(screensizeX)
    screensizeY = int(screensizeY)



    #image2 = cv2.circle(img2, (int(Xdown), int(Ydown)), 10, (255, 0, 0), -1)
    #cv2.imshow("primera", image2)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


    # Draw Point
    imageDown = cv2.circle(imgDown, (int(Xdown), int(Ydown)), 10, (255, 0, 0), -1)
    imageUp = cv2.circle(imgUp, (int(Xup), int(Yup)), 10, (255, 0, 0), -1)

    image = cv2.resize(imageDown, (screensizeX/2, screensizeY/2), interpolation=cv2.INTER_AREA)
    image2 = cv2.resize(imageUp, (screensizeX/2, screensizeY/2), interpolation=cv2.INTER_AREA)

    imstack = np.hstack((image, image2))
    cv2.imshow("points", imstack)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # perform the actual resizing of the image and show it
    #resized = cv2.resize(img2, dim, interpolation=cv2.INTER_AREA)
    #cv2.imshow("resized", resized)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #image = cv2.circle(resized, (int(Xdown), int(Ydown)), 10, (255, 0, 0), -1)
    #cv2.imshow("cut", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


    #img = cutImage(Xdown,Ydown,pathImageDown,screensize)

    #Xdown = screensizeX / 4
    #Ydown = screensizeY / 4

    #image = cv2.circle(img, (int(Xdown), int(Ydown)), 10, (255, 0, 0), -1)
    #cv2.imshow("cut", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    '''
    image = cv2.circle(img, (int(Xdown), int(Ydown)), 10, (255, 0, 0), -1)
    #cv2.imwrite("" + image_down + "", image)

    image2 = cv2.circle(img2, (int(Xup), int(Yup)), 10, (255, 0, 0), -1)
    #cv2.imwrite("2" + image_down + "", image2)

    imstack = np.hstack((image, image2))
    cv2.imshow("Clicks", imstack)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''


def cutImage(x,y,img,screensize):
    img = cv2.imread(img)

    screensizeX,screensizeY = screensize.split("x")
    screensizeX = int(screensizeX)
    screensizeY = int(screensizeY)
    x=int(x)
    y=int(y)

    # take the highest point left and the lowest point right. (to form a rectangle cropbox)
    x1 = x - (screensizeX / 4)
    x2 = x + (screensizeX / 4)
    y1 = y - (screensizeY / 4)
    y2 = y + (screensizeY / 4)

    # width and height
    w = x2 - x1
    h = y2 - y1
    #(x1, y1, w, h)

    # Crop image
    #imCrop = img[x1:x1 + w, y1:y1 + h]


    #imCrop = img[x1:x1+w, y1:y1+h]

    #y: y + h, x: x + w


    #cropped = img[x:w, y:h]
    cropped = img[y:y + h,x:x + w]
    #cv2.imshow("cropped", cropped)
    #cv2.waitKey(0)

    return cropped

    #g = Image.fromarray(imCrop)

    #cv2.imshow("crop", g)
    # take a cropbox
    #image_data = pyautogui.screenshot(region=((x1, y1, w, h)))

if __name__ == '__main__':
    loadClickInfo()
