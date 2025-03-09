from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import config as conf
import mqtt
import cryption

import sys
import pyttsx3
import requests as rq
import json

from ui_about import Ui_About
from ui_floatwindow import Ui_FloatWindow
from ui_send import Ui_Send

CONF_PATH = "./config.json"  # 配置文件路径
VERSION = "0.1.0"  # 当前程序版本


# 接收端
class CallYouAPP_R(QWidget, Ui_FloatWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setupUi(self)
        self.setup()

    # 初始化
    def setup(self):
        self.marginTop = 0  # 距离屏幕上方距离
        self.windowAlpha = 0.85  # 窗口透明度
        self.screenRect = QApplication.primaryScreen().geometry()
        self.animProcessing = None
        self.isShow = True

        self.nowMsg = ""

        # 设置图标和标题
        self.setWindowTitle("CallYou")
        self.setWindowIcon(QIcon("./img/CallYouIcon.png"))

        # 设置窗口样式
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 设置透明背景
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint  | Qt.WindowType.WindowStaysOnTopHint  | Qt.WindowType.Tool
        )  # 设置窗口置顶 + 无边框
        self.setShadow()
        self.moveWindowToTopAndSetAlpha()

        self.setupAnimation()

        # 创建系统托盘图标
        self.createSystemTrayIcon()

        self.aboutWindow = CallYouAbout()

        self.start()
    
    # 设置窗口阴影
    def setShadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(22)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.widget.setGraphicsEffect(shadow)

    # 调整大小、移动、设置透明度
    def moveWindowToTopAndSetAlpha(self):
        self.resize(self.screenRect.width(), 150)
        self.setMinimumWidth(self.screenRect.width())
        self.setMaximumWidth(self.screenRect.width())
        self.move(self.screenRect.width() // 2 - self.width() // 2, self.marginTop)
        self.setWindowOpacity(self.windowAlpha)

    # 初始化动画
    def setupAnimation(self):
        self.animHide = QPropertyAnimation(self, b"geometry")
        self.animHide.setDuration(500)
        self.animHide.setStartValue(
            QRect(
                self.screenRect.width() // 2 - self.width() // 2, self.marginTop,
                self.width(), self.height(),
            )
        )
        self.animHide.setEndValue(
            QRect(
                self.screenRect.width() // 2 - self.width() // 2, int(0 - self.height()),
                self.width(), self.height(),
            )
        )
        self.animHide.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animHide.finished.connect(self.animFinished)

        self.animShow = QPropertyAnimation(self, b"geometry")
        self.animShow.setDuration(500)
        self.animShow.setStartValue(
            QRect(
                self.screenRect.width() // 2 - self.width() // 2, int(0 - self.height()),
                self.width(), self.height(),
            )
        )
        self.animShow.setEndValue(
            QRect(
                self.screenRect.width() // 2 - self.width() // 2, self.marginTop,
                self.width(), self.height(),
            )
        )
        self.animShow.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animShow.finished.connect(self.animFinished)

        self.animRestTime = QPropertyAnimation(self.RestTimeProgressBar, b"value")
        self.animRestTime.setDuration(self.config["show"]["stay_time"])
        self.animRestTime.setStartValue(100000)
        self.animRestTime.setEndValue(0)
        self.animRestTime.finished.connect(self.hideWindow)

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

        self.QuitAction.triggered.connect(self.quitApp)
        self.AboutAction.triggered.connect(self.openAboutWindow)

        self.TrayIcon.show()

    def openAboutWindow(self):
        self.aboutWindow.show()

    def setMqtt(self):
        pass

    def quitApp(self):
        self.stopThread()
        sys.exit()

    # 开始运行
    def start(self):
        self.setupThread()

        self.mqttThread.start()

        self.show()
        self.hideWindow()

    def restart(self):
        self.stopThread()
        self.setupThread()

        self.mqttThread.start()

    def setupThread(self):
        self.mqttWorker = MqttClientWorker_R(self.config)
        self.mqttThread = QThread(self)
        self.mqttWorker.moveToThread(self.mqttThread)

        self.mqttWorker.s_on_connect.connect(self.onConnect)
        self.mqttWorker.s_on_receive.connect(self.onReceiveMessage)
        self.mqttWorker.s_on_disconnect.connect(self.onDisconnect)
        self.mqttThread.started.connect(self.mqttWorker.start)

    def stopThread(self):
        self.mqttWorker.mqttClient.loop_stop()
        self.mqttWorker.mqttClient.disconnect()
        self.mqttThread.exit()
        self.mqttWorker.deleteLater()
        self.mqttThread.deleteLater()

    def onReceiveMessage(self, msg):
        try:
            self.nowMsg = str(cryption.tkcudecrypt(msg, self.config["key"]))
        except Exception as e:
            print(f"ERROR: CAN'T DECRYPT MSG!\n{e}")
            self.showDialogBox(
                "消息错误",
                "无法解析新接收到的消息内容，请检查topic是否与相同服务器下其他用户重合或者检查配对的发送/接收端的秘钥是否一致！",
            )
        else:
            print(self.nowMsg)
            self.TextLabel.setText(self.nowMsg)
            # self.repaint()
            self.showWindow()

    def onConnect(self, rc):
        if rc == "0":
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code is {rc}")

    def onDisconnect(self):
        tmp = self.showDialogBox(
            "断开连接",
            "突然断开了链接！！！！\n点击 Yes 尝试重连，点击 No 退出程序。",
        )
        if tmp:
            self.restart()
        else:
            sys.exit()

    def showDialogBox(self, title: str, content: str):
        return QMessageBox.information(
            self, title, content,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )


class MqttClientWorker_R(QObject):
    s_on_receive = Signal(str)
    s_on_connect = Signal(str)
    s_on_disconnect = Signal()

    def __init__(self, config):
        super().__init__()
        self.config = config

    def start(self):
        self.setMqtt()

    def setMqtt(self):
        mqtt.broker = self.config["mqtt"]["broker"]
        mqtt.port = self.config["mqtt"]["port"]
        mqtt.topic = self.config["mqtt"]["topic"]
        mqtt.client_id = self.config["mqtt"]["client_id"]
        mqtt.username = self.config["mqtt"]["username"]
        mqtt.password = self.config["mqtt"]["password"]

        self.mqttClient = mqtt.connect_mqtt(self.onConnect)
        mqtt.subscribe(self.mqttClient, self.onReceive)
        self.mqttClient.on_disconnect = self.onDisconnect

        self.mqttClient.loop_forever()

    def onReceive(self, client, userdata, msg):
        self.s_on_receive.emit(msg.payload.decode())

    def onConnect(self, client, userdata, flags, rc):
        self.s_on_connect.emit(str(rc))

    def onDisconnect(self, userdata, flags, rc):
        print(f"Disconnected! rc: {rc}")
        if rc != 0:
            self.s_on_disconnect.emit()


class CallYouAPP_S(QWidget, Ui_Send):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.setWindowIcon(QIcon("./img/CallYouIcon.png"))

        self.aboutWindow = CallYouAbout()

        self.aboutPbtn.clicked.connect(self.aboutWindow.show)
        self.seniorEditorPbtn.clicked.connect(
            lambda: self.showMessageBox("提示", "高级编辑器仍在开发当中。")
        )
        self.sendPbtn.clicked.connect(self.sendMsg)

        self.createSystemTrayIcon()

        self.setMqtt()

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
            send_msg_content = cryption.tkcuencrypt(self.MessageEdit.text(), self.config["key"])
            status = mqtt.publish(
                self.mqttClient,
                send_msg_content
            )
            print(send_msg_content)
            # self.mqttClient.loop()
            self.showMessageBox(
                "提示", f"已发送内容，但不知道是否发送成功。\n返回值：{status}\nTips: 当返回值为0时即为发送成功！"
            )

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

    def showDialogBox(
        self, title: str, content: str, yesbt: str = "确定", ccbt: str = "取消"
    ):
        return QMessageBox.information(
            self,
            title,
            content,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

    def showMessageBox(
        self, title: str, content: str, yesbt: str = "确定", ccbt: str = "取消"
    ):
        return QMessageBox.information(
            self,
            title,
            content,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )


class CallYouAbout(QWidget, Ui_About):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.setWindowIcon(QIcon("./img/CallYouIcon.png"))
        self.setWindowTitle("关于 CallYou")

        self.pbtnHomePage.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://github.com/XLBlue1019/TKCallYou"))
        )
        self.pbtnAuthorWebsite.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://xlblue.bluetinker.cn"))
        )
        self.pbtnStudioWebsite.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://bluetinker.cn"))
        )

    def closeEvent(self, event):
        self.hide()
        event.ignore()


