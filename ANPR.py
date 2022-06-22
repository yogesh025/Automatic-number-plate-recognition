#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk,Image
import numpy
import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
import numpy as np


def upload_image():
    #choose file from computer 
    file_path = filedialog.askopenfilename()
    #upload image
    uploaded = Image.open(file_path)
    #upload thumbnail
    uploaded.thumbnail(((top.winfo_width()/2.25),(top.winfo_height()/2.25)))
    #configuration for gui
    im = ImageTk.PhotoImage(uploaded)
    sign_image.configure(image= im)
    sign_image.image = im
    label.configure(text =' ')
    show_classify_button(file_path)
    
def show_classify_button(file_path):
    #show buttons and filename
    classify_btn = Button(top, text='Recognize Plate', command= lambda: classify(file_path), padx=10, pady=5)
    classify_btn.place(relx=0.79, rely=0.46)
    
def classify(file_path):
    # read image
    img = cv2.imread(file_path,cv2.IMREAD_COLOR)
    #resize image
    img = cv2.resize(img, (620,480) )
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale

    gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise

    edged = cv2.Canny(gray, 30, 200) #Perform Edge detection

    # find contours in the edged image, keep only the largest

    # ones, and initialize our screen contour

    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)

    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

    screenCnt = None

    # loop over our contours

    for c in cnts:

     # approximate the contour

     peri = cv2.arcLength(c, True)

     approx = cv2.approxPolyDP(c, 0.018 * peri, True)



     # if our approximated contour has four points, then

     # we can assume that we have found our screen

     if len(approx) == 4:

      screenCnt = approx

      break



    if screenCnt is None:

     detected = 0

     print ("No contour detected")

    else:

     detected = 1

    if detected == 1:

     cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

    # Masking the part other than the number plate

    mask = np.zeros(gray.shape,np.uint8)

    new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)

    new_image = cv2.bitwise_and(img,img,mask=mask)

    # Now crop

    (x, y) = np.where(mask == 255)

    (topx, topy) = (np.min(x), np.min(y))

    (bottomx, bottomy) = (np.max(x), np.max(y))

    Cropped = gray[topx:bottomx+1, topy:bottomy+1]



    #Read the number plate

    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    #show the number plate
    print("Detected Number is:",text)
    label.configure(foreground= '#011638', text = text)

#gui size and style configuration
top = tk.Tk()
top.geometry('800x600')
top.title('GUI')
top.configure(background = '#CDCDCD')
heading = Label(top, text = 'GUI', pady=20, font= ('arial', 20, 'bold'))
heading.configure(background = '#CDCDCD', foreground= '#364156')
upload= Button(top, text = 'upload an image', command= upload_image, padx=10, pady=5)
upload.configure(background = '#364156', foreground= 'white', font= ('arial', 10, 'bold'))
upload.pack(side= BOTTOM, pady=50)
sign_image = Label(top)
sign_image.pack(side= BOTTOM, expand= True)
label = Label(top, background ='#CDCDCD', font= ('arial', 15, 'bold'))
label.pack(side= BOTTOM, expand= True)
#run the program
top.mainloop()


# In[ ]:




