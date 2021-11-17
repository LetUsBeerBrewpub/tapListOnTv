import sys
import datetime
import threading
import json
import requests
from configparser import ConfigParser
import PySide6
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import QTime, Qt, QLineF, QLine
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QGridLayout, QLabel, QFrame, 
    QLineEdit, QPushButton, QMainWindow, QVBoxLayout, QWidget)
from PySide6.QtGui import QGuiApplication, QPixmap, QPainter
from requests.api import get

class TapList(QMainWindow):
    def __init__(self, parent=None):
        # init
        super(TapList, self).__init__(parent)
        self.infoOutput()
        self.initUI()
        self.initLayout()
        self.loadConfig()
        self.makeTapList(getFrom=1, menuSide=0)
        self.reNew()

    def loadConfig(self):
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.side = self.config.get('default', 'side')
        self.bg = self.config.get('default', 'bgcolor')
        self.fg = self.config.get('default', 'fgcolor')
        self.mf = self.config.get('default', 'mainfont')
        self.sf = self.config.get('default', 'subfont')
        self.mode = int(self.config.get('default', 'mode'))

    # setup GUI
    def initUI(self):
        # setup UI
        self.setWindowTitle("Taplist - Let's Beer Brewpub")
        # get screen width and height
        self.screen = QGuiApplication.primaryScreen().geometry()
        self.width = self.screen.width()
        self.height = self.screen.height()
        # set screen size
        self.resize(1920, 1080)
        self.setMinimumWidth(800)
    
    # setup layout
    def initLayout(self):
        self.window = QWidget()
        self.layout = QGridLayout()
        self.window.setLayout(self.layout)

        # set header(logo) layout
        self.layoutH = QLabel()
        self.layoutH.setObjectName('header')
        self.logo = QPixmap('img/logo_w.png')
        self.layoutH.setPixmap(self.logo)
        self.layoutH.setFixedHeight(100)
        self.layoutH.setAlignment(Qt.AlignCenter)

        # set tap list item layout
        self.layout0 = QLabel()
        self.layout0.setObjectName('itme_0')
        self.layout4 = QLabel()
        self.layout4.setObjectName('itme_4')
        self.layout1 = QLabel()
        self.layout1.setObjectName('itme_1')
        self.layout5 = QLabel()
        self.layout5.setObjectName('itme_5')
        self.layout2 = QLabel()
        self.layout2.setObjectName('itme_2')
        self.layout6 = QLabel()
        self.layout6.setObjectName('itme_6')
        self.layout3 = QLabel()
        self.layout3.setObjectName('itme_3')
        self.layout7 = QLabel()
        self.layout7.setObjectName('itme_7')
        self.layout8 = QLabel()                 # splitter line
        self.layout8.setObjectName('splitter')
        self.layout8.setFixedWidth(3)

        # set footer(message bar) layout
        self.layoutF = QLabel()
        self.layoutF.setObjectName('footer')
        self.layoutF.setFixedHeight(120)
        self.layoutF.setAlignment(Qt.AlignCenter)
        self.layoutF.setText("生啤尝味套装 150mL × 4杯 任选 ￥68/组 (不重复)")

        # gridding
        self.layout.addWidget(self.layoutH, 0, 0, 1, 3)
        self.layout.addWidget(self.layout0, 1, 0)
        self.layout.addWidget(self.layout4, 1, 2)
        self.layout.addWidget(self.layout1, 2, 0)
        self.layout.addWidget(self.layout5, 2, 2)
        self.layout.addWidget(self.layout2, 3, 0)
        self.layout.addWidget(self.layout6, 3, 2)
        self.layout.addWidget(self.layout3, 4, 0)
        self.layout.addWidget(self.layout7, 4, 2)
        self.layout.addWidget(self.layout8, 1, 1, 4, 1)
        self.layout.addWidget(self.layoutF, 5, 0, 1, 3)
        # self.layout.addWidget(self.layoutFIcon, 5, 1, 1, 1)
        
        self.setCentralWidget(self.window)

    def draw(self, targetLayout, itemData):
        self.layoutItemDetail = QGridLayout(parent=targetLayout)

        self.layoutItem_no      = QLabel()
        self.layoutItem_no.setObjectName('layoutItem_no')
        self.layoutItem_no.setAlignment(Qt.AlignCenter)
        self.layoutItem_namecn  = QLabel()
        self.layoutItem_namecn.setObjectName('layoutItem_namecn')
        self.layoutItem_namecn.setAlignment(Qt.AlignBottom)
        self.layoutItem_nameen  = QLabel()
        self.layoutItem_nameen.setObjectName('layoutItem_nameen')
        self.layoutItem_data    = QLabel()
        self.layoutItem_data.setObjectName('layoutItem_data')
        self.layoutItem_data.setAlignment(Qt.AlignTop)
        self.layoutItem_price   = QLabel()
        self.layoutItem_price.setObjectName('layoutItem_price')
        self.layoutItem_price.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.layoutItem_capacity = QLabel()
        self.layoutItem_capacity.setObjectName('layoutItem_capacity')
        self.layoutItem_capacity.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        self.layoutItemDetail.addWidget(self.layoutItem_no,    0, 0, 4,  2)
        self.layoutItemDetail.addWidget(self.layoutItem_namecn,0, 3, 2, 12)
        self.layoutItemDetail.addWidget(self.layoutItem_nameen,2, 3, 1, 12)
        self.layoutItemDetail.addWidget(self.layoutItem_data,  3, 3, 1, 12)
        self.layoutItemDetail.addWidget(self.layoutItem_price, 0, 15, 2, 2)
        self.layoutItemDetail.addWidget(self.layoutItem_capacity, 2, 15, 2, 2)

        self.write2Layout(itemData)
    
    def write2Layout(self, itemData):
        self.layoutItem_no.setText('#' + itemData['tapid'])
        self.layoutItem_namecn.setText(
            itemData['brewery'] + ' ' + itemData['beername'] + ' ' + itemData['beerstyle'])
        self.layoutItem_nameen.setText(itemData['beernameen'])
        self.layoutItem_data.setText(
            '酒精度 ' + itemData['abv'] + '% ABV   苦度 ' + itemData['ibu'] + ' IBU')
        self.layoutItem_price.setText('￥' + itemData['price'])
        self.layoutItem_capacity.setText(
            '杯型<br>' + itemData['glass_type'] + 'mL')

    def makeTapList(self, getFrom, menuSide=0):
        # get data
        self.data = self.getData(getdatafrom=getFrom, side=menuSide)
        # draw
        for i in range(8):
            exec('self.draw(targetLayout=self.layout%s,itemData=self.data[i])'%str(i))
            # check item status
            if self.data[i]['status'] == '0':
                exec('self.layout%s.setStyleSheet("color: #F7F7F7;")' % str(i))
            else:
                exec('self.layout%s.setStyleSheet("color: #373737;")' % str(i))

    def getData(self, getdatafrom, side):
        # get data from: 
        # 0-test json data
        # 1-wechat interface
        # 2-dragon head database
        data = []
        if getdatafrom==0:
            # load data from json file
            with open("sandbox/tapdata.json", "r") as f:
                data = json.load(f)
        elif getdatafrom==1:
            data = self.getDataFromWx(side=side)
        return data

    def getDataFromWx(self,side):
        data = []
        token = self.wx_get_access_token()
        # tap info
        if side == 0:
            query_str = '''
            db.collection("tapinfo").where({'tapid':_.lt(8)}).orderBy(
                'tapid', 'asc').limit(8).get()
            '''
        elif side == 1:
            query_str = '''
            db.collection("tapinfo").where({'tapid':_.gte(8)}).orderBy('tapid', 'asc').limit(8).get()
            '''
        try:
            query_result = self.wx_query_data(token=token, query=query_str)
        except:
            data = self.data
            print('err_log:get query data from wx failed.')
        else:
            for row in query_result:
                r = json.loads(row)
                if r['status'] == True:
                    status = '0'
                elif r['status'] == False:
                    status = '1'
                data.append({
                    'tapid': str(r['tapid']),
                    'brewery': r['brewery'],
                    'beername': r['beername'],
                    'beerstyle': r['beerstyle'],
                    'beernameen': r['ebeername'],
                    'abv': r['abv'],
                    'ibu': r['ibu'],
                    'price': r['price'],
                    'glass_type': r['glass_type'],
                    'country': r['country'],
                    'status': status
                })
        return data

    def wx_get_access_token(self):
        cs_url = 'https://api.weixin.qq.com/cgi-bin/token?'
        param = {
            'grant_type': 'client_credential',
            'appid': self.config.get('wx', 'appid'),
            'secret': self.config.get('wx', 'secret')
        }
        headers = {'Accept': 'application/json'}
        try:
            r = requests.get(cs_url, params=param, headers=headers)
        except:
            print('err_log:get access token failed.')
        else:
            data = json.loads(r.text)

        if 'errcode' in data:
            print(data['errmsg'])
        else:
            return data['access_token']

    def wx_get_collection(self, token):
        cs_url = 'https://api.weixin.qq.com/tcb/databasecollectionget?'
        params = {
            'access_token': token
        }
        body = {
            'limit': '10',
            'offset': '0',
            'env': self.config.get('wx', 'envid')
        }
        headers = {'content-type': 'application/json'}
        try:
            r = requests.post(cs_url, params=params,
                            data=json.dumps(body), headers=headers)
        except:
            return self.data
        else:
            data = json.loads(r.text)
        if data['errcode'] == 0:
            return data['collections']
        else:
            return data['errmsg']

    def wx_query_data(self, token, query):
        cs_url = 'https://api.weixin.qq.com/tcb/databasequery?'
        params = {
            'access_token': token
        }
        body = {
            'env': self.config.get('wx', 'envid'),
            'query': query
        }
        headers = {'content-type': 'application/json'}
        try:
            r = requests.post(cs_url, params=params,
                data=json.dumps(body), headers=headers)
        except:
            return self.data
        else:
            data = json.loads(r.text)
            if data['errcode'] == 0:
                return data['data']
            else:
                return data['errmsg']
    
    def reNew(self):
        # timer = QTime()
        # while True:
        #     time.sleep(10)
        #     self.clearLabel()
        #     self.makeTapList(getFrom=0, menuSide=0)
        #     print('renew taplist at:')
        #     print(datetime.datetime.now())
        # time.sleep(10)
        # self.clearLabel()
        # self.layoutF.setText('哈哈哈')
        print('')

    # output information
    def infoOutput(self):
        print(datetime.datetime.now())
        print("Python version is " + sys.version)
        print("PySide6 version is " + PySide6.__version__)


def main():
    # Create the Qt Application
    app = QApplication(sys.argv)
    # load sytle
    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    # Create and show
    taplist = TapList()
    # show full screen
    # taplist.showFullScreen()
    taplist.show()
    # Run the main Qt loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
