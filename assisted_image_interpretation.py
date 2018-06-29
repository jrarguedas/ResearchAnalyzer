# -*- coding: utf-8 -*-
from Tkinter import *
from PIL import ImageTk,Image
import Tkinter as tk
from adminfile import *
from images_interpreter import readClickLog
import checkClickErrorLog
import numpy as np
import cv2
import pyautogui

path = os.getcwd() + "/logs_to_treat"
logsList = os.listdir(path)
listLogInfo = []

class Display(object):

    def __init__(self):
        self.images = []
        self.imgIndex = 0
        self.master = tk.Tk()
        self.master.title('Clasificación')
        self.procIndex = 0
        self.idCrop = 1

        self.milisegundos = ""
        self.pathImage = ""
        self.imageDown = ""
        self.cropName = ""
        self.cropFile = ""

        info, self.processed_image_path, self.click_images_path = self.loadAssistedInfo()
        self.logged_clicks, self.resolution = info

        self.getImgList(self.logged_clicks, self.click_images_path)

        self.image_label = tk.Label(master=self.master)
        self.image_label.pack()

        # opcion Menu
        self.variable = tk.StringVar(self.master)
        self.variable.set("Clasificación")  # default value
        self.menu = tk.OptionMenu(self.master, self.variable, "Subrayado", "Menú", "Boton", "Icono", "Nada")
        self.menu.pack()


        # input text
        self.description = tk.Label(self.master, text="Descripción:")
        self.description.pack()
        self.varInput = tk.StringVar(self.master)
        self.input = tk.Entry(self.master,textvariable=self.varInput, bd=5)
        self.input.pack()

        # botton crop
        self.crop_boton = tk.Button(self.master, text="crop", command=lambda s=self: s.crop())
        self.crop_boton.pack(side='bottom', padx=15, pady=15)

        self.master.protocol('WM_DELETE_WINDOW', lambda: self.quit(self.master))

        self.nextBtn = tk.Button(self.master, text='Next', command=lambda s=self: s.run(self.logged_clicks,self.click_images_path,self.resolution)).place(relx=0.90, rely=0.99, anchor=tk.SE)

        self.master.mainloop()

    def getImgList(self,logged_clicks,clickImagesPath):
        imgList = []
        for f in logged_clicks:
            infoImage = f[0]
            Xdown, Ydown, miliseg_down, click_down, image_down = infoImage.split(",")
            pathImageDown = os.path.join(clickImagesPath, image_down)
            imgList.append(pathImageDown)
        self.images = imgList
        #print self.images

    def popupmsg(self,msg):
        self.popup = tk.Tk()
        self.popup.wm_title("!")
        label = tk.Label(self.popup, text=msg)
        label.pack()

        B1 = tk.Button(self.popup, text="Okay", command=self.quit(self.master))
        B1.pack()
        self.popup.mainloop()


    def getImgOpen(self):
        print('Opening')
        width, height = pyautogui.size()

        if(self.imgIndex == len(self.images)-1):
            self.popupmsg("Has terminado")
            #self.quit_(self.master)
        else:
            print("imgINDEX", self.imgIndex)
            imgDown = cv2.imread(self.images[self.imgIndex])
            image = cv2.resize(imgDown, (width - 400, height - 200), interpolation=cv2.INTER_AREA)

            print("Down sola",self.images[self.imgIndex])
            frame = image
            im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            a = Image.fromarray(im)
            b = ImageTk.PhotoImage(image=a)
            self.image_label.configure(image=b)
            self.image_label._image_cache = b
            self.master.update()
            self.imgIndex += 1

        return

    # define funcao para terminar processo
    def quit(self, master):
        # process.terminate()
        master.destroy()

    def crop(self):
        if (self.imgIndex == 0):
            print("No se puede recortar aún")
        else:
            img = self.pathImage
            img = cv2.imread(img)
            img = cv2.resize(img, (1920 - 400, 1080 - 200), interpolation=cv2.INTER_AREA)
            r = cv2.selectROI(img,False,False)

            # Crop image
            imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

            ventana = "crop"
            cv2.imshow(ventana, imCrop)
            self.guardarImage(imCrop)
            cv2.moveWindow(ventana, 40, 30)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


    def loadAssistedInfo(self):
        for logfolder in logsList:
            processed_image_path = os.path.join(path, logfolder + "/processed_images/")
            createfolder(processed_image_path)
            click_images_path = os.path.join(path, logfolder + "/click_images/")
            click_images_files = [f for f in os.listdir(click_images_path) if f.endswith('.txt')]
            if click_images_files.__len__() >= 1:
                clickLogPath = os.path.join(click_images_path, click_images_files[0])
                clickLogPath = checkClickErrorLog.check_image_log(clickLogPath)
                return readClickLog(clickLogPath),processed_image_path,click_images_path

            else:
                print("Failed to locate the file click_images")
                print(click_images_path)
                exit()

    def processAssisted(self,logged_clicks,clickImagesPath,resolution):
        if (self.procIndex == len(self.logged_clicks) - 1):
            print("termino la process")
        else:
            i = logged_clicks[self.procIndex]
            infoImage1 = i[0]
            infoImage2 = i[1]
            Xdown, Ydown, miliseg_down, click_down, image_down = infoImage1.split(",")
            Xup, Yup, miliseg_up, click_up, image_up = infoImage2.split(",")

            self.milisegundos = miliseg_down
            pathImageDown = os.path.join(clickImagesPath, image_down)
            self.imageDown = image_down
            self.pathImage = pathImageDown
            pathImageUp = os.path.join(clickImagesPath, image_up)
            imgDown = cv2.imread(pathImageDown)
            imgUp = cv2.imread(pathImageUp)

            screensizeX, screensizeY = resolution.split("x")
            screensizeX = int(screensizeX)
            screensizeY = int(screensizeY)

            # Draw Point
            imageDown = cv2.circle(imgDown, (int(Xdown), int(Ydown)), 10, (255, 0, 0), -1)
            imageUp = cv2.circle(imgUp, (int(Xup), int(Yup)), 10, (255, 0, 0), -1)

            crop = cv2.resize(imageDown, (screensizeX / 2, screensizeY / 2), interpolation=cv2.INTER_AREA)

            image = cv2.resize(imageDown, (screensizeX / 2, screensizeY / 2), interpolation=cv2.INTER_AREA)
            image2 = cv2.resize(imageUp, (screensizeX / 2, screensizeY / 2), interpolation=cv2.INTER_AREA)

            print("Down",image_down)
            print("Up",image_up)
            imstack = np.hstack((image, image2))
            ventana = "previsualizacion"
            cv2.imshow(ventana, imstack)
            cv2.moveWindow(ventana, 40, 30)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            self.procIndex += 1

    def guardarImage(self,imCrop):
        #print("guardar imagen")

        img = Image.fromarray(imCrop)
        self.cropName =  "crop" + str(self.idCrop) + ".png"
        self.cropFile = os.path.join(self.processed_image_path, self.cropName)
        #print("ruta crop", self.cropFile)
        img.save(self.cropFile)
        self.idCrop += 1


    def guardarLog(self):
        #print("guardar log")
        #print(self.milisegundos)
        #print(self.processed_image_path)
        #print(self.variable.get()) #clasificacion
        #print(self.varInput.get()) #descripcion

        strData = self.milisegundos + "," + self.imageDown + "," + self.variable.get() + "," + self.varInput.get() + "," + self.cropName + "\n"
        image_path = os.path.join(self.processed_image_path, "processed_image.txt")
        #print("ruta",image_path)
        writefileappend(image_path, strData)

    def reset(self):
        self.variable.set("Clasificación")
        self.varInput.set("")

    def run(self,logged_clicks,clickImagesPath,resolution):
        self.processAssisted(logged_clicks,clickImagesPath,resolution)
        self.getImgOpen()
        self.guardarLog()
        self.reset()

d = Display()
#d.getImgOpen()
