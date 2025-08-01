import os

class S3Sync:
    def sync_folder_to_s3(self,folder,aws_bucket_url):
        '''
        Syncs a local folder to an S3 bucket.
        Args:
            folder (str): The local folder to sync.
            aws_bucket_url (str): The S3 bucket URL to sync to.
        '''
        command = f"aws s3 sync {folder} {aws_bucket_url} "
        os.system(command)

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        '''
        Syncs an S3 bucket to a local folder.
        Args:
            folder (str): The local folder to sync.
            aws_bucket_url (str): The S3 bucket URL to sync from.
        '''
        command = f"aws s3 sync  {aws_bucket_url} {folder} "
        os.system(command)