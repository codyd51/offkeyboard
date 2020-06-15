import wave
from abc import ABC, abstractmethod

import pyaudio
import numpy as np


class FrameProvider(ABC):
    """Protocol to read an audio buffer
    Implementations can be backed by mic input, a sound file, etc.
    """
    def __init__(self, sample_rate=0, samples_per_frame=0):
        self.sample_rate = sample_rate
        self.samples_per_frame = samples_per_frame

    @abstractmethod
    def has_frames(self) -> bool:
        """Is there more data to be read from the audio stream?
        """
        pass

    @abstractmethod
    def get_frame(self):
        """Retrieve the next frame of audio data
        """
        pass


class MicrophoneFrameProvider(FrameProvider):
    def __init__(self, sample_rate: int, samples_per_frame: int) -> None:
        super(MicrophoneFrameProvider, self).__init__(sample_rate, samples_per_frame)

        self.stream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            input=True,
            frames_per_buffer=samples_per_frame)

        self.stream.start_stream()

    def has_frames(self) -> bool:
        return self.stream.is_active()

    def get_frame(self) -> np.array:
        return np.fromstring(self.stream.read(self.samples_per_frame, exception_on_overflow=False), np.int16)


class WavFileFrameProvider(FrameProvider):
    def __init__(self, filename, samples_per_frame: int):
        self.wav = wave.open(filename, 'rb')

        super(WavFileFrameProvider, self).__init__(self.wav.getframerate(), samples_per_frame)

    def has_frames(self) -> bool:
        return True

    def get_frame(self) -> np.array:
        return np.fromstring(self.wav.readframes(self.samples_per_frame), np.int16)
