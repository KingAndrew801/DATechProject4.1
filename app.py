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
                    try:
                        print("-"*39)
                        newname = input('Enter the name of your product:  ')
                        if newname.isalpha():
                            continue
                        else:
                            raise ValueError("You must use letters for your title.")
                    except ValueError as err:
                        print('-' * 39)
                        print(err)
                        print("You will be sent back to the menu shortly...")
                        time.sleep(1)
                        break
                    try:
                        print("-" * 39)
                        newquant = input('Enter the quantity:  ')
                        if isinstance(newquant, int):
                            continue
                        else:
                            raise ValueError("Quantity must be an integer")
                    except ValueError as err:
                        print(err)
                        pass
                    pass
        except ValueError as err:
            print(err)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    startapp()