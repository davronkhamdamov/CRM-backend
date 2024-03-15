from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = "postgresql://nxhimsrt:Erbd22xs5GKHa4vDXmB9Uf_5MV4bOXz3@bubble.db.elephantsql.com/nxhimsrt"

engine = create_engine(url=database_url)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()
