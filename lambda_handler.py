import boto3
import urllib2
import json
import wget
import os
from multiprocessing.pool import ThreadPool
import mimetypes
import logging
import constants
import s3_operations
import github_operations

#   Set logging level
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#   Default git repository for the website. e.g. https://api.github.com/repos/Pajkouisn/SNSTesting/contents
repository_url = constants.repository_url_pattern.format(
    os.getenv(constants.repository_owner),
    os.getenv(constants.repository_name),
    os.getenv(constants.folder_name))

#   Bucket name
bucketName = os.getenv(constants.bucket_name)

def download_from_github_upload_to_s3 (file):

    logger.debug(type(file))
    logger.debug(file)

    #   Fetch the download URL.
    download_url = file[constants.download_url_key]
    logger.debug(download_url)

    #   If the download URL is not present, it is a folder. Recursively download.
    if download_url is None:
        folder_url = file[constants.repository_url_key]
        dispatcher(folder_url)

    else:
        #   Set the bucket name and bucket key.
        key = file[constants.path].replace(os.getenv(constants.folder_name) + '/', "")

        #   Finalename on local FS on Lambda.
        local_FS_file_name = constants.lamdaWriteDirectory + file[constants.name]

        github_operations.download_locally(url = file[constants.download_url_key], local_path = local_FS_file_name)

        #   Arguments to preserve mime type and make objects publicly available.
        extraArgs = {
            constants.content_type_header: constants.formattable_pattern.format(mimetypes.MimeTypes().guess_type(local_FS_file_name)[0]),
            constants.acl_header: constants.acl_public_read
        }

        #   Upload to S3 and make public.
        s3_operations.upload_from_local(localFSFilename=local_FS_file_name, bucketName=bucketName, key=key,
                                        extraArgs=extraArgs)


def dispatcher(repository_url):

    #   Get the list of files in the repository.
    filesInRepository = github_operations.list_content(repository_url)

    logger.debug(json.dumps(filesInRepository))

    #   Dispatch threads to download files and put to S3.
    pool = ThreadPool(processes=16)
    pool.map(download_from_github_upload_to_s3, filesInRepository)

def lambda_handler(event, context):

    s3_operations.delete_all_objects(bucket_name=bucketName)
    dispatcher(repository_url)

