from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class Meme(Base):
    __tablename__ = "meme"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    image_url = Column(String, nullable=False)


def create_meme(db: Session, title: str, image_url: str):
    meme = Meme(title=title, image_url=image_url)
    db.add(meme)
    db.commit()
    db.refresh(meme)
    return meme