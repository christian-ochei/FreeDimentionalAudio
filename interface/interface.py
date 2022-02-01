import os
from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

App = QApplication(sys.argv)

"""
TODO: random crashing
"""


class Draggable(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.setStyleSheet("background-color: #ccc")
        self.setMinimumHeight(30)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.parent.press_control == 0:
                self.pos = e.pos()
                self.main_pos = self.parent.pos()
        super().mousePressEvent(e)
    def mouseMoveEvent(self, e):
        if self.parent.cursor().shape() == Qt.ArrowCursor:
            self.last_pos = e.pos() - self.pos
            self.main_pos += self.last_pos
            self.parent.move(self.main_pos)
        super(Draggable, self).mouseMoveEvent(e)

class IntroVideo(QWidget):
    def __init__(self):
        super().__init__()
        self.top = 200
        self.left = 500
        self.width = 852
        self.height = 480
        self.setGeometry(self.left, self.top, self.width, self.height)
        # self.setWindowIcon(QtGui.QIcon('interface/icons/FreeViewAudio.png'))
        # assert os.path.exists('interface/icons/FreeViewAudio.png'),'Cannot find Icon file'
        # self.setWindowIcon(QtGui.QIcon('interface/icons/FreeViewAudio.png'))


        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.mediaPlayer = QMediaPlayer(None,QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()

        wid = QWidget(self)
        # self.setCentralWidget(wid)
        self.layout.addWidget(self.videoWidget)

        self.videoWidget.layout()
        # self.videoWidget.mouseDoubleClickEvent(QtGui.QMouseEvent())
        wid.setLayout(self.layout)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        # assert os.path.exists("interface/intro.wmv"), 'intro video was not found in ("interface/intro.wmv")'
        self.mediaPlayer.setMedia(
            QMediaContent(QUrl.fromLocalFile("interface/intro.wmv")))
        self.mediaPlayer.mediaStatusChanged.connect(self.statusChanged)
        # self.mediaPlayer.mo(self.statusChanged)
        self.setLayout(self.layout)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Window.borderless = True
        # Window.size = GetSystemMetrics(0), GetSystemMetrics(1)
        # Window.left = 0
        # Window.top = 0
        self.center()
        self.show()

    def statusChanged(self, status):
        print(status)
        if status == QMediaPlayer.EndOfMedia:
            App.CloseAllWindows()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def handleError(self):
        # self.playButton.setEnabled(False)
        self.error.setText("Error: " + self.mediaPlayer.errorString())

    def _begin(self):
        self.mediaPlayer.play()
#
if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = IntroVideo()
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