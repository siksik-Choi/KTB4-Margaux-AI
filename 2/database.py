from sqlmodel import create_engine, SQLModel

# Database 설정
DATABASE_URL = "sqlite:///./posts_comments.db"
engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
