# -*- coding: UTF-8 -*-
# https://docs.python.org/zh-cn/3/library/tk.html

import json, os, time, flag
import tkinter as tk
from PIL import Image, ImageTk
from random import choice
from pymongo import MongoClient
from pprint import pprint

class Planner(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # connect to mongodb
        self.client = MongoClient(
            "mongodb+srv://codingchef:I92IhMEoJgfFm9iV@cluster0.u6tr8.mongodb.net/letusbeer?retryWrites=true&w=majority"
        )
        self.db = self.client.letusbeer
        # init window
        self.master = master
        self.master.title("Let's Beer Brewpub Tap List")
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg='#1c1c1c')
        self.currPath = os.path.abspath(os.path.dirname(__file__))
        self.pack()
        self.draw_logo()
        self.data = self.get_data()
        self.taplist = tk.Frame(self.master, bg="#1c1c1c", height=730, width=1500)
        self.draw()
        self.master.msglabel = tk.Label(root, text=self.data['messages'][0], bg="#1c1c1c", fg="#F7F7F7", font=("fzsxsgysjw", 40))
        self.master.msglabel.pack(side=tk.BOTTOM, fill=tk.X, pady=40)
        self.update_notice()

    def draw_logo(self):
        img = Image.open(self.currPath+"/sandbox/hand.png")
        logoImg = ImageTk.PhotoImage(img)
        logo = tk.Label(root, width=77, height=43, bg="#1c1c1c")
        logo.pack(side=tk.TOP)
        logo.configure(image=logoImg, width=logoImg.width(), height=logoImg.height())
        logo.image = logoImg

    def get_data(self):
        data = {}
        data["tap_data"] = []
        data["messages"] = []

        collection = self.db.brewpub_taplist
        res = collection.find({"tapid":{"$lt":"8"}})
        for row in res:
            data["tap_data"].append(row)
        
        collection = self.db.brewpub_message
        res = collection.find()
        for row in res:
            data["messages"].append(row['msg'])
    
        return(data)

    def draw(self):
        fontname = "fzsxsgysjw"
        fontcolor = "#F7F7F7"
        yy = 83
        # print(self.data["tap_data"]["tapid"])
        for tap in self.data['tap_data']:
            xx = 10
            
            if int(tap['tapid']) == 4:
                yy = 83
            if int(tap['tapid']) > 3:
                xx = 810
            if tap['status'] == "0":
                fontcolor = "#333333"
            else:
                fontcolor = "#F7F7F7"
            tapNum =     tk.Label(self.taplist, text='#'+tap['tapid'], bg="#1c1c1c", fg=fontcolor, font=("apple gothic", 50)).place(x=xx, y=yy)
            tapName =    tk.Label(self.taplist, text=tap['brewery'] + " " + tap['beername'] + " " + tap['beerstyle'], bg="#1c1c1c", fg=fontcolor, font=(fontname, 40)).place(x=xx+90, y=yy-20) 
            tapNameEn =  tk.Label(self.taplist, text="Let's Beer Young Master Xiaobai IPA", bg="#1c1c1c", fg=fontcolor, font=("apple sd gothic neo", 18)).place(x=xx+90, y=yy+30) 
            tapDataAbv = tk.Label(self.taplist, text="ABV " + tap['abv'] + '%', bg="#1c1c1c", fg=fontcolor, font=("apple sd gothic neo", 18)).place(x=xx+90, y=yy+60) 
            tapDataIbu = tk.Label(self.taplist, text="IBU " + tap['ibu'], bg="#1c1c1c", fg=fontcolor, font=("apple sd gothic neo", 18)).place(x=xx+200, y=yy+60)
            tapDataFlag= tk.Label(self.taplist, text=flag.flag(tap['country']), bg="#1c1c1c", font=("Courier", 25)).place(x=xx+270, y=yy+60)
            tapPrice =   tk.Label(self.taplist, text="￥" + tap['price'], bg="#1c1c1c", fg=fontcolor, font=("apple sd gothic neo", 45)).place(x=xx+600, y=yy-16)
            tapPriceLine = tk.Label(self.taplist, text="——————", bg="#1c1c1c", fg=fontcolor, font=("apple sd gothic neo", 15)).place(x=xx+602, y=yy+35)
            tapGlasstype=tk.Label(self.taplist, text=tap['glass_type'] + "mL", bg="#1c1c1c", fg=fontcolor, font=("apple sd gothic neo", 18)).place(x=xx+620, y=yy+55)
            yy = yy + 180
        # b1=tk.Canvas(self.taplist)
        # line1=b1.create_line(50,50,50,120,width=5,fill='red')
        # b1.pack()
        self.taplist.pack(side=tk.TOP)
        
    def update_notice(self):
        self.master.msglabel['text'] = choice(self.data['messages'])
        self.master.after(2000, self.update_notice)
    
    def update(self):
        data = {}
        # get data and check diff
        data = self.get_data()
        shared_items = {k: data[k] for k in data if k in self.data and data[k] == self.data[k]}
        # print(len(shared_items))
        # print(data)
        if len(shared_items) == 1:
            #drop all taplist
            self.drop_all_taplist()
            #redraw
            self.data = data
            self.draw()
        self.master.after(10000, self.update)

    def drop_all_taplist(self):
        for child in self.taplist.winfo_children():
            child.destroy()

root = tk.Tk()
app = Planner(master=root)
app.after(10000, app.update)
app.mainloop()
root.destroy()