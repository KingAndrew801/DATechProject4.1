from sqlalchemy import create_engine, Date, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import csv
from datetime import datetime

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
    product_price = Column(Integer)
    date_updated = Column(Date)
    brand_id = Column(Integer)

    def __repr__(self):
        return f"""{self.product_name}
{self.product_quantity}, {self.product_price}, {self.date_updated}"""

def readerfunc(target):
    with open(f'./store-inventory/{target}.csv', newline='') as csvfile:
        brandreader = csv.reader(csvfile, delimiter=",")
        rows = list(brandreader)
        return rows

def loadbrands():
    rows = readerfunc('brands')
    del rows[0]
    if session.query(Brands).first():
        for row in rows:
            if brandchecker(row[0]):
                continue
            else:
                session.add(Brands(brand_name = row[0]))
    else:
        for row in rows:
            print(row[0])
            newbrand = Brands(brand_name = row[0])
            session.add(newbrand)
    session.commit()

def brandchecker(bsearch):
    for item in session.query(Brands):
        if item.brand_name == bsearch:
            return item

def prodloader():
    rows = readerfunc('inventory')
    del rows[0]
    for row in rows:
        if prodchecker(row):
            cleanprice = row[1].replace('$', '')
            upprod = prodchecker(row)
            upprod.product_price = int(cleanprice.replace('.', ''))
            upprod.product_quantity = int(row[2])
            upprod.date_updated = datetime.strptime(row[3], '%m/%d/%Y').date()
        else:
            cleanprice = row[1].replace('$', '')
            cprod = Product(product_name = row[0],
                    product_price=int(cleanprice.replace('.', '')),
                    product_quantity = int(row[2]),
                    date_updated = datetime.strptime(row[3], '%m/%d/%Y').date(),
                    brand_id = brandidfinder(row[4]))
            session.add(cprod)
    session.commit()

def prodchecker(psearch):
    for item in session.query(Product):
        if item.product_name == psearch[0]:
            return item

def brandidfinder(brand):
    for brandie in session.query(Brands):
        if brandie.brand_name == brand:
            return brandie.brand_id











if __name__ == "__main__":
    Base.metadata.create_all(engine)
    # rows = readerfunc('inventory')
    # for row in rows:
    #     print(row)
    for item in session.query(Brands):
        print(item)
        print(f'Product id = {item.brand_id}')
    # loadbrands()
    # prodloader()
