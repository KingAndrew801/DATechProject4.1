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

def readerfunc(target):
    with open(f'./store-inventory/{target}.csv', newline='') as csvfile:
        brandreader = csv.reader(csvfile, delimiter="|")
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
        cleanerprod = row[0].split(',')
        cleantitle = []
        print(cleanerprod)
        print(f'this is the len = {len(cleanerprod)}')
        if len(cleanerprod) > 5:
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            cleantitle.append(cleanerprod[0])
            modtitle = []
            lenrange = len(cleanerprod) - 5
            print(f'this is the target index {len(cleanerprod) - 5}')
            print(f'this is the target string= {cleanerprod[1]}')
            for titlecount in range(1, (lenrange)):
                print(f"titlecount = {titlecount}")
                cleanesttitle = cleantitle + cleanerprod[titlecount]
                print(cleanesttitle)












if __name__ == "__main__":
    Base.metadata.create_all(engine)
    # rows = readerfunc('inventory')
    # for row in rows:
    #     print(row)
    prodloader()