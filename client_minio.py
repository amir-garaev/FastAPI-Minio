from fastapi import UploadFile
from minio import Minio, S3Error

from config import MINIO_URL, MINIO_BUCKET_NAME, MINIO_ROOT_USER, MINIO_ROOT_PASSWORD

client = Minio(
    MINIO_URL.replace('http://', ''),
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
    secure=False
)


async def upload_image_to_minio(img_meme: UploadFile):
    img_meme.file.seek(0, 2)
    file_length = img_meme.file.tell()
    img_meme.file.seek(0)

    # Проверяем существование бакета и создаем его, если не существует
    try:
        if not client.bucket_exists(MINIO_BUCKET_NAME):
            client.make_bucket(MINIO_BUCKET_NAME)
    except S3Error as exc:
        # Обработка ошибки создания бакета
        return f"Failed to create bucket: {exc}"

    # Загрузка файла в бакет
    try:
        client.put_object(MINIO_BUCKET_NAME, img_meme.filename, img_meme.file, length=file_length)
        return f"{MINIO_URL}/{MINIO_BUCKET_NAME}/{img_meme.filename}"
    except S3Error as exc:
        # Обработка ошибки загрузки файла
        return f"Failed to upload file: {exc}"