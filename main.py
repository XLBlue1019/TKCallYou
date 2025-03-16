from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import config as conf
import mqtt as mqtt_
import cryption

import sys
import pyttsx3
import requests as rq
import json

from ui_about import Ui_About
from ui_floatwindow import Ui_FloatWindow
from ui_send import Ui_Send

CONF_PATH = "./config.json"  # 配置文件路径
VERSION = "0.2.0"  # 当前程序版本


class CallYouAPP(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("./img/CallYouIcon.png"))
        self.createSystemTrayIcon()
        self.aboutWindow = CallYouAbout()

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

    def quitApp(self):
        self.stopThread()
        sys.exit()

    def showDialogBox(self, title: str, content: str):
        return QMessageBox.information(
            self, title, content,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

# 接收端
class CallYouAPP_R(CallYouAPP, Ui_FloatWindow):
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

        # 设置窗口样式
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 设置透明背景
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint  | Qt.WindowType.WindowStaysOnTopHint  | Qt.WindowType.Tool
        )  # 设置窗口置顶 + 无边框
        self.setShadow()
        self.moveWindowToTopAndSetAlpha()

        self.setupAnimation()

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
        # 收起动画
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

        # 弹出动画
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

        # 进度条动画
        self.animRestTime = QPropertyAnimation(self.RestTimeProgressBar, b"value")
        self.animRestTime.setDuration(self.config["show"]["stay_time"])
        self.animRestTime.setStartValue(100000)
        self.animRestTime.setEndValue(0)
        self.animRestTime.finished.connect(self.hideWindow)

    # 收起窗口
    def hideWindow(self):
        self.animProcessing = "hide"
        self.animHide.start()

    # 弹出窗口
    def showWindow(self):
        self.show()
        self.animProcessing = "show"
        self.animShow.start()

    # 当动画播放完成后的操作
    def animFinished(self):
        if self.animProcessing == "hide":
            self.hide() # 隐藏窗口
        elif self.animProcessing == "show":
            # 语音通知
            pyttsx3.speak("通知！通知！" + self.nowMsg)
            self.animRestTime.start()
        self.animProcessing = None
        
    # 开始运行
    def start(self):
        self.setupThread()

        self.mqttThread.start()

        self.show()
        self.hideWindow()

    # 重启MQTT任务
    def restart(self):
        self.stopThread()
        self.setupThread()

        self.mqttThread.start()

    # 初始化QThread
    def setupThread(self):
        self.mqttWorker = MqttClientWorker_R(self.config)
        self.mqttThread = QThread(self)
        self.mqttWorker.moveToThread(self.mqttThread)

        self.mqttWorker.s_on_connect.connect(self.onConnect)
        self.mqttWorker.s_on_receive.connect(self.onReceiveMessage)
        self.mqttWorker.s_on_disconnect.connect(self.onDisconnect)
        self.mqttThread.started.connect(self.mqttWorker.start)

    # 停止QThread
    def stopThread(self):
        self.mqttWorker.mqttClient.loop_stop()
        self.mqttWorker.mqttClient.disconnect()
        self.mqttThread.exit()
        self.mqttWorker.deleteLater()
        self.mqttThread.deleteLater()

    # 弹出消息
    def showMsg(self, msg):
        print(msg)
        self.TextLabel.setText(msg)
        # self.repaint()
        self.showWindow()

    # 当收到消息时
    def onReceiveMessage(self, msg):
        try: # 尝试解密
            self.nowMsg = str(cryption.tkcudecrypt(msg, self.config["key"]))
        except Exception as e: # 解密失败
            print(f"ERROR: CAN'T DECRYPT MSG!\n{e}")
            self.showDialogBox(
                "消息错误",
                "无法解析新接收到的消息内容，请检查topic是否与相同服务器下其他用户重合或者检查配对的发送/接收端的秘钥是否一致！",
            )
        else: # 解密成功
            # 弹出消息
            self.showMsg(self.nowMsg)

    # 当连接上MQTT时
    def onConnect(self, rc):
        if rc == "0":
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code is {rc}")

    # 当断开MQTT时
    def onDisconnect(self):
        tmp = self.showDialogBox(
            "断开连接",
            "突然断开了链接！！！！\n点击 Yes 尝试重连，点击 No 退出程序。",
        )
        if tmp:
            self.restart()
        else:
            sys.exit()


# 接收端MQTT Worker
class MqttClientWorker_R(QObject):
    # 信号
    s_on_receive = Signal(str)
    s_on_connect = Signal(str)
    s_on_disconnect = Signal()

    def __init__(self, config):
        super().__init__()
        self.config = config

    def start(self):
        self.setMqtt()

    # 初始化MQTTClient
    def setMqtt(self):
        self.mqtt = mqtt_.MQTTClient()

        # 加载配置
        self.mqtt.broker = self.config["mqtt"]["broker"]
        self.mqtt.port = self.config["mqtt"]["port"]
        self.mqtt.topic = self.config["mqtt"]["topic"]
        self.mqtt.client_id = self.config["mqtt"]["client_id"]
        self.mqtt.username = self.config["mqtt"]["username"]
        self.mqtt.password = self.config["mqtt"]["password"]

        self.mqttClient = self.mqtt.connect_mqtt(self.onConnect)
        self.mqtt.subscribe(self.mqttClient, self.onReceive)
        self.mqttClient.on_disconnect = self.onDisconnect

        self.mqttClient.loop_forever()

    # 当收到对应信号时
    def onReceive(self, client, userdata, msg):
        self.s_on_receive.emit(msg.payload.decode())

    def onConnect(self, client, userdata, flags, rc):
        self.s_on_connect.emit(str(rc))

    def onDisconnect(self, userdata, flags, rc):
        print(f"Disconnected! rc: {rc}")
        if rc != 0:
            self.s_on_disconnect.emit()


