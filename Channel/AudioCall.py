
from threading import Thread
from Constants import *

import pyaudio

class AudioStream(object):
    """Maneja la llamada"""
    def __init__(self, stream, thread):
        super(AudioStream, self).__init__()
        self.stream = stream
        self.thread = thread

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.thread.join()


class AudioCall(object):
    """Maneja las instancias de pyAudio"""
    CONTINUE = pyaudio.paContinue
    PA = pyaudio.PyAudio()
    OUTPUT = None

    def __init__(self):
        super(AudioCall, self).__init__()

    def record(self, callback):
        stream = AudioCall.PA.open(format=AudioCall.PA.get_format_from_width(Constants.WIDTH),
                    channels=Constants.CHANNELS,
                    rate=Constants.RATE,
                    input=True,
                    stream_callback=callback)
        stream.start_stream()
        thread_record = Thread(target=AuxiliarFunctions.dummy_run, args=(stream.is_active,))
        thread_record.start()

        return AudioStream(stream, thread_record)

    @staticmethod
    def openOutput():
        if AudioCall.OUTPUT is not None:
            return

        # OUTPUT = AudioCall.PA.open(format=AudioCall.PA.get_format_from_width(Constants.WIDTH),
        #                     channels=Constants.CHANNELS,
        #                     rate=Constants.RATE,
        #                     output=True)

    @staticmethod
    def closeOutput():
        pass
