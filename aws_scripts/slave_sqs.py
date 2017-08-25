import boto3
import os

from shutil import copyfile

from sqs_utils import download_song, get_bucket_and_key, polling, delete_song_from_s3
from config import process_song_fragments_sqs, output_sliced_choreography

s3 = boto3.client('s3')

def upload_choreography(choreography_name):
    print ("Uploading choreography: ", choreography_name)
    response = s3.upload_file(choreography_name, output_sliced_choreography, choreography_name)
    print(response)
    # delete local copy of the choreography
    os.remove(choreography_name)

def create_choreography(message):
    song_dict = get_bucket_and_key(message)
    print("Process Song: ", song_dict['object_key'])
    print("Bucket Name: ", song_dict['bucket_name'])
    download_song(song_dict['bucket_name'], song_dict['object_key'])
    
    choreography_name = song_dict['object_key'].replace("mp3", "avi")
    
    # dummy create choreography
    # should be replace with model.predict(song) & many other things i have not implemented
    copyfile(song_dict['object_key'], choreography_name)
    
    # TODO: add music to the choreography
    # upload choreography to S3 bucket
    upload_choreography(choreography_name) 
    # delete song
    os.remove(song_dict['object_key'])
    delete_song_from_s3(song_dict['bucket_name'], song_dict['object_key'])
    
    # delete local copy of the choreography
    os.remove(choreography_name)

polling(process_song_fragments_sqs, create_choreography)

