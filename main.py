import sys
from song import Song, WAVSong, WAVSongSplitter
sys.path.insert(0, 'modules/genreXpose/genreXpose')
from tester import test_model_on_single_file

import warnings
warnings.filterwarnings('ignore')

test_model_on_single_file(sys.argv[1])
song = WAVSong(sys.argv[1])
song.plot_frequencies()
song.split_in_musical_phrases()
