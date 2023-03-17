from sqlalchemy import create_engine, Date, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import csv

engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Brands(Base):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key= True )
    brand_name = Column(String)



class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Float)
    date_updated = Column(Date)

def loadbrands():
    with open('venv/store-inventory/brands.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter= '|')
        rows = list(reader)
        csvlist = []
        del rows[0]
        print(rows)
        while rows:
            session.add(rows.pop(0))



if __name__ == "__main__":
    Base.metadata.create_all(engine)
    loadbrands()
    print(wtf)