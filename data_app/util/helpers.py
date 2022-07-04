import boto3, botocore
import os
import pandas as pd
from werkzeug.utils import secure_filename

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def upload_file_to_s3(file):
    filename = secure_filename(file.filename)
    print(f'HGDEUQYGDK {filename}')
    print(f'HGDEUQYGDK {file}')
    print(f'HGDEUQYGDK {file.content_type}')
    try:
        # with open("FILE_NAME", "rb") as f:
        #     s3.upload_fileobj(f, 
        #                      os.getenv("AWS_BUCKET_NAME"), 
        #                      "OBJECT_NAME")
        s3.upload_fileobj(
            file,
            os.getenv("S3_BUCKET"),
            file.filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    
    # after upload file to s3 bucket, return filename of the uploaded file
    return file.filename

def read_csv_from_s3(key):
    data = s3.get_object(Bucket=os.getenv("S3_BUCKET"), Key=key)
    initial_df = pd.read_csv(data['Body'])
    return initial_df