import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWebEngineWidgets import *
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
)
import pandas as pd
import os.path as osp
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import numpy as np


SENT = "sentiment"
CAT = "category"
UNLABELED = "emptystring"


class MainApp(QMainWindow):
    """This is the class of the MainApp GUI system"""
    def __init__(self):
        """Constructor method that inherits methods from QWidgets"""
        super().__init__()
        self.initUI()
        self.df = pd.read_csv(osp.join("data","scraped","1500_tweets.tsv"), sep="\t")
        self.pbar = None
        self.curidx = 0

    def initUI(self):
        """This method creates our GUI"""
        centralwidget = QWidget()
        self.setCentralWidget(centralwidget)
        self.lay = QVBoxLayout(centralwidget)

        # login
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name:')
        self.line = QLineEdit(self)
        self.loginbutton = QPushButton('login', self)
        self.loginbutton.clicked.connect(self.login)
        self.lay.addWidget(self.nameLabel)
        self.lay.addWidget(self.line)
        self.lay.addWidget(self.loginbutton)

        # Box Layout to organize our GUI
        # labels
        self.w=QWebEngineView()
        self.w.load(QtCore.QUrl('https://twitter.com/HeikoEnderling/status/1458135119408025607')) ## load google on startup
        self.w.showMaximized()
        self.lay.addWidget(self.w)

        self.l1 = QLabel()
        # myFont = QtGui.QFont()
        # myFont.setWeight(24)
        # myFont.setBold(True)
        self.l1.setFont(QFont('Arial', 22))
        self.l1.setText("Hello World!")
        self.l1.setAlignment(Qt.AlignCenter)
        self.lay.addWidget(self.l1)

        radiobuttons = QWidget()
        self.rblay = QHBoxLayout(radiobuttons)
        self.b1 = QRadioButton("Negative")
        self.b2 = QRadioButton("Neutral")
        self.b3 = QRadioButton("Positive")
        self.rblay.addWidget(self.b1)
        self.rblay.addWidget(self.b2)
        self.rblay.addWidget(self.b3)
        self.lay.addWidget(radiobuttons)


        buttons = QWidget()
        blay = QHBoxLayout(buttons)
        labels = ["Informative posts", "Informative questions", "Jokes and sarcasm", "Critique and opinions", "Compassion and sentiment", "Remove"]
        for label in labels:
            button = QtWidgets.QPushButton(label, self)
            button.clicked.connect(self.button_clicked)
            button.setObjectName(label)
            blay.addWidget(button)
        self.lay.addWidget(buttons)

        self.lay.addWidget(buttons)

        self.setGeometry(50, 50, 1800, 1200)
        self.setFixedSize(self.size())
        self.setWindowTitle('MainApp')
        self.setWindowIcon(QIcon('image/logo.png'))
        self.show()


    def button_clicked(self):
        self.w.load(QtCore.QUrl('https://google.com'))

        for b in [self.b1, self.b2, self.b3]:
            if b.isChecked():
                self.df.at[self.curidx, SENT] = b.text()
                print(b.text())

        self.b2.setChecked(True)

        self.df.at[self.curidx, CAT] = str(self.sender().objectName())
        print(self.df.at[self.curidx, CAT])
        self.curidx = np.min(np.where(self.df[CAT] == UNLABELED))
        print(self.curidx)
        self.w.load(QtCore.QUrl(self.df.iloc[self.curidx]["url"]))
        self.l1.setText(self.df.iloc[self.curidx]["text"])
        self.pbar.setValue(int((self.df[CAT] != UNLABELED).sum() / len(self.df)*100))

        self.df.to_csv(osp.join("data","scraped",f"annotated-{self.line.text()}.tsv"), sep="\t", index=False)


    def login(self):
        existing_filename = osp.join("data","scraped",f"annotated-{self.line.text()}.tsv")
        if osp.isfile(existing_filename):
            print('hey I found a file')
            self.df = pd.read_csv(existing_filename, sep="\t")

            print("Welcome back!")
        else:
            self.df[SENT] = UNLABELED
            self.df[CAT] = UNLABELED

        if self.pbar is None:
            self.pbar = QProgressBar(self)
            self.pbar.setValue(int((self.df[SENT] != UNLABELED).sum() / len(self.df)))
            self.lay.addWidget(self.pbar)

        print(self.df.head())
        self.curidx = np.min(np.where(self.df[SENT] == UNLABELED))
        self.w.load(QtCore.QUrl(self.df.iloc[self.curidx]["url"]))
        self.l1.setText(self.df.iloc[self.curidx]["text"])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainApp()
    sys.exit(app.exec_())
