import sys
import cv2
import glob
import os
from os import listdir
import shutil
from pathlib import Path
import string
import numpy as np
import ctypes
import tkinter as tk
from tkinter import ttk
from tkinter import Menu  
from tkinter import messagebox as mbox  
import argparse

global lbl
global txt
global text1

def show_input():
    global lbl
    global txt
    global text1
    text1 = f"{txt.get('1.0', 'end-1c')}"
    lbl.config(text="Ωραία, τώρα κλείσε αυτό το παράθυρο\n και θα ξεκινήσεις από αυτό το αρχείο")

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str)
parser.add_argument('--output', type=str)
args = parser.parse_args()
folder_dir = args.input
#folder_dir = folder_dir.replace(' ', '\\ ')
folder_dir = os.path.join('~', folder_dir)
print(folder_dir)
folder_out = args.output
#folder_out = folder_out.replace(' ', '\\ ')
folder_out_spec = os.path.join('~', folder_out)
print(folder_out_spec)

# root = tk.Tk()
# root.title("Νέος Φάκελος Ξεκίνημα")
# root.geometry('400x200')
# txt = tk.Text(root, height=5, width=40)
# txt.pack()
# btn = tk.Button(root, text="Εισαγωγή φακέλου", command=show_input)
# btn.pack()
# lbl = tk.Label(root, text="")
# lbl.pack()
# root.mainloop()
# data = text1
# folder_in = data
# if folder_in == "video1":
#     folder_dir = os.path.join('~', "/mnt/c/Users/rotas/Desktop/videomicamxeim202627/video1")
# elif folder_in == "video2":
#     folder_dir = os.path.join('~', "/mnt/c/Users/rotas/Desktop/videomicamxeim202627/video2")
# elif folder_in == "video3":
#     folder_dir = os.path.join('~', "/mnt/c/Users/rotas/Desktop/videomicamxeim202627/video3")
# elif folder_in == "video4":
#     folder_dir = os.path.join('~', "/mnt/c/Users/rotas/Desktop/videomicamxeim202627/video4")
# elif folder_in == "video5":
#     folder_dir = os.path.join('~', "/mnt/c/Users/rotas/Desktop/videomicamxeim202627/video5")
# elif folder_in == "video6":
#     folder_dir = os.path.join('~', "/mnt/c/Users/rotas/Desktop/videomicamxeim202627/video6")
# elif folder_in == "video7":
#     folder_dir = os.path.join('~', "/mnt/c/Users/rotas/Desktop/videomicamxeim202627/video7")
# elif folder_in == "video8":
#     folder_dir = os.path.join('~', "/mnt/c/Users/rotas/Desktop/videomicamxeim202627/video8")
img = []
for file_s in os.listdir(folder_dir):
    images = os.fsdecode(file_s)
    if (images.endswith(".png")):
        filetype = ".png"
        img.append(os.path.join(folder_dir, images))
    elif images.endswith(".jpg"):
        filetype = ".jpg"
        img.append(os.path.join(folder_dir, images))
    elif images.endswith(".jpeg"):
        filetype = ".jpeg"
        img.append(os.path.join(folder_dir, images))
print(len(img), "what")
img.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

resolution = (1920, 1080)
dst = folder_out_spec
global i
i = 0
la = [chr(i) for i in range(ord('a'), ord('z') + 1)]
global glbk 
glbk = [0, 0, 0, 0, 0]

def goNext(k1, k2, k3, k4, k5):
    k5 += 1
    if (k5 == 26):
        k5 = 0
        k4 += 1
        if (k4 == 26):
            k4 = 0
            k3 += 1
            if k3 == 26:
                k3 = 0
                k2 += 1
                if k2 ==26:
                    k2 = 0
                    k1 += 1
    ls = []
    ls.append(k1)
    ls.append(k2)
    ls.append(k3)
    ls.append(k4)
    ls.append(k5)
    return ls

