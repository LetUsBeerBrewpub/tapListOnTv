import sys
import datetime
import json
import requests
from configparser import ConfigParser
import PySide6
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt, QThread, QTimer
from PySide6.QtWidgets import (
    QApplication, QGridLayout, QLabel, 
    QMainWindow, QWidget, QMenu)
from PySide6.QtGui import QGuiApplication, QPixmap, QPainter, QContextMenuEvent, QCursor
from requests.api import get

class TapList(QMainWindow):
    def __init__(self, parent=None):
        # init
        super(TapList, self).__init__(parent)
        self.infoOutput()
        self.loadConfig()
        self.initUI()
        self.initLayout()
        self.makeTapList(getFrom=self.data_source, menuSide=self.side)
        self.createContextMenu()
        # start renew timer  
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.renewTimer)
        self.startTimer()

    # load config parameter
    def loadConfig(self):
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.window_title = self.config.get('default', 'window_title')
        self.side = int(self.config.get('default', 'side'))
        self.renew_period = int(self.config.get('default', 'renew_period'))
        self.data_source = int(self.config.get('default', 'data_source'))
        self.notic_0 = self.config.get('default', 'notic_0')
        self.notic_1 = self.config.get('default', 'notic_1')
        self.logo_path = self.config.get('default', 'logo_path')

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
        # self.setMinimumWidth(800)
        self.layout = QGridLayout()
    
    # setup layout
    def initLayout(self):
        self.layout = QGridLayout()
        self.window = QWidget()
        self.window.setLayout(self.layout)

        # set header(logo) layout
        self.layoutH = QLabel()
        self.layoutH.setObjectName('header')
        self.logo = QPixmap(self.logo_path)
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
        if self.side==0:
            notic_text = self.notic_0
        else:
            notic_text = self.notic_1
        self.layoutF.setText(notic_text)

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
        tapnum = ['0', '1', '2', '3', '4', '5', '6',
                  '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        self.layoutItem_no.setText('#' + tapnum[int(itemData['tapid'])])
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
        # 1-wechat interface\
        # 2-dragon head database
        data = []
        if getdatafrom==0:
            # load data from json file
            with open("sandbox/tapdata.json", "r") as f:
                data = json.load(f)
            if side==1:
                data = data[8:]
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
    
    # remake menu (update/switch)
    def reNewMenu(self):
        self.window.setParent(None)
        self.initLayout()
        self.makeTapList(getFrom=self.data_source, menuSide=self.side)
    
    def renewTimer(self):
        self.endTimer()
        self.reNewMenu()
        self.startTimer()
    
    def startTimer(self):
        self.timer.start(self.renew_period)  # 5000 单位是毫秒， 即 5 秒
        print('do renewMenu')

    def endTimer(self):
        self.timer.stop()
    
    def createContextMenu(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        self.contextMenu = QMenu(self)
        self.actionSWitch = self.contextMenu.addAction(u'Switch')
        self.actionRefresh = self.contextMenu.addAction(u'Refresh')

        self.actionSWitch.triggered.connect(self.switchSide)
        self.actionRefresh.triggered.connect(self.reNewMenu)
    
    def showContextMenu(self, pos):
        self.contextMenu.move(QCursor().pos())
        self.contextMenu.show()
    
    def switchSide(self):
        print(self.side)
        if self.side == 0:
            self.side = 1
        elif self.side == 1:
            self.side = 0
        print(self.side)
        self.reNewMenu()



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
    taplist.show()
    # Run the main Qt loop
    sys.exit(app.exec())
    

if __name__ == "__main__":
    main()
