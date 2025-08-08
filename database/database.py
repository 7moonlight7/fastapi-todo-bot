from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///user.db', echo=True)
SessionLocal = sessionmaker(engine)
