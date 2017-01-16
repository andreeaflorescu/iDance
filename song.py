import peakutils
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
from string import rsplit, split
import numpy as np

from pydub import AudioSegment

from globals import Channel


class Song(object):
    def get_fourier_transform(self):
        pass

class WAVSong(Song):

    def __init__(self, song_path):
        self.rate, self.data = wavfile.read(song_path) # load the data
        self.channel_type = self.get_channel_type()
        self.bit_format = self.get_bit_format()
        self.track = self.get_track()
        self.fourier_t = None
        self.song_path = song_path
        s = song_path.rsplit("/", 1)
        if len(s) == 1:
            self.song_name = s[0]
        else:
            self.song_name = s[1]

    def get_rate(self):
        return self.rate

    def get_song_name(self):
        return self.song_name

    # a song can be stereo or mono
    # when the song is stereo, it has two arrays T
    def get_channel_type(self):
        if len(self.data.T.shape) == 1:
            return Channel.TYPE.MONO
        else:
            return Channel.TYPE.STEREO

    '''
    This function returns 32, 16, 8 and it is used for normalizing the vector
    WAV format	dtype
    32-bit      float32
    32-bit      int32
    16-bit      int16
    8-bit   	uint8
    '''
    def get_bit_format(self):
        bits = self.data.dtype.name[len(self.data.dtype.name) - 2:len(self.data.dtype.name)]
        if bits.isdigit():
            bits = int(bits)
        else:
            bits = int(bits[1])
        print "bits=", bits
        return bits

    def get_nr_of_tracks(self):
        if self.channel_type == Channel.TYPE.MONO:
            return 1
        else:
            return 2

    def get_track(self):
        print "data len=",len(self.data.T)
        print "rate=", self.rate
        if self.channel_type == Channel.TYPE.MONO:
            return self.data.T
        else:
            return self.data.T[1]

    def get_fourier_transform(self):
        normalized_track = [(element / 2 ** float(self.bit_format)) * 2 - 1 for element in self.track]
        fourier_t = fft(normalized_track)
        self.fourier_t = fourier_t
        return fourier_t

    def get_chunks_size(self):
        chunks = []
        # chunk_size = 0
        start_index = 0
        # end_index = 0
        # musical phrases should be at least 4 seconds
        min_dist = self.index_to_seconds(0, 1)
        # print len(np.absolute(self.fourier_t))
        length = len(self.fourier_t)
        values = self.fourier_t[:length/2]
        print "leng=", len(values)
        indexes = peakutils.indexes(values, min_dist=min_dist)
        print len(indexes)
        if self.channel_type == Channel.TYPE.STEREO:
            indexes = indexes[:len(indexes)/2 - 1]
        # verify that the first chunk has more than 4 seconds or else exclude it
        if indexes[0] < min_dist:
            indexes = indexes[1:]

        for i in indexes:
            chunk_size = i/(self.rate*self.get_nr_of_tracks())
            chunks.append(chunk_size)

        return chunks

    '''
    Returns the index of the fourier_transform element which is
    nr of seconds grater than the start element
    start = index in fourier_t
    seconds = number of seconds
    '''

    def index_to_seconds(self, start, seconds):
        # rate is the number of samples per seconds
        return start + self.rate * seconds

    def split_in_musical_phrases(self):
        splitter = WAVSongSplitter(self.song_path, "new")
        splitter.split_song_in_chunks(self.get_chunks_size())


class WAVSongSplitter(object):
    def __init__(self, song_path, results_dir=""):
        self.song = AudioSegment.from_wav(song_path)
        s = song_path.rsplit("/", 1)
        if len(s) == 1:
            self.song_name = s[0]
            self.results_dir = ""
        else:
            self.song_name = s[1]
            self.results_dir = s[0]

        print "song name: ", self.song_name
        if results_dir:
            self.results_dir = results_dir

        print "results directory: ", self.results_dir

    # chunk is in seconds
    def split_song_in_chunks(self, chunks):
        start = 0
        for index, chunk in enumerate(chunks):
            m_chunk = chunk * 1000 # pydub works with milliseconds
            end = start + m_chunk
            chunk_name = "{0}{1}.wav".format(self.song_name, index)
            chunk_song = self.song[start:end]
            chunk_song.export(self.results_dir + "/" + chunk_name, format="wav")
            start = end