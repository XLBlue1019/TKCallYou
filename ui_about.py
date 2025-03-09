# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UI_About.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(512, 240)
        About.setMinimumSize(QSize(512, 240))
        About.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(About)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(About)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(About)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(About)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_3.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pbtnHomePage = QPushButton(About)
        self.pbtnHomePage.setObjectName(u"pbtnHomePage")

        self.horizontalLayout.addWidget(self.pbtnHomePage)

        self.pbtnAuthorWebsite = QPushButton(About)
        self.pbtnAuthorWebsite.setObjectName(u"pbtnAuthorWebsite")

        self.horizontalLayout.addWidget(self.pbtnAuthorWebsite)

        self.pbtnStudioWebsite = QPushButton(About)
        self.pbtnStudioWebsite.setObjectName(u"pbtnStudioWebsite")

        self.horizontalLayout.addWidget(self.pbtnStudioWebsite)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(About)

        QMetaObject.connectSlotsByName(About)
    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle("")
        self.label.setText(QCoreApplication.translate("About", u"\u5173\u4e8e About", None))
        self.label_2.setText(QCoreApplication.translate("About", u"CallYou! V0.2.0 By XLBlue", None))
        self.label_3.setText(QCoreApplication.translate("About", u"\u672c\u9879\u76ee\u7531 \u53ee\u5f53\u5de5\u4f5c\u5ba4 \u5c0f\u84ddXLBlue \u57fa\u4e8e PySide6, paho-mqtt, pycryptodome \u7b49\u5e93\u8fdb\u884c\u5f00\u53d1\n"
"\u672c\u9879\u76ee\u57fa\u4e8e GPLv3 \u8bb8\u53ef\u8bc1 \u5f00\u6e90", None))
        self.pbtnHomePage.setText(QCoreApplication.translate("About", u"\u6b64\u9879\u76ee\u4e3b\u9875", None))
        self.pbtnAuthorWebsite.setText(QCoreApplication.translate("About", u"\u5c0f\u84ddXLBlue \u7684\u7f51\u7ad9", None))
        self.pbtnStudioWebsite.setText(QCoreApplication.translate("About", u"\u53ee\u5f53\u5de5\u4f5c\u5ba4 \u7684\u7f51\u7ad9", None))
    # retranslateUi

