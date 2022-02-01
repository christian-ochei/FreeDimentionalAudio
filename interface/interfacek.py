import os

from PyQt5 import QtGui,QtCore
from win32api import GetSystemMetrics

from PyQt5.QtCore import QDir, Qt, QUrl

import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizeGrip,QGraphicsScene
from PyQt5.QtMultimediaWidgets import QVideoWidget,QGraphicsVideoItem
import sys
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
from BlurWindow.blurWindow import blur

import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.top = 200
        self.left = 500
        self.width = 852
        self.height = 480

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self._scene = QGraphicsScene(self)
        self._gv = QtWidgets.QGraphicsView(self._scene)

        self.setWindowFlags(flags)
        self.mediaPlayer = QMediaPlayer(None,QMediaPlayer.VideoSurface)
        self.videoWidget = QGraphicsVideoItem()

        wid = QWidget(self)
        self.setCentralWidget(wid)

        # self.layout.addWidget(QSizeGrip(None))
        # self.layout.addWidget(self.videoWidget)
        self._scene.addItem(self.videoWidget)
        self.layout.addWidget(self._gv)


        wid.setLayout(self.layout)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.setMedia(
            QMediaContent(QUrl.fromLocalFile("intro.wmv")))
        # self.mediaPlayer.error.emit(self.handleError)

        # sizegrip.setVisible(True)
        self.setLayout(self.layout)
        self.setAttribute(Qt.WA_TranslucentBackground)
        blur(self.winId())


        Window.borderless = True
        Window.size = GetSystemMetrics(0), GetSystemMetrics(1)
        Window.left = 0
        Window.top = 0

        self.show()

    def handleError(self):
        # self.playButton.setEnabled(False)
        self.error.setText("Error: " + self.mediaPlayer.errorString())

    def _begin(self):
        self.mediaPlayer.play()

#
if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    window._begin()
    sys.exit(App.exec())
#
#
# from PyQt5.QtWidgets import QApplication, QFileDialog
# from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
# from PyQt5.QtMultimediaWidgets import QVideoWidget
#
# if __name__ == '__main__':
#     app = QApplication([])
#     player = QMediaPlayer()
#     wgt_video = QVideoWidget()  # Video display widget
#     wgt_video.show()
#     player.setVideoOutput(wgt_video)  # widget for video output
#     player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # Select video file
#     player.play()
#     app.exec_()