# 发送端
class CallYouAPP_S(CallYouAPP, Ui_Send):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setupUi(self)
        self.setup()

    # 初始化
    def setup(self):
        self.aboutPbtn.clicked.connect(self.aboutWindow.show)
        self.seniorEditorPbtn.clicked.connect(
            lambda: self.showDialogBox("提示", "高级编辑器仍在开发当中。")
        )
        self.sendPbtn.clicked.connect(self.sendMsg)

        self.setMqtt()

    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
        self.show()

    def setMqtt(self):
        self.mqtt = mqtt_.MQTTClient()

        self.mqtt.broker = self.config["mqtt"]["broker"]
        self.mqtt.port = self.config["mqtt"]["port"]
        self.mqtt.topic = self.config["mqtt"]["topic"]
        self.mqtt.client_id = self.config["mqtt"]["client_id"]
        self.mqtt.username = self.config["mqtt"]["username"]
        self.mqtt.password = self.config["mqtt"]["password"]

        self.mqttClient = self.mqtt.connect_mqtt(self.onConnect)

        self.mqttClient.loop()

    # 发送消息
    def sendMsg(self):
        # 检测消息框是否为空
        if self.MessageEdit.text() == "":
            self.showDialogBox("提示", "你还没有填写发布内容！")
        else:
            send_msg_content = cryption.tkcuencrypt(self.MessageEdit.text(), self.config["key"]) # 加密信息
            status = self.mqtt.publish(
                self.mqttClient,
                send_msg_content
            )
            print(send_msg_content)
            # self.mqttClient.loop()
            self.showDialogBox(
                "提示", f"已发送内容，但不知道是否发送成功。\n返回值：{status}\nTips: 当返回值为0时即为发送成功！"
            )


# 关于
class CallYouAbout(QWidget, Ui_About):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.setWindowIcon(QIcon("./img/CallYouIcon.png"))
        self.setWindowTitle("关于 CallYou")

        # 绑定按钮至相应链接
        self.pbtnHomePage.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://github.com/XLBlue1019/TKCallYou"))
        )
        self.pbtnAuthorWebsite.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://xlblue.bluetinker.cn"))
        )
        self.pbtnStudioWebsite.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://bluetinker.cn"))
        )

    # 避免销毁窗口
    def closeEvent(self, event):
        self.hide()
        event.ignore()


# 检查更新
def check_update():
    data = json.loads(
        rq.get(
            "https://raw.githubusercontent.com/XLBlue1019/TKCallYou/main/version.json", # version.json中的url
            verify=False, # 避免某些情况下的连接失败
        ).text
    )
    return data


# 程序主函数
def run():
    app = QApplication(sys.argv)

    # 尝试检测更新
    try:
        check = check_update()

        # 如果有新版本，则弹出升级提示
        if check["nowVersion"] != VERSION:
            w = QWidget()
            w.setWindowIcon(QIcon("./img/CallYouIcon.png"))
            msgBox = QMessageBox.information(
                w,
                "提示",
                f"""软件有新版本！是否前往下载？
------
如果有的话：
提取码为：{check["psw1"]}
解压密码为：{check["psw2"]}""",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if msgBox:
                QDesktopServices.openUrl(QUrl(check["downloadLink"]))
                sys.exit()
    except:
        # 失败后，弹窗提示
        w = QWidget()
        w.setWindowIcon(QIcon("./img/CallYouIcon.png"))
        msgBox = QMessageBox.critical(
            w,
            "错误",
            """软件无法检测更新！即将继续运行。
可能的原因如下：
    1. Github Raw无法访问（大多数情况）
    2. 你暂未连接到互联网，这时候你很有可能也无法访问你设置的Mqtt服务器（内网除外）
解决方案：
    1. 自行前往本项目主页（https://github.com/XLBlue1019/TKCallYou）手动更新
    2. 检查网络连接\n3. 克隆源代码，将main.py中的“raw.githubusercontent.com”改为其他Github Raw镜像站后自行打包""",
            QMessageBox.StandardButton.Yes,
        )

    # 加载配置
    config = conf.load_json(CONF_PATH)

    # 判断对应模式并实例化对应窗口
    if config["mode"] == "r":
        window = CallYouAPP_R(config)
    elif config["mode"] == "s":
        window = CallYouAPP_S(config)
    else: # 若设置的模式错误
        w = QWidget()
        w.setWindowIcon(QIcon("./img/CallYouIcon.png"))
        msgBox = QMessageBox.critical(
            w,
            "错误",
            "",
            QMessageBox.StandardButton.Yes,
        )

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
