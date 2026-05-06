from app.db.session import Base, engine

# Import models here
from app.models.user import User  # noqa


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()