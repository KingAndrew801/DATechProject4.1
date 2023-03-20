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

    def __repr__(self):
        return f"{self.brand_name}"



class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Float)
    date_updated = Column(Date)

def loadbrands():
    with open('./store-inventory/brands.csv', newline='') as csvfile:
        brandreader = csv.reader(csvfile, delimiter= "|")
        rows= list(brandreader)
        del rows[0]
        for row in rows:
            print(row[0])
            newbrand = Brands(row[0])
            session.add(newbrand)



if __name__ == "__main__":
    Base.metadata.create_all(engine)
    loadbrands()