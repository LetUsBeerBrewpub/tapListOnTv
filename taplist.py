# -*- coding: UTF-8 -*-
# https://docs.python.org/zh-cn/3/library/tk.html

import json, os, time, flag
from configparser import ConfigParser
import tkinter as tk
from PIL import Image, ImageTk
from random import choice
from pymongo import MongoClient
from pprint import pprint
import requests

class Planner(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # load config file
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.bg = self.config.get('default', 'bgcolor')
        self.fg = self.config.get('default', 'fgcolor')
        self.mf = self.config.get('default', 'mainfont')
        self.sf = self.config.get('default', 'subfont')

        # connect to mongodb
        self.client = MongoClient(
            self.config.get('mongodb', 'url')
        )
        self.db = self.client.letusbeer
        # init window
        self.master = master
        self.master.title(self.config.get('default', 'title'))
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg='#1c1c1c')
        self.currPath = os.path.abspath(os.path.dirname(__file__))
        self.pack()
        self.draw_logo()
        self.data = self.get_data()
        self.taplist = tk.Frame(self.master, bg=self.bg, height=730, width=1500)
        self.draw()
        self.master.msglabel = tk.Label(root, text=self.data['messages'][0], bg=self.bg, fg=self.fg, font=(self.mf, 40))
        self.master.msglabel.pack(side=tk.BOTTOM, fill=tk.X, pady=40)
        self.update_notice()

    def draw_logo(self):
        img = Image.open(self.currPath+"/img/logo.png")
        logoImg = ImageTk.PhotoImage(img)
        logo = tk.Label(root, width=77, height=43, bg=self.bg)
        logo.pack(side=tk.TOP)
        logo.configure(image=logoImg, width=logoImg.width(), height=logoImg.height())
        logo.image = logoImg

    def get_data(self):
        data = {}
        data["tap_data"] = []
        data["messages"] = []
        messages = []

        token = self.wx_get_access_token()
        # tap info
        if self.config.get('default', 'side') == 'left':
            query_str = '''
            db.collection("tapinfo").where({'tapid':_.lt(8)}).orderBy('tapid', 'asc').limit(8).get()
            '''
        elif self.config.get('default', 'side') == 'right':
            query_str = '''
            db.collection("tapinfo").where({'tapid':_.gte(8)}).orderBy('tapid', 'asc').limit(8).get()
            '''
        query_result = self.wx_query_data(token = token, query = query_str)
        for row in query_result:
            data["tap_data"].append(json.loads(row))

        # message
        query_str = '''
        db.collection("message").get()
        '''
        query_result = self.wx_query_data(token = token, query = query_str)
        for row in query_result:
            messages.append(json.loads(row)['content'])
        if self.config.get('default', 'side') == 'left':
            data["messages"] = messages[::2]
        elif self.config.get('default', 'side') == 'right':
            data["messages"] = messages[1::2]  

        return(data)

    def draw(self):
        fontcolor = self.fg

        tapnum = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

        if self.config.get('default', 'side') == 'left':
            num = [4,3]
        elif self.config.get('default', 'side') == 'right':
            num = [12,11]

        yy = 83
        for tap in self.data['tap_data']:
            xx = 10
            if tap['tapid'] == num[0]:
                yy = 83
            if tap['tapid'] > num[1]:
                xx = 810

            if tap['status'] == 0:
                fontcolor = "#333333"
            else:
                fontcolor = self.fg

            tapNum =     tk.Label(self.taplist, bg=self.bg, fg=fontcolor, font=(self.sf, 50), text='#'+ tapnum[tap['tapid']]).place(x=xx, y=yy)
            tapName =    tk.Label(self.taplist, bg=self.bg, fg=fontcolor, font=(self.mf, 40), text=tap['brewery'] + " " + tap['beername'] + " " + tap['beerstyle']).place(x=xx+90, y=yy-20) 
            tapNameEn =  tk.Label(self.taplist, bg=self.bg, fg=fontcolor, font=(self.sf, 18), text="Let's Beer Young Master Xiaobai IPA").place(x=xx+90, y=yy+30) 
            tapDataAbv = tk.Label(self.taplist, bg=self.bg, fg=fontcolor, font=(self.sf, 18), text="ABV " + str(tap['abv']) + '%').place(x=xx+90, y=yy+60) 
            tapDataIbu = tk.Label(self.taplist, bg=self.bg, fg=fontcolor, font=(self.sf, 18), text="IBU " + str(tap['ibu'])).place(x=xx+200, y=yy+60)
            tapDataFlag= tk.Label(self.taplist, bg=self.bg, font=(self.sf, 25), text=flag.flag(tap['country'])).place(x=xx+270, y=yy+55)
            tapPrice =   tk.Label(self.taplist, bg=self.bg, fg=fontcolor, font=(self.sf, 45), text="￥" + str(tap['price'])).place(x=xx+600, y=yy-16)
            tapPriceLine=tk.Label(self.taplist, bg=self.bg, fg=fontcolor, font=(self.sf, 15), text="——————").place(x=xx+602, y=yy+35)
            tapGlasstype=tk.Label(self.taplist, bg=self.bg, fg=fontcolor, font=(self.sf, 18), text=str(tap['glass_type']) + "mL").place(x=xx+620, y=yy+55)
            yy = yy + 180
        # b1=tk.Canvas(self.taplist)
        # line1=b1.create_line(50,50,50,120,width=5,fill='red')
        # b1.pack()
        self.taplist.pack(side=tk.TOP)
        
    def update_notice(self):
        self.master.msglabel['text'] = choice(self.data['messages'])
        self.master.after(self.config.get('default', 'msgchangetime'), self.update_notice)
    
    def update(self):
        data = {}
        # get data and check diff
        data = self.get_data()
        shared_items = {k: data[k] for k in data if k in self.data and data[k] == self.data[k]}

        if len(shared_items) == 1:
            #drop all taplist
            self.drop_all_taplist()
            #redraw
            self.data = data
            self.draw()
        self.master.after(self.config.get('default', 'tapinfochecktime'), self.update)

    def drop_all_taplist(self):
        for child in self.taplist.winfo_children():
            child.destroy()
    
    def wx_get_access_token(self):
        cs_url = 'https://api.weixin.qq.com/cgi-bin/token?'
        param  = {
            'grant_type':'client_credential',
            'appid':self.config.get('wx', 'appid'),
            'secret':self.config.get('wx', 'secret')
        }
        headers = {'Accept':'application/json'}
        r = requests.get(cs_url, params = param, headers = headers)
        data = json.loads(r.text)
        return data['access_token']

    def wx_get_collection(self, token):
        cs_url = 'https://api.weixin.qq.com/tcb/databasecollectionget?'
        params = {
            'access_token':token
        }
        body = {
            'limit':'10',
            'offset':'0',
            'env':self.config.get('wx', 'envid')
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(cs_url, params = params, data = json.dumps(body), headers = headers)
        data = json.loads(r.text)
        if data['errcode'] == 0:
            return data['collections']
        else:
            return data['errmsg']

    def wx_query_data(self, token, query):
        cs_url = 'https://api.weixin.qq.com/tcb/databasequery?'
        params = {
            'access_token':token
        }
        body = {
            'env':self.config.get('wx', 'envid'),
            'query':query
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(cs_url, params = params, data = json.dumps(body), headers = headers)
        data = json.loads(r.text)
        if data['errcode'] == 0:
            return data['data']
        else:
            return data['errmsg']

cfg = ConfigParser()
cfg.read('config.ini')

root = tk.Tk()
app = Planner(master=root)
app.after(cfg.get('default', 'tapinfochecktime'), app.update)
app.mainloop()
# root.destroy()