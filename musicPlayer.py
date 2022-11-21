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
    # s = 1000
    # m = 60000
    # h = 360000
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

        self.buttAddToPlayer.clicked.connect(self.open_file)
        # self.music_play = QMediaPlayer()

        # self.playMusic.setPlaylist(self.favorite_list)


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
        # print(selection_model)
        selection_model.selectionChanged.connect(self.playlist_selection_changed)

        self.playMusic_fv = QMediaPlayer()

        self.favorite___list = QMediaPlaylist()
        self.playMusic_fv.setPlaylist(self.favorite___list)

        self.model_fv = PlaylistModel(self.favorite___list)
        self.favorite_list.setModel(self.model_fv)
        self.favorite___list.currentIndexChanged.connect(self.favorite_position_changed)
        selection_model_favorite = self.favorite_list.selectionModel()
        # print(selection_model_favorite)
        selection_model_favorite.selectionChanged.connect(self.favorite_selection_changed)
        # self.buttAdd_to_favorite_list.clicked.connect(self.playlit_add_to_favorite

        self.playMusic.durationChanged.connect(self.update_duration)
        self.playMusic.positionChanged.connect(self.update_position)
        self.mediaMusicRow.valueChanged.connect(self.playMusic.setPosition)




        self.buttDell_from_favorite_list.clicked.connect(self.delete_from_favorite_list)
        self.buttAdd_to_favorite_list.clicked.connect(self.add_to_favorite)
        self.buttDell_from_play_list.clicked.connect(self.delete_from_play_list)
        # self.play___list.connect(self.playMusic.save)
        # self.buttRandom.clicked.connect(self.randommm)

        self.butt_skin_1.clicked.connect(self.skin_1)
        self.butt_skin_2.clicked.connect(self.skin_2)
        self.butt_skin_3.clicked.connect(self.skin_3)

        self.checkBox.stateChanged.connect(self.clickBox)
        # if self.checkBox.isChecked() == True:
        #     self.test()
        # else:
        #     print(Falsex)
        self.openEvent()

        self.mediaTime.setButtonSymbols(2)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)
        self.show()



    # def randommm(self):
    #     self.play___list.setPlaybackMode(QMediaPlaylist.Random)

    def clickBox(self,state):
        if state == QtCore.Qt.Checked:
            self.play___list.setPlaybackMode(QMediaPlaylist.Random)
        else:
            self.play___list.setPlaybackMode(QMediaPlaylist.Loop)



    def timerEvent(self):
        self.mediaTime.setTime(self.mediaTime.time().addSecs(1))
        # print(self.mediaTime.time())

    

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
            # print(dataurl)
            # f.write(f"{dataurl}\n")
            f.write('%s;%s\n' % (dataurl,dataname))

            # f = open('music_list.txt','r')
            # print(f.read())
        f.close()


    # def random(self):
    #     s = self.play___list.mediaCount()
    #     r = randint(0,s)
    #     k = self.play___list.media(r)
    #     k.play()
    def update_duration(self, duration):
        self.mediaMusicRow.setMaximum(duration)

    def update_position(self, position):
        self.mediaMusicRow.blockSignals(True)
        self.mediaMusicRow.setValue(position)
        self.mediaMusicRow.blockSignals(False)

    def skin_1(self):
        print('1')

    def skin_2(self):
        self.buttPause.setStyleSheet('background-color : yellow;border-radius: 25px;')
        self.buttPlay.setStyleSheet('background-color : yellow')


    def skin_3(self):
        print('3')
    # def playlit_add_to_favorite(self):
    #     self.favorite_list.takeItem( self.play___list.media(index.row()))
    #     print('adsad')



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
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        self.play___list.setCurrentIndex(i)

    def playlist_position_changed(self, i):
        if i > -1:
            ix = self.model.index(i)
            self.play_list.setCurrentIndex(ix)    

    def favorite_selection_changed(self, ix):
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        self.favorite___list.setCurrentIndex(i)

    def favorite_position_changed(self, i):
        if i > -1:
            ix = self.model_fv.index(i)
            self.favorite_list.setCurrentIndex(ix)    


    def add_to_favorite(self):

        ss = self.play_list.selectedIndexes()
        # ss = 'C:/music_player/My_player/Honk.mp3'
        # print(ss)
        # print(dir(ss))
        for item in ss:
            # print(type(item))
            # print(dir(item))
            test= self.play___list.media(item.row()).canonicalUrl().toString().replace('file:///','')
            self.favorite___list.addMedia(QMediaContent(QUrl.fromLocalFile(test)))
            self.model_fv.layoutChanged.emit()

    #     self.model_fv = PlaylistModel(self.play___list)
    #     self.favorite_list.setModel(self.models)
    #     s = self.play_list.selectedIndexes()
    #     for y in s:
    #         # print((y.row()))
    #         self.favorite_list.setCurrentIndex(y)
        

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
    #     # print('okey')
        if path:
            print(path)
            self.play___list.addMedia(QMediaContent(QUrl.fromLocalFile(path)))
            # self.favorite___list.addMedia(QMediaContent(QUrl.fromLocalFile(path)))

            # self.play___list.addMedia(QMediaContent(QUrl.fromLocalFile(path)))


        self.model.layoutChanged.emit()
        # self.model_fv.layoutChanged.emit()

    # def toggle_viewer(self, state):
    #     if state:
    #         self.viewer.show()
    #     else:
    #         self.viewer.hide()

    # def erroralert(self, *args):
    #     print(args)


if __name__ == "__main__":
    app = QApplication([])
    app.setApplicationName("ssssssssssssssssssssssss")
    app.setStyle("Fusion")

    window = MainWindow()
    app.exec_()