from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    bucket_name = 'cutcy-bucket'
    location = 'media'

# may be used later to store static files separately in a 'static' folder on s3 bucket
# class StaticStorage(S3Boto3Storage):
#     bucket_name = 'cutcy-bucket'
#     location = 'static'