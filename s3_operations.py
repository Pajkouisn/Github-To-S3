import boto3
import logging
import constants

#   Set logging level
logger = logging.getLogger()

#   Boto3 client for S3.
s3 = boto3.client('s3')

def delete_all_objects(bucket_name = None):
    #   TODO recursively delete all objects in case there are more than 1000 objects.
    #   List and delete all objects fom the bucket.
    objects = s3.list_objects(Bucket=bucket_name)
    logger.debug(objects)

    #   Delete all existing objects
    try:
        for object in objects['Contents']:
            key = object[constants.object_key]
            try:
                s3.delete_object(
                    Bucket=bucket_name,
                    Key=key)
                logger.info('Deleted ' + key)
            except:
                logger.info('Cannot delete ' + key)
    except KeyError as e:
        logger.info('No objects to delete')

def upload_from_local(localFSFilename = None, bucketName = None, key = None, extraArgs = None):
    #   Upload file to S3.
    s3.upload_file(
        localFSFilename,
        bucketName,
        key,
        ExtraArgs= extraArgs
    )