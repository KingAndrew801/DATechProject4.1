from models import Base, engine, Product, Brands
import datetime, models, time, csv


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
                print('---------------------------------------')
                input(f'''Here are your results:
{models.session.query(Product).filter(Product.product_id == prodid)[0]}
---------------------------------------
Press enter to proceed...''')
            elif choice == 'n':
                    createprod()
            elif choice == 'a':
                mostexp = ['nada', 0]
                for i in models.session.query(Product):
                    if i.product_price > mostexp[1]:
                        mostexp = [i.product_name, i.product_price]
                print(f"{mostexp[0]} is the most expensive product ({mostexp[1]})")
                leastexp = ['nada', 99999999]
                for i in models.session.query(Product):
                    if i.product_price < leastexp[1]:
                        leastexp = [i.product_name, i.product_price]
                print(f"{leastexp[0]} is the cheapest product ({leastexp[1]})")
                brandies = []
                largie = ('nada' , 0)
                for b in models.session.query(Brands):
                    brandies.append((b, len(list(models.session.query(Product).filter(Product.brand_id == b.brand_id)))))
                for v in brandies:
                    if v[1] > largie[1]:
                        largie = v
                print(f'{largie[0]} has the most products of any brand ({largie[1]})')
                oldie = ('nada', datetime.date.today())
                for p in models.session.query(Product):
                    if p.date_updated < oldie[1]:
                        oldie = (p.product_name, p.date_updated)
                print(f'{oldie[0]} has spent the most time without an update ({oldie[1]})')
                wenis = input('''---------------------------------------
Press enter to continue...''')

            elif choice == 'b':
                with open('backup.csv', 'a', newline='') as csvfile:
                    fieldnames = ['product_id', 'product_name', 'product_price', 'product_quantity', 'date_updated', 'brand_id']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for item in models.session.query(Product):
                        if len(str(item.product_price)) >= 3:
                            newp = '$' + str(item.product_price)[:-2] + '.' + str(item.product_price)[1:]
                        if len(str(item.product_price)) == 2:
                            newp = '$' + '0.' + str(item.product_price)
                        if len(str(item.product_price)) == 1:
                            newp = '$' + '0.0' + str(item.product_price)
                        writer.writerow({
                            'product_id': item.product_id,
                            'product_name': item.product_name,
                            'product_price': newp, 'product_quantity': item.product_quantity,
                            'date_updated': str(datetime.datetime.strftime(item.date_updated, '%m/%d/%Y')),
                            'brand_id': item.brand_id})
                wenis = input('''---------------------------------------
A backup for your database has been created :)
Press any Key to continue...''')

        except ValueError as err:
            print(err)
    input("Press enter to continue...")
def createprod():
    newp = Product(product_name = newpname(), product_quantity = newpquant(),
                   product_price = newpprice(),date_updated = datetime.datetime.now().date(),
                   brand_id = newpbrand())
    return newp



def newpname():
    trying = True
    while trying:
        try:
            print("-" * 39)
            newprodname = input('Enter the name of your product:  ')
            for dbprod in models.session.query(Product):
                if dbprod.product_name == newprodname:
                    print("A product with this name already exists.")
                else:
                    trying = False
                    return newprodname
        except TypeError as err:
            print(err)
            print("Please try again...")

def newpquant():
    trying = True
    while trying:
        try:
            print("-" * 39)
            newquant = input('Enter the quantity:  ')
            if isinstance(int(newquant), int):
                trying = False
                return newquant
            else:
                raise TypeError("Quantity must be expressed as an integer")
        except TypeError as err:
            print(err)
            print("Please try again...")

def newpprice():
    trying = True
    while trying:
        try:
            print("-" * 39)
            print("Enter price with no special charachters.")
            print("If price is $2.00 then enter: 200")
            print("-" * 39)
            newprice = input('Enter product price:  ')
            if len(newprice) > 2:
                if isinstance(int(newprice), int):
                    trying = False
                    return newprice
            else:
                raise TypeError("Price must be integer of at least 3 digits.")
        except TypeError as err:
            print(err)

def newpbrand():
    trying = True
    while trying:
        try:
            print("-" * 39)
            newbrand = input("Enter brand's name of your product :  ")
            if models.brandchecker(newbrand):
                trying = False
                print(models.brandchecker(newbrand))
                print("### this returns a brand id from existing product")
                return models.brandchecker(newbrand).brand_id()
            else:
                trying = False
                return Brands(brand_name = newbrand.title())
        except TypeError as err:
            print(err)
            print("Please try again...")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    startapp()
