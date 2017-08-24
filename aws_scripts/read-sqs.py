import boto3
import os

from sqs_utils import download_song, get_bucket_and_key, polling, delete_song_from_s3
from config import create_choreography_sqs

s3 = boto3.client('s3')

def split_song_equally(nr_instances, song_path, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    command = "mp3splt {} -S {} -d {}".format(song_path, nr_instances, out_dir)
    os.system(command)

def upload_fragments(fragment_dir):
    fragments = os.listdir(fragment_dir)
    for fragment in os.listdir(fragment_dir):
        fragment_path = fragment_dir + "/" + fragment
        print("Upload fragment: ", fragment_path)
        s3.upload_file(fragment_path, "idance.input.slices", fragment)
        # delete file
        os.remove(fragment_path)

    # detele the fragment dir
    os.rmdir(fragment_dir)
    
def split_song(message):
    song_dict = get_bucket_and_key(message)
    print("Process Song: ", song_dict['object_key'])
    download_song(song_dict['bucket_name'], song_dict['object_key'])
    fragments_dir=song_dict['object_key'] + "_fragments"
    split_song_equally(3, song_dict['object_key'], fragments_dir)
    upload_fragments(fragments_dir)
    
    # delete song
    os.remove(song_dict['object_key'])
    delete_song_from_s3(song_dict['bucket_name'], song_dict['object_key'])
    
polling(create_choreography_sqs, split_song)
