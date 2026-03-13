from sqlalchemy import Column, Float, Integer, String, Text
from database import Base

class EthicsAnalysis(Base):

    __tablename__ = "ethics_analysis"

    id = Column(Integer, primary_key=True, index=True)
    idea = Column(String)

    bias_risk = Column(Integer)
    privacy_risk = Column(Integer)
    transparency_risk = Column(Integer)
    misuse_risk = Column(Integer)

    overall_risk = Column(String)
    
    accuracy = Column(Float)
    processing_time = Column(Float)
    compliance_score = Column(Float)

    suggestion1 = Column(String)
    suggestion2 = Column(String)
    suggestion3 = Column(String)

    ethics_report = Column(Text)