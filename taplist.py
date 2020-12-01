# -*- coding: UTF-8 -*-
# https://docs.python.org/zh-cn/3/library/tk.html

import json, os
import tkinter as tk
from PIL import Image, ImageTk
import time
from random import choice
import flag

os.getcwd
currentPath = os.path.abspath(os.path.dirname(__file__))
# get data
with open(currentPath+'/sandbox/tapdata.json', 'r') as f:
    tap_data = json.load(f) 

with open(currentPath+'/sandbox/message.json', 'r') as f:
    message = json.load(f) 

root = tk.Tk()
# title
root.title("Let's Beer Brewpub Tap List")
# fullscreen
root.attributes('-fullscreen', True)
# background color
root.configure(bg='#1c1c1c')
# logo image
img = Image.open(currentPath+"/logo.png")
logoImg = ImageTk.PhotoImage(img)
logo = tk.Label(root, width=77, height=43, bg="#1c1c1c")
logo.pack(side=tk.TOP)
logo.configure(image=logoImg, width=logoImg.width(), height=logoImg.height())
logo.image = logoImg

yy = 180
for tap in tap_data:
    xx = 90
    if int(tap['tapid']) == 4:
        yy = 180
    if int(tap['tapid']) > 3:
        xx = 900
    tapNum = tk.Label(root, text='#'+tap['tapid'], bg="#1c1c1c", fg="#F7F7F7", font=("apple gothic", 50)).place(x=xx, y=yy)
    tapName = tk.Label(root, text=tap['brewery'] + " " + tap['beername'] + " " + tap['beerstyle'], bg="#1c1c1c", fg="#F7F7F7", font=("fzsxsgysjw", 40)).place(x=xx+90, y=yy-20) 
    tapNameEn = tk.Label(root, text="Let's Beer Young Master Xiaobai IPA", bg="#1c1c1c", fg="#F7F7F7", font=("apple sd gothic neo", 18)).place(x=xx+90, y=yy+30) 
    tapDataAbv = tk.Label(root, text="ABV " + tap['abv'] + '%', bg="#1c1c1c", fg="#F7F7F7", font=("apple sd gothic neo", 18)).place(x=xx+90, y=yy+60) 
    tapDataIbu = tk.Label(root, text="IBU " + tap['ibu'], bg="#1c1c1c", fg="#F7F7F7", font=("apple sd gothic neo", 18)).place(x=xx+200, y=yy+60)
    tapDataFlag= tk.Label(root, text=flag.flag(tap['country']), bg="#1c1c1c", font=("Courier", 25)).place(x=xx+270, y=yy+60) 
    tapPrice = tk.Label(root, text="￥" + tap['price'], bg="#1c1c1c", fg="#F7F7F7", font=("apple sd gothic neo", 38)).place(x=xx+600, y=yy-10)
    # tapPriceLine = tk.Label(root, text="----", bg="#1c1c1c", fg="#F7F7F7", font=("apple sd gothic neo", 38)).place(x=xx+600, y=yy+20)
    yy = yy + 180

# function which changes time on Label 
def update_msg():
    # change text on Label 
    msglabel['text'] = choice(message)
    # run `update_time` again after 1000ms (1s)
    root.after(2000, update_msg) # function name without() 

# create label for current time 
msglabel = tk.Label(root, text=message[0], bg="#1c1c1c", fg="#F7F7F7", font=("fzsxsgysjw", 35))
msglabel.pack(side=tk.BOTTOM, fill=tk.X, pady=40)

# run `update_time` first time after 1000ms (1s) 
root.after(2000, update_msg) # function name without() 
#update_time() # or run first time immediately 
root.mainloop()
