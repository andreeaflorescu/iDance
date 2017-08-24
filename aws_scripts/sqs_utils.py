import boto3
import json
import botocore

# Create SQS client
sqs = boto3.client('sqs')
s3_resource = boto3.resource('s3')
s3 = boto3.client('s3')

def download_song(bucket_name, song_key):
    song_key = song_key.replace("+", " ")
    try:
        s3_resource.Bucket(bucket_name).download_file(song_key, song_key)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
             print("The object does not exist.")
        else:
             raise

def get_bucket_and_key(message):
    body = json.loads(message['Body'])
    s3 = body['Records'][0]['s3']
    bucket_name = s3['bucket']['name']
    key = s3['object']['key']
    res = {}
    res['bucket_name'] = bucket_name
    res['object_key'] = key
    return res

def polling(queue_url, process_message_callback):
    while 1:
        try:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                WaitTimeSeconds=5,
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ],
                VisibilityTimeout=0,
            )

            message = response['Messages'][0]
            receipt_handle = message['ReceiptHandle']
            print("received message")
            # Delete received message from queue
            try:
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=receipt_handle
                )
            except Exception as e:
                print("Insuficient permissions to delete message")

            process_message_callback(message)

        except Exception as e:
            # an Exception is thrown if there are no messages in the queue
            # do nothing
            continue

def delete_song_from_s3(bucket_name, song_key):
    response = s3.delete_object(
        Bucket=bucket_name,
        Key=song_key)
    print(response)
