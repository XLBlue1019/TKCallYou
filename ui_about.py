# Form implementation generated from reading ui file 'UI_About.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(512, 240)
        About.setMinimumSize(QtCore.QSize(360, 240))
        About.setMaximumSize(QtCore.QSize(512, 240))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(About)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(parent=About)
        self.frame.setMinimumSize(QtCore.QSize(494, 222))
        font = QtGui.QFont()
        font.setFamily("阿里巴巴普惠体 3.0 55 Regular")
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("阿里巴巴普惠体 3.0 95 ExtraBold")
        font.setPointSize(18)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("阿里巴巴普惠体 3.0 95 ExtraBold")
        font.setPointSize(12)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(parent=self.frame)
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbtnHomePage = PushButton(parent=self.frame)
        self.pbtnHomePage.setObjectName("pbtnHomePage")
        self.horizontalLayout.addWidget(self.pbtnHomePage)
        self.pbtnAuthorWebsite = PushButton(parent=self.frame)
        self.pbtnAuthorWebsite.setObjectName("pbtnAuthorWebsite")
        self.horizontalLayout.addWidget(self.pbtnAuthorWebsite)
        self.pbtnStudioWebsite = PushButton(parent=self.frame)
        self.pbtnStudioWebsite.setObjectName("pbtnStudioWebsite")
        self.horizontalLayout.addWidget(self.pbtnStudioWebsite)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addWidget(self.frame)

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "Form"))
        self.label.setText(_translate("About", "关于 About"))
        self.label_2.setText(_translate("About", "CallYou! V1.0.0 By XLBlue"))
        self.label_3.setText(_translate("About", "本项目由 叮当工作室 小蓝XLBlue 基于 PyQt6 和 PyQt6-Fluent-Widgets 组件库 进行开发\n"
"本项目基于 GPLv3 许可证 开源"))
        self.pbtnHomePage.setText(_translate("About", "此项目主页"))
        self.pbtnAuthorWebsite.setText(_translate("About", "小蓝XLBlue 的网站"))
        self.pbtnStudioWebsite.setText(_translate("About", "叮当工作室 的网站"))
from qfluentwidgets import PushButton
