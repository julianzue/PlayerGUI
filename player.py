import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QListWidget, QSlider, QLabel
from PyQt5.QtCore import Qt, QTimer
import os
import vlc

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()



    def open_url(self):

        self.list.clear()

        self.files = []

        for file in os.scandir(self.url.text()):
            self.files.append(file.name)

        self.files.sort()

        for f in self.files:
            self.list.addItem(f)
        
    def play_song(self):

        self.timer.start(1000)

        try:
            if self.player.is_playing():
                self.player.stop()
        except Exception:
            pass

        path = self.url.text() + self.list.currentItem().text()

        self.player = vlc.MediaPlayer(path)

        self.player.play()

        self.title.setText(self.list.currentItem().text())

    def stop_song(self):
        try:
            if self.player.is_playing():
                self.player.stop()
        except Exception:
            pass

    def seek_slider(self):
        percent = int(self.player.get_time() / self.player.get_length() * 100)
        self.seek.setValue(percent)

    def scroll_to(self):
        self.seek.value()

        song_value = int(self.player.get_length() * self.seek.value() / 100)

        self.player.set_time(song_value)

    def open_folder(self):

        new_path = self.url.text() + self.list.currentItem().text() + "/"

        self.url.setText(new_path)
        self.open_url()

    def back(self):

        split = self.url.text().split("/")

        new_path = "/".join(split[:(len(split) - 2)])

        self.url.setText(new_path + "/")
        self.open_url()
        
    def initUI(self):
        
        self.setGeometry(300, 300, 800, 620)
        self.setWindowTitle('Music Player')
        self.setFixedSize(800,620)
        self.setStyleSheet("QWidget {background: black}")

        self.url = QLineEdit(self)
        self.url.move(20,20)
        self.url.resize(600, 30)
        self.url.setStyleSheet("QLineEdit { padding: 5px; background: white; border: none; color: black; }")
        self.url.setText("/home/julian/Music/")

        self.url_btn = QPushButton(self)
        self.url_btn.move(640, 20)
        self.url_btn.resize(140, 30)
        self.url_btn.setStyleSheet("QPushButton { padding: 5px; background: darkorange; border: none; color: black; }")
        self.url_btn.setText("Open")
        self.url_btn.clicked.connect(self.open_url)

        self.list = QListWidget(self)
        self.list.move(20, 70)
        self.list.resize(760, 400)
        self.list.setStyleSheet("QListWidget { background: white; border: none; color: black; } QListWidget::item:selected { background: darkorange; color: black; } QListWidget::item{  padding: 5px; }")

        self.play = QPushButton(self)
        self.play.move(20, 490)
        self.play.resize(140, 30)
        self.play.setStyleSheet("QPushButton { padding: 5px; background: lime; border: none; color: black; }")
        self.play.setText("Play")
        self.play.clicked.connect(self.play_song)

        self.stop = QPushButton(self)
        self.stop.move(180, 490)
        self.stop.resize(140, 30)
        self.stop.setStyleSheet("QPushButton { padding: 5px; background: darkorange; border: none; color: black; }")
        self.stop.setText("Stop")
        self.stop.clicked.connect(self.stop_song)

        self.folder = QPushButton(self)
        self.folder.move(340, 490)
        self.folder.resize(140, 30)
        self.folder.setStyleSheet("QPushButton { padding: 5px; background: darkorange; border: none; color: black; }")
        self.folder.setText("Open Folder")
        self.folder.clicked.connect(self.open_folder)

        self.back_btn = QPushButton(self)
        self.back_btn.move(500, 490)
        self.back_btn.resize(140, 30)
        self.back_btn.setStyleSheet("QPushButton { padding: 5px; background: darkorange; border: none; color: black; }")
        self.back_btn.setText("Folder Up")
        self.back_btn.clicked.connect(self.back)

        self.exit = QPushButton(self)
        self.exit.move(660, 490)
        self.exit.resize(120, 30)
        self.exit.setStyleSheet("QPushButton { padding: 5px; background: red; border: none; color: black; }")
        self.exit.setText("Close")
        self.exit.clicked.connect(lambda: quit())

        self.seek = QSlider(Qt.Horizontal, self)
        self.seek.move(20, 540)
        self.seek.resize(760, 10)
        self.seek.setStyleSheet("QSlider { background: white; } QSlider::groove:horizontal { border: 1px solid dakrorange; height: 10px; } QSlider::handle:horizontal { background: darkorange; width: 10px; height: 10px; }")
        self.seek.sliderMoved.connect(self.scroll_to)

        self.title = QLabel(self)
        self.title.move(20, 570)
        self.title.resize(760, 30)
        self.title.setStyleSheet("QLabel { color: white; font-size: 15px; }")
        self.title.setText("--")

        self.timer = QTimer()
        self.timer.timeout.connect(self.seek_slider)

        self.open_url()
        self.show()
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