def goPrev(k1, k2, k3, k4, k5):
    if (k5 == 0 and k2 == 0 and k3 == 0 and k1 == 0 and k4 == 0):
        return [0, 0, 0, 0, 0]
    k5 -= 1
    if k5 == -1:
        k5 = 9
        k4 -= 1
        if k4 == -1:
            k4 = 9
            k3 -= 1
            if k3 == -1:
                k3 = 9
                k2 -= 1
                if k2 == -1:
                    k2 = 0
                    k1 -= 1
    ls = []
    ls.append(k1)
    ls.append(k2)
    ls.append(k3)
    ls.append(k4)
    ls.append(k5)
    return ls

def hconcat_resize(img_list, 
                   interpolation 
                   = cv2.INTER_CUBIC):
    h_min = min(img.shape[0] 
                for img in img_list)
    
    im_list_resize = [cv2.resize(img,
                       (int(img.shape[1] * h_min / img.shape[0]),
                        h_min), interpolation
                                 = interpolation) 
                      for img in img_list]
    
    return cv2.hconcat(im_list_resize)

def vconcat_resize(img_list, interpolation 
                   = cv2.INTER_CUBIC):
    w_min = min(img.shape[1] 
                for img in img_list)
    
    im_list_resize = [cv2.resize(img,
                      (w_min, int(img.shape[0] * w_min / img.shape[1])),
                                 interpolation = interpolation)
                      for img in img_list]
    return cv2.vconcat(im_list_resize)

def concat_vh(list_2d):
  
    return cv2.vconcat([cv2.hconcat(list_h) 
                        for list_h in list_2d])

def copyStore():
    global glbk
    global t
    k1 = glbk[0]
    k2 = glbk[1]
    k3 = glbk[2]
    k4 = glbk[3]
    k5 = glbk[4]
    nm = dst + f"/{la[k1]}{la[k2]}{la[k3]}{la[k4]}{la[k5]}.png"
    if os.path.exists(nm):
        while os.path.exists(nm):
            ls = goNext(k1, k2, k3, k4, k5)
            k1 = ls[0]
            k2 = ls[1]
            k3 = ls[2]
            k4 = ls[3]
            k5 = ls[4]
            nm = dst + f"/{la[k1]}{la[k2]}{la[k3]}{la[k4]}{la[k5]}.png"
    offset = t-1
    shutil.copyfile(img[i+offset], nm)
    ls = goNext(k1, k2, k3, k4, k5)
    k1 = ls[0]
    k2 = ls[1]
    k3 = ls[2]
    k4 = ls[3]
    k5 = ls[4]
    glbk = [k1, k2, k3, k4, k5]


def click_event(event, x, y, flags, params):

	# checking for left mouse clicks
	if event == cv2.EVENT_LBUTTONDOWN:

		# displaying the coordinates
		# on the Shell
		print(x, ' ', y)

		# displaying the coordinates
		# on the image window
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(img, str(x) + ',' +
					str(y), (x,y), font,
					1, (255, 0, 0), 2)
		cv2.imshow('image', img)


def whenClicked(action, x, y, flags, *userdata):
    global t
    img_t = cv2.imread(img[3], cv2.IMREAD_ANYCOLOR)
    d_y = img_t.shape[0]
    d_x = img_t.shape[1]
    if action == cv2.EVENT_LBUTTONDOWN:
        if y < d_y:
            if x < d_x:
                t = 1
            elif x < 2*d_x:
                t = 2
            else:
                t = 3
        elif y < 2*d_y:
            if x < d_x:
                t = 4
            elif x < 2*d_x:
                t = 5
            else:
                t = 6
        else:
            if x < d_x:
                t = 7
            elif x < 2*d_x:
                t = 8
            else:
                t = 9
        copyStore()



