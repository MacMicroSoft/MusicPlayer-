from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from mainWindow import Ui_Favorite_name
from PyQt5.QtCore import QTimer,QDateTime
from PyQt5.QtWidgets import QMainWindow, QLabel, QCheckBox, QWidget
from random import randint


def hhmmss(ms):
    s = round(ms / 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return ("%d:%02d:%02d" % (h, m, s)) if h else ("%d:%02d" % (m, s))



class PlaylistModel(QAbstractListModel):
    def __init__(self, play___list, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.play___list = play___list
    def data(self, index, role):
        if role == Qt.DisplayRole: 
            media = self.play___list.media(index.row())
            return media.canonicalUrl().fileName()

    def rowCount(self, index):
        return self.play___list.mediaCount()


class MainWindow(QMainWindow, Ui_Favorite_name):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowTitle('Music Player')
        self.window = QMainWindow()
        self.playMusic = QMediaPlayer()
        self.setFixedSize(550, 600)

        self.buttAddToPlayer.clicked.connect(self.open_file)


        self.play_list.doubleClicked.connect(self.play_list_play)
        self.favorite_list.doubleClicked.connect(self.play_favorite_play)

        self.play___list = QMediaPlaylist()
        self.playMusic.setPlaylist(self.play___list)

        self.model = PlaylistModel(self.play___list)

        self.buttPlay.clicked.connect(self.playMusic.play)
        self.buttPause.clicked.connect(self.playMusic.pause)
        self.buttStop.clicked.connect(self.playMusic.stop)
        self.mediaVolume.valueChanged.connect(self.playMusic.setVolume)
        self.buttReverse.clicked.connect(self.play___list.previous)
        self.buttForward.clicked.connect(self.play___list.next)


        self.play_list.setModel(self.model)
        self.play___list.currentIndexChanged.connect(self.playlist_position_changed)
        selection_model = self.play_list.selectionModel()
        selection_model.selectionChanged.connect(self.playlist_selection_changed)

        self.playMusic_fv = QMediaPlayer()

        self.favorite___list = QMediaPlaylist()
        self.playMusic_fv.setPlaylist(self.favorite___list)

        self.model_fv = PlaylistModel(self.favorite___list)
        self.favorite_list.setModel(self.model_fv)
        self.favorite___list.currentIndexChanged.connect(self.favorite_position_changed)
        selection_model_favorite = self.favorite_list.selectionModel()
        selection_model_favorite.selectionChanged.connect(self.favorite_selection_changed)

        self.playMusic.durationChanged.connect(self.update_duration)
        self.playMusic.positionChanged.connect(self.update_position)
        self.mediaMusicRow.valueChanged.connect(self.playMusic.setPosition)




        self.buttDell_from_favorite_list.clicked.connect(self.delete_from_favorite_list)
        self.buttAdd_to_favorite_list.clicked.connect(self.add_to_favorite)
        self.buttDell_from_play_list.clicked.connect(self.delete_from_play_list)

        self.butt_skin_1.clicked.connect(self.skin_1)
        self.butt_skin_2.clicked.connect(self.skin_2)
        self.butt_skin_3.clicked.connect(self.skin_3)
        self.butt_skin_4.clicked.connect(self.skin_4)
        self.checkBox.stateChanged.connect(self.clickBox)

        self.openEvent()

        self.mediaTime.setButtonSymbols(2)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)
        self.show()



    def clickBox(self,state):
        if state == QtCore.Qt.Checked:
            self.play___list.setPlaybackMode(QMediaPlaylist.Random)
        else:
            self.play___list.setPlaybackMode(QMediaPlaylist.Loop)



    def timerEvent(self):
        self.mediaTime.setTime(self.mediaTime.time().addSecs(1))
    

    def openEvent(self):
        with open("music_list.txt",'r') as data_file:
            for line in data_file:
                data = line.replace('\n','').split(';')
                print(data)
                self.play___list.addMedia(QMediaContent(QUrl.fromLocalFile(data[0])))


    def closeEvent(self, event):
        f = open('music_list.txt','w')
        for i in range(self.play___list.mediaCount()):
            t = self.play___list.media(i)
            dataurl = t.canonicalUrl().toString().replace('file:///','')
            dataname = t.canonicalUrl().fileName()
            f.write('%s;%s\n' % (dataurl,dataname))
        f.close()


    def update_duration(self, duration):
        self.mediaMusicRow.setMaximum(duration)

    def update_position(self, position):
        self.mediaMusicRow.blockSignals(True)
        self.mediaMusicRow.setValue(position)
        self.mediaMusicRow.blockSignals(False)

    def skin_1(self):
        self.buttPause.setStyleSheet('background-color : grey')
        self.buttPlay.setStyleSheet('background-color : grey')
        self.buttStop.setStyleSheet('background-color : grey')
        self.buttReverse.setStyleSheet('background-color : grey')
        self.buttForward.setStyleSheet('background-color : grey')
        self.buttAdd_to_favorite_list.setStyleSheet('background-color : grey')
        self.buttDell_from_play_list.setStyleSheet('background-color : grey')
        self.buttDell_from_favorite_list.setStyleSheet('background-color : grey')
        self.buttDell_from_play_list.setStyleSheet('background-color : grey')
        self.buttAddToPlayer.setStyleSheet('background-color : grey')


    def skin_2(self):
        self.buttPause.setStyleSheet('background-color : red')
        self.buttPlay.setStyleSheet('background-color : red')
        self.buttStop.setStyleSheet('background-color : red')
        self.buttReverse.setStyleSheet('background-color : red')
        self.buttForward.setStyleSheet('background-color : red')
        self.buttAdd_to_favorite_list.setStyleSheet('background-color : red')
        self.buttDell_from_play_list.setStyleSheet('background-color : red')
        self.buttDell_from_favorite_list.setStyleSheet('background-color : red')
        self.buttDell_from_play_list.setStyleSheet('background-color : red')
        self.buttAddToPlayer.setStyleSheet('background-color : red')


    def skin_3(self):
        self.buttPause.setStyleSheet('background-color : blue')
        self.buttPlay.setStyleSheet('background-color : blue')
        self.buttStop.setStyleSheet('background-color : blue')
        self.buttReverse.setStyleSheet('background-color : blue')
        self.buttForward.setStyleSheet('background-color : blue')
        self.buttAdd_to_favorite_list.setStyleSheet('background-color : blue')
        self.buttDell_from_play_list.setStyleSheet('background-color : blue')
        self.buttDell_from_favorite_list.setStyleSheet('background-color : blue')
        self.buttDell_from_play_list.setStyleSheet('background-color : blue')
        self.buttAddToPlayer.setStyleSheet('background-color : blue')


    def skin_4(self):
        self.buttPause.setStyleSheet('background-color : green')
        self.buttPlay.setStyleSheet('background-color : green')
        self.buttStop.setStyleSheet('background-color : green')
        self.buttReverse.setStyleSheet('background-color : green')
        self.buttForward.setStyleSheet('background-color : green')
        self.buttAdd_to_favorite_list.setStyleSheet('background-color : green')
        self.buttDell_from_play_list.setStyleSheet('background-color : green')
        self.buttDell_from_favorite_list.setStyleSheet('background-color : green')
        self.buttDell_from_play_list.setStyleSheet('background-color : green')
        self.buttAddToPlayer.setStyleSheet('background-color : green')


    def delete_from_favorite_list(self):
        s = self.favorite_list.selectedIndexes()
        for items in s:
            self.favorite___list.removeMedia(items.row())


    def delete_from_play_list(self):
        s = self.play_list.selectedIndexes()
        for item in s:
            print(dir(self.play___list.media(item.row())))
            print(self.play___list.media(item.row()).canonicalUrl())

            self.play___list.removeMedia(item.row())

    def playlist_selection_changed(self, ix):
        i = ix.indexes()[0].row()
        self.play___list.setCurrentIndex(i)

    def playlist_position_changed(self, i):
        if i > -1:
            ix = self.model.index(i)
            self.play_list.setCurrentIndex(ix)    

    def favorite_selection_changed(self, ix):
        i = ix.indexes()[0].row()
        self.favorite___list.setCurrentIndex(i)

    def favorite_position_changed(self, i):
        if i > -1:
            ix = self.model_fv.index(i)
            self.favorite_list.setCurrentIndex(ix)    


    def add_to_favorite(self):

        ss = self.play_list.selectedIndexes()
        for item in ss:
            test= self.play___list.media(item.row()).canonicalUrl().toString().replace('file:///','')
            self.favorite___list.addMedia(QMediaContent(QUrl.fromLocalFile(test)))
            self.model_fv.layoutChanged.emit()
        

    def play_list_play(self):
        self.playMusic_fv.stop()
        self.playMusic.play() 

    def play_favorite_play(self):
        self.playMusic.stop()
        self.playMusic_fv.play() 


    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "mp3 Audio (*.mp3);;mp4 Video (*.mp4);;Movie files (*.mov);;All files (*.*)",
        )
        if path:
            print(path)
            self.play___list.addMedia(QMediaContent(QUrl.fromLocalFile(path)))

        self.model.layoutChanged.emit()

if __name__ == "__main__":
    app = QApplication([])
    app.setApplicationName("Music_Player")
    app.setStyle("Fusion")

    window = MainWindow()
    app.exec_()
