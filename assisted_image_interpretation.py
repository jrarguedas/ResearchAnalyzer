import cv2
import numpy as np
import subprocess
import pytesseract
import pyautogui
from PIL import Image
from adminfile import *

path = os.getcwd() + "/logs_to_treat"

logsList = os.listdir(path)

listLogInfo = []

def loadClickInfo():
    for logfolder in logsList:
        processed_image_path = os.path.join(path, logfolder + "/processed_images/")
        createfolder(processed_image_path)
        click_images_path = os.path.join(path, logfolder+"/click_images/")
        click_images_files = [f for f in os.listdir(click_images_path) if f.endswith('.txt')]
        if click_images_files.__len__() >= 1:
            clickLogPath = os.path.join(click_images_path, click_images_files[0])
            #print(click_images_path)
            process(clickLogPath,click_images_path)
        else:
            print("Failed to locate the file click_images")
            print (click_images_path)
            exit()

# get screen size
def getScreenSize():
    size = pyautogui.size()
    return size


# execute bash command and generate the nameLog
def executeCommand(file):
    bashCommand = "cat "+file+" | cut -f8 -d'|' | tr ' ' '\n' | sed '/^$/d' | paste -s -d'\t\n' > " + nameLog + ""
    p1 = subprocess.Popen(['bash','-c', bashCommand])
    p1.wait()

# find the x, y coordinates inside the image and draw a circle
def findCoordinates(image_down,image_up,ImageDirectory):
    screensize = getScreenSize()
    img = cv2.imread("" + ImageDirectory + "" + image_down + "")
    img2 = cv2.imread("" + ImageDirectory + "" + image_up + "")

    x = screensize[0] / 4
    y = screensize[1] / 4

    image = cv2.circle(img, (x, y), 10, (255, 0, 0), -1)
    #cv2.imwrite("" + image_down + "", image)

    image2 = cv2.circle(img2, (x, y), 10, (255, 0, 0), -1)
    #cv2.imwrite("2" + image_down + "", image2)

    imstack = np.hstack((image, image2))
    cv2.imshow("Clicks", imstack)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# crop the image according to the selection box
def cutImage(img,ImageDirectory):
    # Select ROI
    img = cv2.imread("" + ImageDirectory + "" + img + "")
    r = cv2.selectROI(img)

    # Crop image
    imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

    cv2.imwrite("seleccion.png", imCrop)

    finalimg = Image.fromarray(imCrop)

    return finalimg

# recognize the text in the image with pytesseract
def recognizeText(img):
    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(img)

    print ("Realizo click en --> " + result)


def process(file,ImageDirectory):
    executeCommand(file)
    file = open(nameLog, "r")
    for line in file.readlines():
        info = line.split("\t")
        if len(info)==2:
            infoImage1 = info[0]
            infoImage2 = info[1].rstrip("\n")
            Xdown, Ydown, miliseg_down, click_down, image_down = infoImage1.split(",")
            Xup, Yup, miliseg_up, click_up, image_up = infoImage2.split(",")
            findCoordinates(image_down,image_up,ImageDirectory)
            recognizeText(cutImage(image_down,ImageDirectory))
        else:
            print ("tiene una mas")

loadClickInfo()