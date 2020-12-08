# -*- coding: UTF-8 -*-
# https://docs.python.org/zh-cn/3/library/tk.html

import json, os, time, flag
import tkinter as tk
from PIL import Image, ImageTk
from random import choice

class Planner(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # init
        self.master.title("Let's Beer Brewpub Tap List")
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg='#1c1c1c')
        self.currPath = os.path.abspath(os.path.dirname(__file__))
        self.pack()
        self.drawLogo()
        self.getData()
        self.master.msglabel = tk.Label(root, text=self.messages[0], bg="#1c1c1c", fg="#F7F7F7", font=("fzsxsgysjw", 40))
        self.master.msglabel.pack(side=tk.BOTTOM, fill=tk.X, pady=40)   
    
    def drawLogo(self):
        img = Image.open(self.currPath+"/sandbox/hand.png")
        logoImg = ImageTk.PhotoImage(img)
        logo = tk.Label(root, width=77, height=43, bg="#1c1c1c")
        logo.pack(side=tk.TOP)
        logo.configure(image=logoImg, width=logoImg.width(), height=logoImg.height())
        logo.image = logoImg

    def getData(self):
        with open(self.currPath+'/sandbox/tapdata.json', 'r') as f:
            self.tap_data = json.load(f)
        with open(self.currPath+'/sandbox/message.json', 'r') as f:
            self.messages = json.load(f)

    def draw(self):
        fontname = "fzsxsgysjw"
        yy = 180
        for tap in self.tap_data:
            xx = 90
            if int(tap['tapid']) == 4:
                yy = 180
            if int(tap['tapid']) > 3:
                xx = 900
            tapNum = tk.Label(root, text='#'+tap['tapid'], bg="#1c1c1c", fg="#F7F7F7", font=("apple gothic", 50)).place(x=xx, y=yy)
            tapName = tk.Label(root, text=tap['brewery'] + " " + tap['beername'] + " " + tap['beerstyle'], bg="#1c1c1c", fg="#F7F7F7", font=(fontname, 40)).place(x=xx+90, y=yy-20) 
            tapNameEn = tk.Label(root, text="Let's Beer Young Master Xiaobai IPA", bg="#1c1c1c", fg="#F7F7F7", font=("apple sd gothic neo", 18)).place(x=xx+90, y=yy+30) 
            tapDataAbv = tk.Label(root, text="ABV " + tap['abv'] + '%', bg="#1c1c1c", fg="#F7F7F7", font=("apple sd gothic neo", 18)).place(x=xx+90, y=yy+60) 
            tapDataIbu = tk.Label(root, text="IBU " + tap['ibu'], bg="#1c1c1c", fg="#F7F7F7", font=("apple sd gothic neo", 18)).place(x=xx+200, y=yy+60)
            tapDataFlag= tk.Label(root, text=flag.flag(tap['country']), bg="#1c1c1c", font=("Courier", 25)).place(x=xx+270, y=yy+60) 
            tapPrice = tk.Label(root, text="￥" + tap['price'], bg="#1c1c1c", fg="#F7F7F7", font=("apple sd gothic neo", 38)).place(x=xx+600, y=yy-10)
            # tapPriceLine = tk.Label(root, text="----", bg="#1c1c1c", fg="#F7F7F7", font=("apple sd gothic neo", 38)).place(x=xx+600, y=yy+20)
            yy = yy + 180
    
    def updateNotice(self):
        self.master.msglabel['text'] = choice(self.messages)
        self.master.after(2000, self.updateNotice)






root = tk.Tk()
app = Planner(master=root)
app.draw()
app.updateNotice()
app.mainloop()