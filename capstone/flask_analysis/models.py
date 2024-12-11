from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class DIMCountry(Base):
    __tablename__ = 'DIM_Country'
    Country_Key = Column(Integer, primary_key=True)
    Country_Code = Column(String(10), unique=True, nullable=False)
    Country_Name = Column(String(72))
    Region = Column(String(255))
    IncomeGroup = Column(String(255))
    SpecialNotes = Column(Text)

class DIMIndicator(Base):
    __tablename__ = 'DIM_Indicator'
    Indicator_Key = Column(Integer, primary_key=True)
    Indicator_Code = Column(String(10), unique=True, nullable=False)
    Indicator_Name = Column(String(255))

class DIMTime(Base):
    __tablename__ = 'DIM_Time'
    Time_Key = Column(Integer, primary_key=True)
    Year = Column(Integer, nullable=False)

class FACTEnrollment(Base):
    __tablename__ = 'FACT_Enrollment'
    Fact_Key = Column(Integer, primary_key=True)
    Country_Key = Column(Integer, ForeignKey('DIM_Country.Country_Key'))
    Indicator_Key = Column(Integer, ForeignKey('DIM_Indicator.Indicator_Key'))
    Time_Key = Column(Integer, ForeignKey('DIM_Time.Time_Key'))
    Indicator_Value = Column(Float)
    Load_Time = Column(String(50))
    Update_Time = Column(String(50))

    country = relationship("DIMCountry", backref="facts")
    indicator = relationship("DIMIndicator", backref="facts")
    time = relationship("DIMTime", backref="facts")
