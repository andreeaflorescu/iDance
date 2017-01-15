from scipy.fftpack import fft
from scipy.io import wavfile # get the api
from string import rsplit, split

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
            return 0
        else:
            return 1

    def get_track(self):
        if self.channel_type == Channel.TYPE.MONO:
            return self.data.T
        else:
            return self.data.T[1]

    def get_fourier_transform(self):
        normalized_track = [(element / 2 ** float(self.bit_format)) * 2 - 1 for element in self.track]
        fourier_t = fft(normalized_track)
        return fourier_t


class WAVSongSplitter(object):
    def __init__(self, song_path, results_dir=""):
        self.song = AudioSegment.from_wav(song_path)
        self.song_name = song_path.rsplit("/", 1)[1]
        print "song name: ", self.song_name
        if results_dir:
            self.results_dir = results_dir
        else:
            self.results_dir = song_path.rsplit("/", 1)[0]

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