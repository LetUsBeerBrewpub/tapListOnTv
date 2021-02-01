# -*- coding: UTF-8 -*-
# https://docs.python.org/zh-cn/3/library/tk.html

import json, os, time, flag
from configparser import ConfigParser
import tkinter as tk
from PIL import Image, ImageTk
from random import choice
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

        # set window
        self.master = master
        self.master.title(self.config.get('default', 'title'))
        self.master.attributes('-fullscreen', True)
        self.w_width = self.master.winfo_width()
        self.w_height = self.master.winfo_height()

        # get path
        self.currPath = os.path.abspath(os.path.dirname(__file__))

        # init build
        self.canvas = tk.Canvas(
            self.master,
            width=self.w_width, 
            height=self.w_height,
            borderwidth=0, 
            highlightthickness=0,
            bg=self.bg
        )
        self.canvas.place(x=0, y=0)
        self.canvas.pack(fill='both', expand='yes')

        # output to gui
        self.data = self.get_data()
        self.draw()

    def draw_logo(self):
        img = Image.open(self.currPath+"/img/logo.png")
        self.canvas.logo = ImageTk.PhotoImage(img)
        self.canvas.create_image(self.w_width/2, 15, anchor="n", image=self.canvas.logo)

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

        # draw logo
        self.draw_logo()

        # draw a parting line
        self.canvas.create_line(self.w_width/2, 150, self.w_width/2, self.w_height-300, fill=self.fg, width=2)
        # draw taplist
        yy = 150
        for tap in self.data['tap_data']:
            xx = self.w_width/16
            if tap['tapid'] == num[0]:
                yy = 150
            if tap['tapid'] > num[1]:
                xx += 830

            if tap['status'] == 0:
                fontcolor = "#333333"
            else:
                fontcolor = self.fg

            self.canvas.create_text(xx, yy, fill=fontcolor, font=(self.sf, 60), text='#'+ tapnum[tap['tapid']])
            self.canvas.create_text(xx+100, yy-20, anchor="w", fill=fontcolor, font=(self.mf, 32), text=tap['brewery'] + " " + tap['beername'] + " " + tap['beerstyle'])
            self.canvas.create_text(xx+100, yy+40, anchor="w", fill=fontcolor, font=(self.sf, 19), text=tap['ebeername'])
            self.canvas.create_text(xx+100, yy+88, anchor="w", fill=fontcolor, font=(self.sf, 22), text="ABV " + str(tap['abv']) + '%')
            self.canvas.create_text(xx+250, yy+88, anchor="w", fill=fontcolor, font=(self.sf, 22), text="IBU " + str(tap['ibu']))
            self.canvas.create_text(xx+330, yy+88, anchor="w", fill=fontcolor, font=(self.sf, 22), text=flag.flag(tap['country']))
            self.canvas.create_text(xx+600, yy+20, anchor="w", fill=fontcolor, font=(self.sf, 42), text="￥" + str(tap['price']))
            self.canvas.create_line(xx+590, yy+40, xx+680, yy+40, fill=fontcolor, width=2)
            self.canvas.create_text(xx+620, yy+55, anchor="w", fill=fontcolor, font=(self.sf, 18), text=str(tap['glass_type']) + "mL")
            yy = yy + 200
        
        # messages
        self.notice = self.canvas.create_text(self.w_width/2, 900, anchor="n", fill=self.fg, font=(self.mf, 40), text=self.data['messages'][0])
        self.update_notice()
        
    def update_notice(self):
        new_text = choice(self.data['messages'])
        self.canvas.itemconfig(self.notice, text=new_text)
        self.canvas.after(self.config.get('default', 'msgchangetime'), self.update_notice)
    
    def update(self):
        data = {}
        # get data and check diff
        data = self.get_data()
        shared_items = {k: data[k] for k in data if k in self.data and data[k] == self.data[k]}

        if len(shared_items) == 1:
            #drop all taplist
            self.canvas.delete("all")
            #redraw
            self.data = data
            self.draw()
        self.master.after(self.config.get('default', 'tapinfochecktime'), self.update)
    
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