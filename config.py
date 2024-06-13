import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
MINIO_URL = os.getenv('MINIO_URL')
MINIO_ROOT_USER = os.getenv('MINIO_ROOT_USER')
MINIO_ROOT_PASSWORD = os.getenv('MINIO_ROOT_PASSWORD')
MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')