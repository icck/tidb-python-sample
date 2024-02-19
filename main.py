import os

from dotenv import load_dotenv
from sqlalchemy import URL, Column, Text, Uuid, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

dsn = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("TIDB_USER", "root"),
    password=os.getenv("TIDB_PASSWORD", ""),
    host=os.getenv("TIDB_HOST", "127.0.0.1"),
    port=int(os.getenv("TIDB_PORT", "4000")),
    database=os.getenv("TIDB_DB_NAME", "test"),
)

connect_args = {
    "ssl_verify_cert": True,
    "ssl_verify_identity": True,
    "ssl_ca": os.getenv("CA_PATH", ""),
}


engine = create_engine(dsn, connect_args=connect_args, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    uuid = Column(Uuid, primary_key=True)
    name = Column(Text, unique=True)


def sampleQuery():
    with Session() as session:
        result = session.query(User).all()

        for user in result:
            print(f"{user.uuid}, {user.name}")


if __name__ == "__main__":
    sampleQuery()
