import matplotlib.pyplot as plt
import scipy
import peakutils
# import sys
# from scipy.fftpack import fft
# from scipy.io import wavfile # get the api
# rate, data = wavfile.read("scale.wav") # load the data
# print rate
# bits = data.dtype.name[len(data.dtype.name) - 2:len(data.dtype.name)]
# print len(data.T[1])
# track = data.T[1] # this is a two channel soundtrack, I get the first track
#
# normalized_track=[(element / 2 ** float(bits)) * 2 - 1 for element in track] # this is 8-bit track, b is now normalized on [-1,1)
# print len(normalized_track)
# fourier_t = fft(normalized_track) # calculate fourier transform (complex numbers list)
# print len(fourier_t)
# print rate
# # d = len(fourier_t) / 2  # you only need half of the fft list (real signal symmetry)
# # plt.plot(fourier_t[:(d - 1)], 'r')
# # plt.show()
import sys
from song import Song, WAVSong, WAVSongSplitter

song = WAVSong(sys.argv[1])
fourier_t = song.get_fourier_transform()

song.split_in_musical_phrases()
d = len(fourier_t)/2
plt.plot(fourier_t[:(d -1)], 'r')

# plt.plot(fourier_t[indexes], 'bo')
# plt.show()
# s_splitter = WAVSongSplitter(sys.argv[1], "chunks")
# s_splitter.split_song_in_chunks([10,10,10])