while (i < len(img)-9):
    while True:
        k1 = glbk[0]
        k2 = glbk[1]
        k3 = glbk[2]
        k4 = glbk[3]
        k5 = glbk[4]
        name = "Shoes - Milan"
        cv2.namedWindow(name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
        cv2.moveWindow(name,20,5)
        cv2.resizeWindow(name, resolution[0], resolution[1])
        img_1 = cv2.imread(img[i], cv2.IMREAD_ANYCOLOR)
        img_1_c = img_1.copy()
        print(f"Shape of img1: {img_1_c.shape}")
        text = img[i]
        text = text[63::]
        org_d = (50,450)
        cv2.putText(img_1_c, text, org_d, fontFace = cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.5, color = (0,0,255))
        img_2 = cv2.imread(img[i+1], cv2.IMREAD_ANYCOLOR)
        img_2_c = img_2.copy()
        text = img[i+1]
        text = text[63::]
        org_d = (50,450)
        cv2.putText(img_2_c, text, org_d, fontFace = cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.2, color = (0,0,255))
        img_3 = cv2.imread(img[i+2], cv2.IMREAD_ANYCOLOR)
        img_3_c = img_3.copy()
        text = img[i+2]
        text = text[63::]
        org_d = (50,450)
        cv2.putText(img_3_c, text, org_d, fontFace = cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.2, color = (0,0,255))
        img_4 = cv2.imread(img[i+3], cv2.IMREAD_ANYCOLOR)
        img_4_c = img_4.copy()
        text = img[i+3]
        text = text[63::]
        org_d = (50,450)
        cv2.putText(img_4_c, text, org_d, fontFace = cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.2, color = (0,0,255))
        img_5 = cv2.imread(img[i+4], cv2.IMREAD_ANYCOLOR)
        img_5_c = img_5.copy()
        text = img[i+4]
        text = text[63::]
        org_d = (50,450)
        cv2.putText(img_5_c, text, org_d, fontFace = cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.2, color = (0,0,255))
        img_6 = cv2.imread(img[i+5], cv2.IMREAD_ANYCOLOR)
        img_6_c = img_6.copy()
        text = img[i+5]
        text = text[63::]
        org_d = (50,450)
        cv2.putText(img_6_c, text, org_d, fontFace = cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.2, color = (0,0,255))
        img_7 = cv2.imread(img[i+6], cv2.IMREAD_ANYCOLOR)
        img_7_c = img_7.copy()
        text = img[i+6]
        text = text[63::]
        org_d = (50,450)
        cv2.putText(img_7_c, text, org_d, fontFace = cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.2, color = (0,0,255))
        img_8 = cv2.imread(img[i+7], cv2.IMREAD_ANYCOLOR)
        img_8_c = img_8.copy()
        text = img[i+7]
        text = text[63::]
        org_d = (50,450)
        cv2.putText(img_8_c, text, org_d, fontFace = cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.2, color = (0,0,255))
        img_9 = cv2.imread(img[i+8], cv2.IMREAD_ANYCOLOR)
        img_9_c = img_9.copy()
        text = img[i+8]
        text = text[63::]
        org_d = (50,450)
        cv2.putText(img_9_c, text, org_d, fontFace = cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.2, color = (0,0,255))
        res = concat_vh([[img_1_c, img_2_c, img_3_c], [img_4_c, img_5_c, img_6_c], [img_7_c, img_8_c, img_9_c]])
        print(f"Coordinates of final image: {res.shape}")
        cv2.imshow(name, res)
        what = cv2.setMouseCallback(name, whenClicked)
        key = cv2.waitKey(0)
        if (key == ord('n')):
            break
        elif (key == ord('p')):
            i -= 18
            break
        elif (key == ord('h')):
            root = tk.Tk()
            root.title("Νέο ξεκίνημα")
            root.geometry('400x200')
            txt = tk.Text(root, height=5, width=40)
            txt.pack()
            btn = tk.Button(root, text="Εισαγωγή", command=show_input)
            btn.pack()
            lbl = tk.Label(root, text="")
            lbl.pack()
            root.mainloop()
            data = text1
            file_n = data
            fold_dir = os.path.join('./', "folder", file_n)
            if ((not fold_dir.endswith(filetype))):
                fold_dir = fold_dir + filetype
            if fold_dir in img:
                i = img.index(fold_dir) - 9
                print(i)
                break
            else:
                print("error")
        elif (key == ord('d')):
            ls = goPrev(k1, k2, k3, k4, k5)
            k1 = ls[0]
            k2 = ls[1]
            k3 = ls[2]
            k4 = ls[3]
            k5 = ls[4]
            glbk = [k1, k2, k3, k4, k5]
            nm = dst + f"/{la[k1]}{la[k2]}{la[k3]}{la[k4]}{la[k5]}.png"
            if (os.path.exists(nm)):
                os.remove(nm)
        elif (key == ord('q') or key == 27):
            sys.exit()
    i += 9

cv2.destroyAllWindows()
