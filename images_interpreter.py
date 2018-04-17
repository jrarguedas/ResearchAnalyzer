# -*- coding: utf-8 -*-

from loginfo import LogInfo
import os
import subprocess
import pyautogui
from image_underline import diffImage
import cv2
from adminfile import *

path = os.getcwd() + "/logs_to_treat"

logsList = os.listdir(path)

listLogInfo = []
nameLog = "coordinates.log"

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
            #print(click_images_path)
            readClickLog(clickLogPath,click_images_path)
        else:
            print("Failed to locate the file click_images")
            print (click_images_path)
            exit()


# execute bash command and generate the nameLog
def executeCommand(file):
    bashCommand = "cat "+file+" | cut -f8 -d'|' | tr ' ' '\n' | sed '/^$/d' | paste -s -d'\t\n' > " + nameLog + ""
    p1 = subprocess.Popen(['bash','-c', bashCommand])
    p1.wait()

def readClickLog(file, clickImagesPath):
    executeCommand(file)
    file = open(nameLog, "r")
    for line in file.readlines():
        info = line.split("\t")
        if len(info) == 2:
            processClickLog(info,clickImagesPath)

        else:
            print ("tiene una más")

def processClickLog(info,clickImagesPath):
    infoImage1 = info[0]
    infoImage2 = info[1].rstrip("\n")
    Xdown, Ydown, miliseg_down, click_down, image_down = infoImage1.split(",")
    Xup, Yup, miliseg_up, click_up, image_up = infoImage2.split(",")
    if (Xdown != Xup or Ydown != Yup):
        print("se sospecha que subrayo")
        print(image_up)
        pathImageDown = os.path.join(clickImagesPath, image_down)
        pathImageUp = os.path.join(clickImagesPath, image_up)
        im = diffImage(pathImageDown, pathImageUp)
        # cv2.imshow("h",im)

loadClickInfo()
