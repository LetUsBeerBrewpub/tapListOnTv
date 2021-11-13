import sys, datetime
import PySide6
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt, QLineF, QLine
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QGridLayout, QLabel, QFrame, 
    QLineEdit, QPushButton, QMainWindow, QVBoxLayout, QWidget)
from PySide6.QtGui import QGuiApplication, QPixmap, QPainter


class TapList(QMainWindow):
    def __init__(self, parent=None):
        # init
        super(TapList, self).__init__(parent)
        self.infoOutput()
        self.initUI()
        self.initLayout()
        self.draw(targetLayout=self.layout0)
        self.draw(targetLayout=self.layout1)
        self.draw(targetLayout=self.layout2)
        self.draw(targetLayout=self.layout3)
        self.draw(targetLayout=self.layout4)
        self.draw(targetLayout=self.layout5)
        self.draw(targetLayout=self.layout6)
        self.draw(targetLayout=self.layout7)

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
        self.layoutFIcon = QLabel()
        self.layoutFIcon.setObjectName('layoutFIcon')

        self.beerSetIcon = QPixmap('img/beerset.png')
        self.layoutFIcon.setPixmap(self.beerSetIcon)
        # self.beerSetIcon.setFixedHeight(80)
        # self.layoutF.setAlignment(Qt.AlignCenter)

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

    def draw(self, targetLayout, itemData = 0):
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

        self.layoutItem_no.setText('#0')
        self.layoutItem_namecn.setText('乐啤 乳酸菌苏打 (无酒精)')
        self.layoutItem_nameen.setText('Let’s Beer Sour Milk Soda')
        self.layoutItem_data.setText('酒精度 0.0% ABV   苦度 0 IBU')
        self.layoutItem_price.setText('￥28')
        self.layoutItem_capacity.setText('杯型<br>330mL')

    def makeTapList(self):
        # get data

        # draw
        self.draw(targetLayout=self.layout0)
    
    def setSoldout(self, layoutname):
        layoutname.setStyleSheet("color: #373737;")

    def emptyTaplist(self):
        # remove all taplist detail layout
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
