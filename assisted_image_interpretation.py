import cv2
import numpy as np
from adminfile import *
import checkErrorLog
from images_interpreter import readClickLog


path = os.getcwd() + "/logs_to_treat"
logsList = os.listdir(path)

listLogInfo = []

# Function that checks if there are folders or not in the address logs_to_treat
# Check the logs of each folder with the scriptchecker script
# For each folder generates a loginfo instance and creates a list
def loadAssistedInfo():
    for logfolder in logsList:
        processed_image_path = os.path.join(path, logfolder + "/processed_images/")
        createfolder(processed_image_path)
        click_images_path = os.path.join(path, logfolder+"/click_images/")
        click_images_files = [f for f in os.listdir(click_images_path) if f.endswith('.txt')]
        if click_images_files.__len__() >= 1:
            clickLogPath = os.path.join(click_images_path, click_images_files[0])
            clickLogPath = checkErrorLog.check_image_log(clickLogPath)
            logged_clicks,resolution = readClickLog(clickLogPath)
            processAssisted(logged_clicks,click_images_path,processed_image_path,resolution)
        else:
            print("Failed to locate the file click_images")
            print (click_images_path)
            exit()


def processAssisted(logged_clicks,clickImagesPath,processed_image_path,resolution):
    for i in logged_clicks:
        infoImage1 = i[0]
        infoImage2 = i[1]
        Xdown, Ydown, miliseg_down, click_down, image_down = infoImage1.split(",")
        Xup, Yup, miliseg_up, click_up, image_up = infoImage2.split(",")


        pathImageDown = os.path.join(clickImagesPath, image_down)
        pathImageUp = os.path.join(clickImagesPath, image_up)
        findCoordinates(Xdown,Ydown,pathImageDown,Xup,Yup,pathImageUp,resolution)
        cutImage(pathImageDown)


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


# crop the image according to the selection box
def cutImage(img):
    # Select ROI
    img = cv2.imread(img)
    r = cv2.selectROI(img)

    # Crop image
    imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

    cv2.imshow("points", imCrop)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #cv2.imwrite("seleccion.png", imCrop)

    #finalimg = Image.fromarray(imCrop)

    #return finalimg

if __name__ == '__main__':
    loadAssistedInfo()