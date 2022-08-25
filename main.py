from __future__ import print_function
import os
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
import pyaudio
import wave
import speech_recognition as sr
from googletrans import Translator
import soundcard as sc
import time


class MyNotification(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        # with this function You can Move Your Window by mouse dragging!
        def move_page(page):
            mxpos = 0
            mypos = 0

            def GetMousePosition():
                mouse_position = QCursor.pos()
                return mouse_position.x(), mouse_position.y()

            def first_sub(obj):
                geom = obj.geometry()
                x0 = geom.x()
                y0 = geom.y()
                w = geom.width()
                h = geom.height()

            def second_sub(*args, **kwargs):
                global mxpos
                global mypos
                mxpos, mypos = GetMousePosition()

            def third_sub(*args, **kwargs):
                global mxpos
                global mypos
                temp = page.frameGeometry()
                x0 = temp.x()
                y0 = temp.y()
                x, y = GetMousePosition()
                dx = x - mxpos
                dy = y - mypos
                mxpos = x
                mypos = y
                page.move(x0 + dx, y0 + dy)

            page.mousePressEvent = second_sub
            page.mouseMoveEvent = third_sub

        # < Styles >
        self.background_style_css = "background-color: rgba(22, 22, 22, 100); border-radius: 4px;"
        self.close_button_style_css = """
                                        QPushButton{
                                                    background-color: none;
                                                    color: white; border-radius: 6px;
                                                    font-size: 18px;
                                                    }
                                    """
        self.text_label_style_css = "color: white; font-size: 60px"
        # </ Styles >

        # < Global Settings >
        self.setFixedSize(2510, 160)
        self.move(30, 1200)
        # </ Global Settings >

        # < Main Style >
        self.main_back = QLabel(self)
        self.main_back.resize(2500, 150)
        self.main_back.setStyleSheet(self.background_style_css)
        # </ Main Style >

        # < Close Button >
        self.close_button = QPushButton(self)
        self.close_button.setStyleSheet(self.close_button_style_css)
        self.close_button.setText("X")
        self.close_button.resize(20, 20)
        self.close_button.move(2475, 5)
        self.close_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.close_button.clicked.connect(self.close_window)
        # < Close Button >

        # < Test Button >
        self.test_button = QPushButton(self)
        self.test_button.setStyleSheet(self.close_button_style_css)
        self.test_button.setText("Translate")
        self.test_button.resize(75, 20)
        self.test_button.move(2390, 5)
        self.test_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.test_button.clicked.connect(self.change_text)
        # < Test Button >

        # < Text Label >
        self.text_label = QLabel(self)
        self.text_label.move(10, 0)
        self.text_label.resize(2300, 100)
        self.text_label.setText("Original Sentence")
        self.text_label.setStyleSheet(self.text_label_style_css)
        # < Text Label >

        # < Translate Label >
        self.translate_label = QLabel(self)
        self.translate_label.move(10, 65)
        self.translate_label.resize(2300, 100)
        self.translate_label.setText("Translation")
        self.translate_label.setStyleSheet(self.text_label_style_css)
        # < Text Label >

        # < Header Style >
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # </ Header Style >

        move_page(self)

    def close_window(self):

        self.close()
        sys.exit()

    def change_text(self):
        r = sr.Recognizer()
        mic = sr.Microphone(device_index=1)
        with mic as source:
            audio = r.listen(source)
        text = r.recognize_google(audio)
        print(text)
        self.text_label.setText(text)
        translator = Translator()
        translation = translator.translate(text, src="en", dest="fr")
        print(translation.text)
        self.translate_label.setText(translation.text)


def get_audio():

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()
    # SPEAKERS = p.get_default_output_device_info()["hostApi"]
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=1)
    # input_host_api_specific_stream_info=SPEAKERS)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    """
    # get a list of all speakers:
    speakers = sc.all_speakers()
    # get the current default speaker on your system:
    default_speaker = sc.default_speaker()

    # get a list of all microphones:v
    mics = sc.all_microphones(include_loopback=True)
    # get the current default microphone on your system:
    default_mic = mics[4]

    for i in range(len(mics)):
        try:
            print(f"{i}: {mics[i].name}")
        except Exception as e:
            print(e)

    with default_mic.recorder(samplerate=148000) as mic, \
            default_speaker.player(samplerate=148000) as sp:
        print("Recording...")
        data = mic.record(numframes=1000000)
        print("Done...Stop your sound so you can hear playback")
        time.sleep(5)
        sp.play(data)
    """


if __name__ == '__main__':
    """
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ",
                  p.get_device_info_by_host_api_device_index(0, i).get('name'))
    """
    #p = pyaudio.PyAudio()
    """
    temp = [p.get_device_info_by_index(i) for i in range(p.get_device_count())]
    for i in temp:
        print(i['index'], i['name'])

    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if (dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0):
            dev_index = dev['index']
            print('dev_index', dev_index)
    """
    get_audio()
    My_Application = QApplication(sys.argv)
    MainWindow = MyNotification()
    MainWindow.show()
    sys.exit(My_Application.exec_())