def check_update():
    data = json.loads(
        rq.get(
            "https://raw.githubusercontent.com/XLBlue1019/TKCallYou/main/version.json",
            verify=False,
        ).text
    )
    return data


def run():
    app = QApplication(sys.argv)

    try:
        check = check_update()

        if check["nowVersion"] != VERSION:
            w = QWidget()
            w.setWindowIcon(QIcon("./img/CallYouIcon.png"))
            msgBox = QMessageBox.information(
                w,
                "提示",
                f"""软件有新版本！是否前往下载？\n---\n如果有的话：\n提取码为：{check["psw1"]}\n解压密码为：{check["psw2"]}""",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if msgBox:
                QDesktopServices.openUrl(QUrl(check["downloadLink"]))
                sys.exit()
    except:
        w = QWidget()
        w.setWindowIcon(QIcon("./img/CallYouIcon.png"))
        msgBox = QMessageBox.critical(
            w,
            "错误",
            "软件无法检测更新！即将继续运行。\n可能的原因如下：\n1. Github Raw无法访问（大多数情况）\n2. 你暂未连接到互联网，这时候你很有可能也无法访问你设置的Mqtt服务器（内网除外）\n解决方案：\n1. 自行前往本项目主页（https://github.com/XLBlue1019/TKCallYou）手动更新\n2. 检查网络连接\n3. 克隆源代码，将main.py中的“raw.githubusercontent.com”改为其他Github Raw镜像站后自行打包",
            QMessageBox.StandardButton.Yes,
        )

    config = conf.load_json(CONF_PATH)

    if config["mode"] == "r":
        window = CallYouAPP_R(config)
    elif config["mode"] == "s":
        window = CallYouAPP_S(config)

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
