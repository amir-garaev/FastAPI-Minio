from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Query, Header
from base.models import create_meme, Meme
from client_minio import client, upload_image_to_minio
from minio.error import S3Error
from sqlalchemy.orm import Session
from config import MINIO_BUCKET_NAME
from base.session import get_db

router = APIRouter()

def admin_token_required(admin_token: str = Header(None)):
    if admin_token != "admin meme":
        raise HTTPException(status_code=403, detail="Ты не админ мемов ;(")

#http://0.0.0.0:9999/memes/1
@router.get("/{meme_id}")
async def get_meme(meme_id: int, db: Session = Depends(get_db)):
    """
    Получить мем по его ID.

    Параметры:
    - meme_id: ID мема

    Возвращает:
    - ID, заголовок и URL изображения мема
    """
    meme = db.query(Meme).filter(Meme.id == meme_id).first()
    if meme is None:
        raise HTTPException(status_code=404, detail="Мем не найден ;(")
    return {"id": meme.id, "title": meme.title, "image_url": meme.image_url}


#http://0.0.0.0:9999/memes/?skip=0&limit=10
@router.get("/")
async def get_memes_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Получить список мемов.

    Параметры:
    - skip: Количество пропущенных мемов
    - limit: Максимальное количество возвращаемых мемов

    Возвращает:
    - Список мемов с их ID, заголовками и URL изображений
    """
    memes = db.query(Meme).offset(skip).limit(limit).all()
    if not memes:
        raise HTTPException(status_code=404, detail="Мемов нету ;(")
    return [{"id": meme.id, "title": meme.title, "image_url": meme.image_url} for meme in memes]


@router.post("/")
async def upload_meme(title_meme: str,
                      img_meme: UploadFile = File(...),
                      db: Session = Depends(get_db),
                      admin_token: str = Depends(admin_token_required)):
    """
    Загрузить новый мем.

    Параметры:
    - title_meme: Заголовок мема
    - img_meme: Файл изображения мема

    Возвращает:
    - Сообщение об успешной загрузке и ID мема
    """
    try:
        file_url = await upload_image_to_minio(img_meme)
        meme = create_meme(db=db, title=title_meme, image_url=file_url)

        return {"message": "Мем успешно загружен :)", "meme_id": meme.id}

    except S3Error as e:
        return {"error": f"Что-то пошло не так ;( Ошибка: {e}"}


@router.delete("/{meme_id}")
async def delete_meme(meme_id: int, db: Session = Depends(get_db), admin_token: str = Depends(admin_token_required)):
    """
    Удалить мем по его ID.

    Параметры:
    - meme_id: ID мема

    Возвращает:
    - Сообщение об успешном удалении
    """
    meme = db.query(Meme).filter(Meme.id == meme_id).first()
    if meme is None:
        raise HTTPException(status_code=404, detail="Мем не найден ;(")

    try:
        object_name = meme.image_url.split("/")[-1]
        client.remove_object(MINIO_BUCKET_NAME, object_name)
    except Exception as e:
        print(f"Failed to delete image from Minio: {e}")

    db.delete(meme)
    db.commit()
    return {"message": "Мем успешно удален :)"}



@router.put("/{meme_id}")
async def update_meme(meme_id: int,
                      title_meme: str = Query(None),
                      img_meme: UploadFile = File(None),
                      db: Session = Depends(get_db),
                      admin_token: str = Depends(admin_token_required)):
    """
    Обновить мем по его ID.

    Параметры:
    - meme_id: ID мема
    - title_meme: Новый заголовок мема (опционально)
    - img_meme: Новый файл изображения мема (опционально)

    Возвращает:
    - Сообщение об успешном обновлении
    """
    meme = db.query(Meme).filter(Meme.id == meme_id).first()
    if meme is None:
        raise HTTPException(status_code=404, detail="Мем не найден ;(")

    if title_meme is not None:
        meme.title = title_meme

    if img_meme is not None:
        file_url = await upload_image_to_minio(img_meme)
        meme.image_url = file_url

    db.commit()
    return {"message": "Мем успешно обновлен :)"}