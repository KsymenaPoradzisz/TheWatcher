#Authors: Ksymena Poradzisz, Maciej Kucab


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStyle, QSlider, QFileDialog, QStyle
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys 
import os

class Window(QWidget): #creating a window for video player - QWidget is parent class and Window is class which inherit from it
	def __init__(self):
		super().__init__() #super allows easier heritance, we derive initializator from parent class
		self.filename = None
		self.setWindowIcon(QIcon("CD.png")) #Ikonka programu 
		self.setWindowTitle("The Watcher") #title of window of application
		self.setGeometry(350, 100, 700, 500) # wymiary okienka, window dimensions (?), 
		#czy da sie sprawdzic rozdzielczosc komputera i ustawic to zgodnie z jego rozdzielczoscia?
		self.create_player()
		self.path = os.path.dirname(os.path.abspath(__file__))
	
	def create_player(self):
		self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
		
		videowidget = QVideoWidget()
		
		#create open button
		self.openBtn = QPushButton('Open Video')
		self.openBtn.clicked.connect(self.open_file)
		
		self.playBtn = QPushButton()
		self.playBtn.setEnabled(False)
		self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
		self.playBtn.clicked.connect(self.play_video)
		
		self.nextBtn = QPushButton()
		self.nextBtn.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
		self.nextBtn.clicked.connect(self.next_file)
		
		self.previousBtn = QPushButton()
		self.previousBtn.setIcon(self.style().standardIcon(QStyle.SP_ArrowBack))
		self.previousBtn.clicked.connect(self.prev_file)
		
		self.slider = QSlider(Qt.Orientation.Horizontal) #czas trwania filmiku, przesuwak, nie wiem
		self.slider.setRange(0,0)
		self.slider.sliderMoved.connect(self.set_position)
		
		#QHBoxLayout - uklad horizontal
		hbox = QHBoxLayout()
		hbox.setContentsMargins(0,0,0,0)
		hbox.addWidget(self.openBtn) # adding button to our window app in horizontal manner
		hbox.addWidget(self.previousBtn)
		hbox.addWidget(self.playBtn)
		hbox.addWidget(self.nextBtn)
		hbox.addWidget(self.slider)
		
		vbox = QVBoxLayout()
		vbox.addWidget(videowidget)
		vbox.addLayout(hbox)
		
		self.mediaPlayer.setVideoOutput(videowidget)
		
		self.setLayout(vbox)
		
		self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
		self.mediaPlayer.positionChanged.connect(self.position_changed)
		self.mediaPlayer.durationChanged.connect(self.duration_changed)
		
	def open_file(self):
		self.filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
		if self.filename != '':
			self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.filename)))
			self.playBtn.setEnabled(True)
			video_name = self.filename.split("/")[-1] #creates list of a name and takes the last part
			self.setWindowTitle(f"{video_name}") #fstring
		next_ep_path = self.create_next_path(self.filename)
		prev_ep_path = self.create_previous_path(self.filename)
		if os.path.exists(prev_ep_path):
			self.previousBtn.setEnabled(True)
		else:
			self.previousBtn.setEnabled(False)
		if os.path.exists(next_ep_path):
			#open_file(next_ep)
			self.nextBtn.setEnabled(True)
		else:
			self.nextBtn.setEnabled(False)
		
	def open_video(self, path_to_video):
		if path_to_video:
			self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path_to_video)))
			self.playBtn.setEnabled(True)
			next_ep_path = self.create_next_path(self.filename)
			prev_ep_path = self.create_previous_path(self.filename)
			if os.path.exists(prev_ep_path):
				self.previousBtn.setEnabled(True)
			else:
				self.previousBtn.setEnabled(False)
			if os.path.exists(next_ep_path):
					#open_file(next_ep)
				self.nextBtn.setEnabled(True)
			else:
				self.nextBtn.setEnabled(False)
		
	def create_next_path(self,file_name):
		video_name = file_name.split("/")[-1] 
		ep_number = video_name.split("-")[-1]
		ep_number = ep_number.split(".")[0]
		series_name = "-".join(video_name.split("-")[:-1])
		next_ep_number = str(int(ep_number)+1)
		next_ep = series_name + "-" + next_ep_number + ".mp4"
		next_ep_path = os.path.join(self.path,"TVseries", series_name, next_ep)
		return next_ep_path
	def create_previous_path(self, file_name):
		video_name = file_name.split("/")[-1]
		ep_number = video_name.split("-")[-1]
		ep_number = ep_number.split(".")[0]
		series_name = "-".join(video_name.split("-")[:-1])
		prev_ep_num = str(int(ep_number)-1)
		prev_ep = series_name + "-" + prev_ep_num + ".mp4"
		prev_ep_path = os.path.join(self.path, "TVseries", series_name, prev_ep)
		return prev_ep_path
	def next_file(self):
		self.filename= self.create_next_path(self.filename)
		self.open_video(self.filename)
		video_name = self.filename.split("/")[-1]
		self.setWindowTitle(f"{video_name}")
		self.mediaPlayer.play()
	def prev_file(self):
		self.filename = self.create_previous_path(self.filename)
		self.open_video(self.filename)
		video_name = self.filename.split("/")[-1]
		self.setWindowTitle(f"{video_name}")
		self.mediaPlayer.play()
		
	def play_video(self):
		if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
			self.mediaPlayer.pause()
		else:
			self.mediaPlayer.play()
	
	def mediastate_changed(self,state):
		if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
			self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
		else:
			self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
	def position_changed(self, position):
		self.slider.setValue(position)
	def duration_changed(self, duration):
		self.slider.setRange(0, duration)
	
	def set_position(self,position):
		self.mediaPlayer.setPosition(position)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())	



#aby zrobic to jako aplikacje .exe to mozna wywolac komende:
#pyinstaller --onefile -windowed --icon=ikona.ico the_watcher.py
#ikona musi byc w 	forcmacie .ico
