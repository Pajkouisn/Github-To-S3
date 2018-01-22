import boto3
import urllib2
import json
import wget
import os
from multiprocessing.pool import ThreadPool
import mimetypes

#   Boto3 client for S3.
s3 = boto3.client('s3')

#   Default git repository for the website. e.g. https://api.github.com/repos/Pajkouisn/SNSTesting/contents
repository = 'https://api.github.com/repos/{}/{}/contents/{}'.format(os.getenv('repository_owner'), os.getenv('repository_name'), os.getenv('folder_name'))

#   The Download URL key.
downloadUrlKey = 'download_url'

#   In a lambda you can only write to /tmp/
lamdaWriteDirectory = '/tmp/'

def lambda_handler(event, context):

    #   Get the list of files in the repository.
    filesInRepository = json.loads(urllib2.urlopen(repository).read())

    print filesInRepository

    pool = ThreadPool(processes=16)
    pool.map(download, filesInRepository)

#   Function to download files using Wget.
def download(file):

    print type(file)
    print file
    print file[downloadUrlKey]

    #   Set the bucket name and bucket key.
    bucketName = os.getenv('bucket_name')
    # print bucketName
    key = file['name']
    # print key

    #   Finalename on local FS on Lambda.
    localFSFilename = lamdaWriteDirectory + key

    #   Download the file from github.
    wget.download(file[downloadUrlKey], out=localFSFilename)

    #   Upload file to S3.
    s3.upload_file(
        localFSFilename,
        bucketName,
        key,
        ExtraArgs=
        {
            'ContentType': '{}'.format(mimetypes.MimeTypes().guess_type(localFSFilename)[0]),
            'ACL':'public-read'
        }
    )

