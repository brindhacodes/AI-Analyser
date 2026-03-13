from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
db_url = "postgresql://postgres:sana07@localhost:5432/ai_risk_db"
#SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://ai_user:sana07@localhost:5432/ai_risk_db"
engine = create_engine(db_url) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
Base=declarative_base()