
from threading import Thread
from Constants import *

import pyaudio

class AudioStream(object):
    """Maneja la llamada"""
    def __init__(self, stream):
        super(AudioStream, self).__init__()
        self.stream = stream

    def stop(self):
        print("Terminando hilo.. mensajes en cola pueden no ser enviados..")
        self.stream.stop_stream()
        self.stream.close()


class AudioCall(object):
    """Maneja las instancias de pyAudio"""
    CONTINUE = pyaudio.paContinue

    def __init__(self):
        super(AudioCall, self).__init__()
        self.pa = pyaudio.PyAudio()
        self.stream = None

    def record(self, callback):
        stream = self.pa.open(format=self.pa.get_format_from_width(Constants.WIDTH),
                    channels=Constants.CHANNELS,
                    rate=Constants.RATE,
                    input=True,
                    stream_callback=callback)
        stream.start_stream()
        thread_record = Thread(target=AuxiliarFunctions.dummy_run, args=(stream.is_active,))
        thread_record.start()

        return AudioStream(stream)

    def openOutput(self):
        self.stream = self.pa.open(format=self.pa.get_format_from_width(Constants.WIDTH),
                            channels=Constants.CHANNELS,
                            rate=Constants.RATE,
                            output=True)

    def closeOutput(self):
        self.stream.stop_stream()
        self.stream.close()

    def play(self, audio):
        self.stream.write(audio)
