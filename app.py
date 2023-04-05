from models import Base, engine
from models import Product
from models import Brands
import models
import time


def startapp():
    print("""---------------------------------------
I am the inventory application.
I exist to organize your inventory. :)
I will serve my purpose shortly...
---------------------------------------""")
    time.sleep(0)
    menu()
def menu():
    choosing = True
    while choosing:
        try:
            choice = input("""---------------------------------------
How can I serve you?
---------------------------------------
V = View products by ID number
N = New addition to inventory
A = Analyze inventory database
B = Backup the database
---------------------------------------
Enter selection:  """).lower()
            if choice == 'v':
                prodid = input('''---------------------------------------
Enter product ID number:  ''')
                input(f'''Here are your results:
{models.session.query(Product).filter(Product.product_id == prodid)[0]}
---------------------------------------
Press enter to proceed...''')
            elif choice == 'n':
                    createprod()
            elif choice == 'a':
                pass
        except ValueError as err:
            print(err)

def createprod():
    newpname()
    newpquant()
    newpprice()



def newpname():
    trying = True
    while trying:
        try:
            print("-" * 39)
            newprodname = input('Enter the name of your product:  ')
            if newprodname.isalpha():
                for dbprod in models.session.query(Product):
                    if dbprod.product_name == newprodname:
                        print("A product with this name already exists.")
                    else:
                        trying = False
                        return newprodname
            else:
                raise TypeError('You must use letters for your title.')
        except TypeError as err:
            print(err)
            print("Please try again...")

def newpquant():
    trying = True
    while trying:
        try:
            print("-" * 39)
            newquant = input('Enter the quantity:  ')
            if isinstance(newquant, int):
                trying = False
                return newquant
            else:
                raise ValueError("Quantity must be an integer")
        except TypeError as err:
            print(err)

def newpprice():



if __name__ == "__main__":
    Base.metadata.create_all(engine)
    startapp()