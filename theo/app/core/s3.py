import os
import boto3
from botocore.exceptions import ClientError
import logging
from app.core.config import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name="ap-south-1",
)

s3_folder = "theo_images"
bucket = settings.AWS_BUCKET
local_directory = "./static/"


def create_presigned_url(file_key):
    try:
        response = s3_client.generate_presigned_url(
            "get_object", Params={"Bucket": bucket, "Key": file_key}
        )
    except ClientError as e:
        logging.error(e)
        return None
    return response


def upload_obj(file, file_path) -> None:
    try:
        s3_client.upload_fileobj(file, bucket, file_path)
        logging.info(f"\t[ Upload to S3 ]")
    except Exception as e:
        logging.error(e)


def copy_obj(old_path, new_path):
    try:
        s3_client.copy_object(
            Bucket=bucket, CopySource={"Bucket": bucket, "Key": old_path}, Key=new_path
        )
        logging.info(f"\t[ Copy {old_path} to {new_path} on S3 ]")
    except Exception as e:
        logging.error(e)


def move_folder(source, old_prefix, new_prefix) -> None:
    objects = s3_client.list_objects(Bucket=bucket, Prefix=source)
    try:
        for obj in objects["Contents"]:
            old_folder = obj["Key"]
            new_folder = old_folder.replace(old_prefix, new_prefix, 1)
            copy_obj(old_folder, new_folder)
        if old_prefix != new_prefix:
            remove_folder(source)
    except Exception as e:
        print(f"\n{e}\n")
    logging.info(f"\t[ Move {source} to {new_prefix} ]")


def download_obj(file_name):
    try:
        os.makedirs(local_directory, exist_ok=True)
        local_file_path = os.path.join(local_directory, file_name)
        s3_client.download_file(bucket, file_name, local_file_path)
        logging.info(f"\t[ Download {file_name} from S3 ]")
    except Exception as e:
        logging.error(e)
        return False
    return True


def remove_obj(file_key):
    try:
        s3_client.delete_object(Bucket=bucket, Key=file_key)
        logging.info(f"\t[ Remove object {file_key.split('/')[1]} from S3 ]")
    except Exception as e:
        logging.error(e)


def remove_folder(folder_key):
    try:
        objects = s3_client.list_objects(Bucket=bucket, Prefix=folder_key)
        for obj in objects["Contents"]:
            remove_obj(obj["Key"])
        s3_client.delete_object(Bucket=bucket, Key=folder_key)

        logging.info(f"\t[ Remove folder {folder_key.split('/')[-1]}/ from S3 ]")
    except Exception as e:
        logging.error(e)
