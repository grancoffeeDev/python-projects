import os
from google.cloud import storage

class gcs:
        def __init__(self,credentials=None) -> None:
                self.credentials = credentials
                if self.credentials!=None:
                    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= self.credentials 

        def set(self, project,bucket_name,folder):
            self.project = project
            self.bucket_name = bucket_name
            self.folder = folder
            return

        def sendFile(self, File, remote_file):
            project_id = self.project 
            bucket_name = self.bucket_name
            bucket_file = self.folder+remote_file 
            local_file = File

            # Initialise a client
            client = storage.Client(project_id)
            bucket = client.get_bucket(bucket_name)
            blob = bucket.blob(bucket_file)
            blob.open()
            # Upload the file to a destination
            blob.upload_from_filename(local_file)
            #blob.upload_from_string(Data)
            return
            
        def upload_blob(self, blob_text, remote_file):
            bucket_file = self.folder+remote_file
            storage_client = storage.Client(self.project)
            bucket = storage_client.get_bucket(self.bucket_name)
            blob = bucket.blob(bucket_file)
#            blob.open()
            blob.upload_from_string(blob_text,content_type='application/json')
            return