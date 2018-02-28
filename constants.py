#   Environment Variable keys
folder_name = "folder_name"
bucket_name = 'bucket_name'
repository_name = 'repository_name'
repository_owner = 'repository_owner'
repository_url = 'repository_url'

#   keys
download_url_key = 'download_url'
repository_url_key = 'url'
object_key = 'Key'
name = 'name'
path = 'path'
acl_public_read = 'public-read'
content_type_header = 'ContentType'
acl_header = 'ACL'


#   Regex
repository_url_pattern = 'https://api.github.com/repos/{}/{}/contents/{}'
formattable_pattern = '{}'

#   In a lambda you can only write to /tmp/
lamdaWriteDirectory = '/tmp/'