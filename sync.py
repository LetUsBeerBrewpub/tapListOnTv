# -*- coding: UTF-8 -*-
# https://docs.python.org/zh-cn/3/library/tk.html

import json, os, time, pymysql
from pymysql.converters import escape_string
from configparser import ConfigParser
import requests

class Sync():
    def __init__(self):
        super().__init__()

        # load config file
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.side = self.config.get('default', 'side')
        self.bg = self.config.get('default', 'bgcolor')
        self.fg = self.config.get('default', 'fgcolor')
        self.mf = self.config.get('default', 'mainfont')
        self.sf = self.config.get('default', 'subfont')
        self.mode = int(self.config.get('default', 'mode'))

        # mysql connect
        self.mydb = pymysql.connect(
            host=self.config.get('mysql', 'db_host'), 
            user=self.config.get('mysql', 'db_user'),
            passwd=self.config.get('mysql', 'db_pass'),
            db=self.config.get('mysql', 'db_name'),
            port=3306, 
            charset='utf8')
        
    def wx_get_access_token(self):
        cs_url = 'https://api.weixin.qq.com/cgi-bin/token?'
        param  = {
            'grant_type':'client_credential',
            'appid':self.config.get('wx', 'appid'),
            'secret':self.config.get('wx', 'secret')
        }
        headers = {'Accept':'application/json'}
        r = requests.get(cs_url, params=param, headers=headers)
        data = json.loads(r.text)
        # print(type(data))
        if 'errcode' in data:
            print(data['errmsg'])
        else:
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

    def get_data(self):
        data = {}
        data["tap_data"] = []
        data["messages"] = []
        messages = []

        token = self.wx_get_access_token()
        # tap info
        query_str = '''
        db.collection("tapinfo").orderBy('tapid', 'asc').limit(16).get()
        '''
        query_result = self.wx_query_data(token=token, query=query_str)
        # print(query_result)
        for row in query_result:
            data["tap_data"].append(json.loads(row))

        # message
        query_str = '''
        db.collection("message").get()
        '''
        query_result = self.wx_query_data(token=token, query=query_str)
        for row in query_result:
            messages.append(json.loads(row)['content'])
        data["messages"] = messages

        str = escape_string(data["messages"])
        print(str)

        return(data)

    def store2db(self, data):
        cursor = self.mydb.cursor()
        res = cursor.execute('update json_data set tapinfo='+escape_string(data['tapinfo'])+', message='+escape_string(data['message'])+'where id=1')
        print(res)
        # self.mydb.close()
    
    def update(self):
        data = self.get_data()
        self.store2db(data = data)
        



sync = Sync()
res = sync.get_data()
