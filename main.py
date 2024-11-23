from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys

from qframelesswindow import FramelessWindow, StandardTitleBar
from qfluentwidgets import *

import config
import mqtt
import cryption

import pyttsx3
import requests as rq
import os

from ui_about import Ui_About
from ui_floatwindow import Ui_FloatWindow
from ui_send import Ui_Send

CONF_PATH = ".\config.json" # 配置文件路径
VERSION = "1.0.0"


class CallYouAPP_R(QWidget, Ui_FloatWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()

    
    def setup(self):
        self.marginTop = 0 # 距离屏幕上方距离
        self.windowAlpha = 0.85 # 窗口透明度
        self.screenRect = QApplication.primaryScreen().geometry()
        self.animProcessing = None
        self.isShow = True

        self.nowMsg = ""

        self.fontUsed = [
            "阿里巴巴普惠体 3.0 55 Regular", 
            "阿里巴巴普惠体 3.0 75 SemiBold", 
            "阿里巴巴普惠体 3.0 95 ExtraBold",
        ]

        self.loadConf()

        self.animHide = QPropertyAnimation(self, b"geometry")
        self.animHide.setDuration(500)
        self.animHide.setStartValue(QRect(self.screenRect.width()//2 - self.width()//2, self.marginTop, self.width(), self.height()))
        self.animHide.setEndValue(QRect(self.screenRect.width()//2 - self.width()//2, int(0-self.height()), self.width(), self.height()))
        self.animHide.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animHide.finished.connect(self.animFinished)
        
        self.animShow = QPropertyAnimation(self, b"geometry")
        self.animShow.setDuration(500)
        self.animShow.setStartValue(QRect(self.screenRect.width()//2 - self.width()//2, int(0-self.height()), self.width(), self.height()))
        self.animShow.setEndValue(QRect(self.screenRect.width()//2 - self.width()//2, self.marginTop, self.width(), self.height()))
        self.animShow.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animShow.finished.connect(self.animFinished)

        self.animRestTime = QPropertyAnimation(self.RestTimeProgressBar, b"value")
        self.animRestTime.setDuration(self.config["show"]["stay_time"])
        self.animRestTime.setStartValue(100000)
        self.animRestTime.setEndValue(0)
        self.animRestTime.finished.connect(self.hideWindow)

        self.setWindowTitle("ClassIsland")
        self.setWindowIcon(QIcon("./img/CallYouIcon.png"))

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # 设置透明背景
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool) # 设置窗口置顶 + 无边框

        self.setShadow()
        self.moveWindowToTopAndSetAlpha()
        self.createSystemTrayIcon()

        # self.setMqtt()

        self.aboutWindow = CallYouAbout()
        
        self.systemCheck()

        # self.show()
        # self.hideWindow()


    def systemCheck(self):
        for i in self.fontUsed:
            if not i in QFontDatabase.families():
                r = self.showDialogBox("提示", "由于您的计算机没有安装需要的字体（阿里巴巴普惠体 3.0），导致无法运行本程序，点击 确定 将前往 阿里巴巴普惠体官网 进行下载。")
                if r:
                    QDesktopServices.openUrl(QUrl("https://www.alibabafonts.com/#/font"))
                sys.exit()
        
        if self.screenRect.width() / self.screenRect.height() != 16 / 9:
            print(self.screenRect.width(), self.screenRect.height(), 16 / 9)
            r = self.showDialogBox("提示", "由于您的计算机显示器长宽比不为16:9，在部分情况下，本软件可能无法达到预期的效果。", "退出程序", "继续运行")
            if r:
                sys.exit()

        self.setMqtt()
        self.show()
        self.hideWindow()


    def setShadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(22)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.widget.setGraphicsEffect(shadow)


    def moveWindowToTopAndSetAlpha(self):
        self.move(self.screenRect.width()//2 - self.width()//2, self.marginTop)
        self.setWindowOpacity(self.windowAlpha)


    def hideWindow(self):
        self.animProcessing = "hide"
        self.animHide.start()


    def showWindow(self):
        self.show()
        self.animProcessing = "show"
        self.animShow.start()


    def animFinished(self):
        if self.animProcessing == "hide":
            self.hide()
        elif self.animProcessing == "show":
            pyttsx3.speak("通知！通知！" + self.nowMsg)
            self.animRestTime.start()
        self.animProcessing = None


    def createSystemTrayIcon(self):
        self.QuitAction = QAction("退出", self)
        self.AboutAction = QAction("关于", self)

        self.TrayMenu = QMenu(self)
        self.TrayMenu.addAction(self.AboutAction)
        self.TrayMenu.addSeparator()
        self.TrayMenu.addAction(self.QuitAction)

        self.TrayIcon = QSystemTrayIcon(self)
        self.TrayIcon.setContextMenu(self.TrayMenu)
        self.TrayIcon.setIcon(QIcon("./img/CallYouIcon.png"))

        self.QuitAction.triggered.connect(sys.exit)
        self.AboutAction.triggered.connect(self.openAboutWindow)

        self.TrayIcon.show()


    def openAboutWindow(self):
        self.aboutWindow.show()


    def loadConf(self):
        self.config = config.load_json(CONF_PATH)


    def setMqtt(self):
        mqtt.broker = self.config["mqtt"]["broker"]
        mqtt.port = self.config["mqtt"]["port"]
        mqtt.topic = self.config["mqtt"]["topic"]
        mqtt.client_id = self.config["mqtt"]["client_id"]
        mqtt.username = self.config["mqtt"]["username"]
        mqtt.password = self.config["mqtt"]["password"]

        self.mqttClient = mqtt.connect_mqtt(self.onConnect)

        mqtt.subscribe(self.mqttClient, self.onReceiveMessage)

        self.mqttLoop()

    
    def mqttLoop(self):
        self.mqttClient.loop()

        self.mqttTimer = QTimer()
        self.mqttTimer.start(self.config["performance"]["refresh_time"])
        self.mqttTimer.timeout.connect(self.mqttLoop)


    def onReceiveMessage(self, client, userdata, msg):
        self.nowMsg = cryption.tkcudecrypt(msg.payload.decode(), self.config["key"])

        print(self.nowMsg)
        self.TextLabel.setText(self.nowMsg)
        self.showWindow()

        # self.showTimer = QTimer()
        # self.showTimer.start(self.config["show"]["stay_time"])
        # self.showTimer.timeout.connect(self.hideWindow)


    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)


    def showDialogBox(self, title: str, content: str, yesbt: str = "确定", ccbt: str = "取消"):
        w = Dialog(title, content, self)
        w.yesButton.setText(yesbt)
        w.cancelButton.setText(ccbt)
        w.setTitleBarVisible(False)
        w.setContentCopyable(True)
        if w.exec():
            return True
        else:
            return False
        


class CallYouAPP_S(FramelessWindow, Ui_Send):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()


    def setup(self):
        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.raise_()

        self.setWindowIcon(QIcon("./img/CallYouIcon.png"))

        self.aboutWindow = CallYouAbout()

        self.aboutPbtn.setIcon(FluentIcon.INFO)
        self.aboutPbtn.setText("")

        self.aboutPbtn.clicked.connect(self.aboutWindow.show)
        self.seniorEditorPbtn.clicked.connect(lambda: self.showMessageBox("提示", "高级编辑器仍在开发当中。"))
        self.sendPbtn.clicked.connect(self.sendMsg)

        self.fontUsed = [
            "阿里巴巴普惠体 3.0 55 Regular", 
            "阿里巴巴普惠体 3.0 75 SemiBold", 
            "阿里巴巴普惠体 3.0 95 ExtraBold",
        ]

        self.loadConf()
        self.createSystemTrayIcon()

        self.systemCheck()


    def systemCheck(self):
        for i in self.fontUsed:
            if not i in QFontDatabase.families():
                r = self.showDialogBox("提示", "由于您的计算机没有安装需要的字体（阿里巴巴普惠体 3.0），导致无法运行本程序，点击 确定 将前往 阿里巴巴普惠体官网 进行下载。")
                if r:
                    QDesktopServices.openUrl(QUrl("https://www.alibabafonts.com/#/font"))
                sys.exit()

        self.setMqtt()


    def loadConf(self):
        self.config = config.load_json(CONF_PATH)


    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
        self.show()


    def setMqtt(self):
        mqtt.broker = self.config["mqtt"]["broker"]
        mqtt.port = self.config["mqtt"]["port"]
        mqtt.topic = self.config["mqtt"]["topic"]
        mqtt.client_id = self.config["mqtt"]["client_id"]
        mqtt.username = self.config["mqtt"]["username"]
        mqtt.password = self.config["mqtt"]["password"]

        self.mqttClient = mqtt.connect_mqtt(self.onConnect)

        self.mqttClient.loop()


    def sendMsg(self):
        if self.MessageEdit.text() == "":
            self.showMessageBox("提示", "你还没有填写发布内容！")
        else:
            status = mqtt.publish(self.mqttClient, cryption.tkcuencrypt(self.MessageEdit.text(), self.config["key"]))
            # self.mqttClient.loop()
            self.showMessageBox("提示", f"已发送内容，但不知道是否发送成功。\n返回值：{status}")


    def createSystemTrayIcon(self):
        self.QuitAction = QAction("退出", self)
        self.AboutAction = QAction("关于", self)

        self.TrayMenu = QMenu(self)
        self.TrayMenu.addAction(self.AboutAction)
        self.TrayMenu.addSeparator()
        self.TrayMenu.addAction(self.QuitAction)

        self.TrayIcon = QSystemTrayIcon(self)
        self.TrayIcon.setContextMenu(self.TrayMenu)
        self.TrayIcon.setIcon(QIcon("./img/CallYouIcon.png"))

        self.QuitAction.triggered.connect(sys.exit)
        self.AboutAction.triggered.connect(self.aboutWindow.show)

        self.TrayIcon.show()


    def showDialogBox(self, title: str, content: str, yesbt: str = "确定", ccbt: str = "取消"):
        w = Dialog(title, content, self)
        w.yesButton.setText(yesbt)
        w.cancelButton.setText(ccbt)
        w.setTitleBarVisible(False)
        w.setContentCopyable(True)
        if w.exec():
            return True
        else:
            return False
        

    def showMessageBox(self, title: str, content: str, yesbt: str = "确定", ccbt: str = "取消"):
        w = MessageBox(title, content, self)
        w.yesButton.setText(yesbt)
        w.cancelButton.setText(ccbt)
        w.setContentCopyable(True)
        if w.exec():
            return True
        else:
            return False



class CallYouAbout(FramelessWindow, Ui_About):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()


    def setup(self):
        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.raise_()

        self.setWindowIcon(QIcon("./img/CallYouIcon.png"))

        self.pbtnHomePage.released.connect(lambda: QDesktopServices.openUrl(QUrl("https://soft.bluetinker.cn")))
        self.pbtnAuthorWebsite.released.connect(lambda: QDesktopServices.openUrl(QUrl("https://xlblue.bluetinker.cn")))
        self.pbtnStudioWebsite.released.connect(lambda: QDesktopServices.openUrl(QUrl("https://bluetinker.cn")))


    def closeEvent(self, event):
        self.hide()
        event.ignore()



def check_update():
    data = json.loads(rq.get("https://soft.bluetinker.cn/cu/version.json").text)
    return data


def restart():
    try:
        os.system(os.path.realpath("./CallYou.exe"))
    except:
        pass
    sys.exit()


def run():
    app = QApplication(sys.argv)

    try:
        check = check_update()
    except:
        w = QWidget()
        try:
            w.setWindowIcon(QIcon("./img/CallYouIcon.png"))
        except:
            pass
        msgBox = QMessageBox.critical(w, "严重错误", "软件无法检测更新,将无法继续运行！即将重启软件。", QMessageBox.StandardButton.Yes)
        restart()
        sys.exit()

    if check["nowVersion"] == VERSION:
        try:
            if config.load_json(CONF_PATH)["mode"] == "r":
                Window = CallYouAPP_R()
            else:
                Window = CallYouAPP_S()

        except:
            w = QWidget()
            try:
                w.setWindowIcon(QIcon("./img/CallYouIcon.png"))
            except:
                pass
            msgBox = QMessageBox.critical(w, "严重错误", "软件无法继续运行，请联系软件开发者进行协助。即将重启程序。", QMessageBox.StandardButton.Yes)
            restart()
        sys.exit(app.exec())
    else:
        w = QWidget()
        try:
            w.setWindowIcon(QIcon("./img/CallYouIcon.png"))
        except:
            pass
        msgBox = QMessageBox.information(w, "提示", f'''软件有新版本！即将前往下载。\n如果有的话：\n提取码为：{check["psw1"]}\n解压密码为：{check["psw2"]}''', QMessageBox.StandardButton.Yes)
        QDesktopServices.openUrl(QUrl(check["downloadLink"]))
        sys.exit()


if __name__ == "__main__":
    run()