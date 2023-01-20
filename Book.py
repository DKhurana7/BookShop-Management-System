import mysql.connector as cntr
import datetime as dt
import os
from random import shuffle
from tempfile import mktemp
from os import system, startfile
import matplotlib.pyplot as plt

db = cntr.connect(host = 'localhost' , user = 'root' , passwd = 'abcd1234' , database = 'shop_management')
cur = db.cursor(buffered=True)
db.autocommit = True


#Function to check is it leap year
is_leapyear = lambda year : year % 4 == 0


#Function to get last date of month
def last_month(month , year):
    if month in (1,3,5,7,8,10,12) : return 31
    elif month == 2 and is_leapyear(year) : return 29
    elif month == 2 : return 28
    else : return 30
    

clrscreen = lambda: os.system('cls' if os.name=='nt' else 'clear')


def view_stock() :
    cur.execute("select Book_No , Book_Name , Available_Stock from stock")
    data = cur.fetchall()
    print("{:15s} {:25s} {:10s}" \
        .format("Book Number", "Book Name", "Stock")) 
    for row in data :
         print (str(row[0]).ljust(15," "),row[1].ljust(25," "),row[2])           

            
def add_stock() :            
    print('Add Stock'.center(89 , '='))
    bno = unique_book_no()
    if bno :
        print("Book Number : " , bno)
    else :
        bno = 10000
        print("Book Number : " , bno)
    bname = input("Enter the Book\'s Name : ")
    auth = input("Enter the Author of the Book : ")
    publ = input("Enter the Publisher of the Book : ")
    cost = eval(input("Enter the Cost per Book : "))
    stock = int(input("Enter the Quantity purchased : "))
    cur.execute("insert into stock values ({} , '{}' , '{}' , '{}' , {} , {} , {} , '{}')" \
                .format(bno , bname , auth , publ , cost , stock , 0, dt.date.today()))
    print("Inserted Sucessfully !!!")
    

        
def add_user() :
    user = input("Enter the user name : ")
    passwd = input("Enter a Password : ")
    passwd2 = input("Enter Password to confirm : ")
    if passwd == passwd2 :
        cur.execute("insert into users values('{}' , '{}')".format(user , passwd))
        print("Created Successfully!!!")
    elif passwd != passwd2 : print("You've entered different passwords")
    
def sell_book() :
    print('Purchase')
    cname = input("Enter the Customer Name : ")
    phno = int(input("Enter the phone number : "))
    bno = int(input("Enter book number : "))
    cur.execute("select Book_Name, Cost_per_Book from stock where Book_No = {}".format(bno))
    data=cur.fetchall()
    if cur.rowcount == 1 :
        bname = data[0][0]
        cost = data[0][1]
    else :
        print ("Book Not Found")
        return False
    print ("Book Name : ", bname)          
    cost = cost *1.1
    print ("Book Cost : ", str(cost))          
    cur.execute("insert into purchased values({} , '{}')".format(bno , dt.date.today()))
    cur.execute("update stock set qty_purchased = qty_purchased + 1 where Book_No = {}".format(bno))
    cur.execute("update stock set Available_Stock = Available_Stock - 1 where Book_No = {}".format(bno))
    print("Transaction Completed")
    q = '''Book Shop\nName : {}\nPhone No : {}\nBook Number : {}\nBook Name : {}\nCost : {}\nDate Of Purchase : {}''' \
    .format(cname , phno , bno , bname , cost , dt.date.today())
    filename = mktemp('.txt')
    open(filename , 'w').write(q)
    startfile(filename , 'print')
    cur.execute('select Book_Name , Book_No , Author from stock where Available_Stock = 0')
    if cur.rowcount == 1 :
        print("STOCK OF ")
        print("Book Name : " , cur.fetchall()[0][0])
        print("Book Number : " , cur.fetchall()[0][1])
        print("Author : " , cur.fetchall()[0][2])
        print("EXHAUSTED")
        cur.execute('delete from stock where Available_Stock = 0')
    
        
        
def unique_book_no () :
    cur.execute("select max(Book_No) from stock")
    data = cur.fetchall()
    if bool(data[0][0]) :
         return data[0][0] + 1
    else : return False

def view_sales () :
    print('Overall Sales This Month')        
    cur.execute("select distinct(s.Book_Name) , s.qty_purchased from stock s , purchased p where \
    s.Book_No = p.Book_No and p.purchased_on between '{year}-{month}-01' and '{year}-{month}-{date}'" \
    .format(year = dt.date.today().year , month = dt.date.today().month , \
    date = last_month(dt.date.today().month , dt.date.today().year)))
    data = cur.fetchall()
    L1 , L2 = [] , []
    for row in data :
        L1.append(row[0])
        L2.append(row[1])
    plt.bar(L1 , L2)
    plt.xlabel('Books')
    plt.ylabel('Sales')
    plt.title('Sales')
    plt.show()    

def login():
    user = input("Enter the username : ")
    pwd = input("Enter the password : ")
    cur.execute("Select * from users where (username = '{}' and password = '{}')".format(user , pwd))
    if cur.rowcount : return True

def update_stock() :
    bno = int(input("Enter the book number : "))
    cur.execute("select Book_Name , Available_Stock from stock where Book_No = {}".format(bno))
    data = cur.fetchall()
    print("Book Name : " , data[0][0])
    print("Available Stock : " , data[0][1])
    stock = int(input("Enter the new stock purchased : "))
    cur.execute("update stock set Available_Stock = Available_Stock + {}".format(stock) + " where Book_No = {}".format(bno))
    print("Updated Successfully")

    
    
