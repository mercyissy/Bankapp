import mysql.connector as sql
import random
import pwinput

mycon =  sql.connect(
    host = '127.0.0.1',
    user = 'root', 
    password = '',
    database = 'bankdata' 
)

mycursor = mycon.cursor()
mycon.autocommit = True

# mycursor.execute("CREATE DATABASE bankdata")
# print('Database created')

# mycursor.execute('DROP TABLE transaction')

# mycursor.execute("CREATE TABLE customer(customer_id INT PRIMARY KEY AUTO_INCREMENT, fullname VARCHAR(50), email VARCHAR(50) UNIQUE, address VARCHAR(500),gender VARCHAR(10), phone_number VARCHAR(14) UNIQUE, account_number VARCHAR(10) UNIQUE, date_created DATETIME DEFAULT CURRENT_TIMESTAMP)")
# print('Table created')
# mycursor.execute('DROP TABLE transaction')

# mycursor.execute("CREATE TABLE transaction(transaction_id INT PRIMARY KEY AUTO_INCREMENT, receiver VARCHAR(50), email VARCHAR(50), sender VARCHAR(50), amount FLOAT, transaction_type VARCHAR(50), transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP)")
# print('Table created')

# mycursor.execute('ALTER TABLE customer ADD(gender VARCHAR(10))')
# print('column updated')


# mycursor.execute('ALTER TABLE customer ADD(account_balance FLOAT(15))')
# print('column updated')

# mycursor.execute("ALTER TABLE customer ADD(password VARCHAR(50))")
# print('column updated')

# mycursor.execute("SHOW COLUMNS FROM customer")
# for column in mycursor:
#    print(column)

class Bankapp():
   def __init__(self):  
      self.name = "Bankapp"
      self.email = ''
      self.fullname = ''
      self.account_number = ''
      self.balance = 0



      
   def dashboard(self):
       print( '''
        Welcome to kUDA APP
              
        1. Register
        2. Login
        3. ForgetPassword
        #. Exit
        ''')
       
       option = input('option: ')
       if option == '1':
            self.Register()
       elif option == '2':
            self.Login()
       elif option == '3':
            self.Forgetpassword()
       elif option == '#':
            exit()
       else:
            print('Invalid option')
            self.dashboard()

   def dashboard2(self):
       print('''
            1. Deposit
            2. Withdraw
            3. Balance
            4. Transfer
            5. Transaction History
            6. Changepassword
            #. Exit

         ''')
       
       option = input('option: ')
       if option == '1':
           self.Deposit()
       elif option == '2':
           self.Withdraw()
       elif option == '3':
           self.Balance()
       elif option == '4':
            self.Transfer()
       elif option == '5':
           self.History()
       elif option == '6':
            self.Changepassword()
       elif option == '#':
             exit()  

   def Register(self):
       fullname = input('Fullname: ')
       email = input('Email: ')
       address = input('Address: ')
       gender = input('Gender: ')
       phone_numb = input('Phone number: ')
       password = input('Password: ')
       account_number = random.randint(30200000000,  30299999999)
       balance =  0


       query = "INSERT INTO customer(fullname, email, address, gender, phone_number, password, account_number, account_balance) VALUE(%s, %s, %s, %s, %s, %s, %s, %s)"
       values = (fullname, email, address, gender, phone_numb, password, account_number, balance)
       mycursor.execute(query, values)
       print(f"Registration successful\nYour account number  is: {account_number}")
       self.dashboard()

   def Login(self):
       self.email = input('Email: ')
       password = pwinput.pwinput()


       query =  "SELECT fullname, email, password, account_number, account_balance FROM customer WHERE email = %s AND password = %s"
       val = (self.email, password)
       mycursor.execute(query, val)
       details = mycursor.fetchone()
       if details:
           self.fullname = details[0]
           self.account_number = details[3]
           self.balance = details[4]
           print('Login successful..')
           self.dashboard2()

       else:
           print('Incorrect email or password.\nKindly input the correct details')
           self.dashboard()

   def Forgetpassword(self):
        while True:
            email = input("Email: ").strip()

    # Trying to Check if the email exists in the database
            query = "SELECT password FROM customer WHERE email = %s"
            val = (email,)
            mycursor.execute(query, val)
            psw = mycursor.fetchone()

            if not psw:
                print("Incorrect email. Please try again.")
            else:
                break

    # Trying to Get a new password from the user
        while True:
            newPassword = input("New Password: ").strip()
            retrypsw = input("Enter New Password Again: ").strip()

            if newPassword != retrypsw:
                print("Passwords do not match. Please try again.")
            else:
                break

    # Trying to Update the password in the database
        query2 = "UPDATE customer SET password = %s WHERE email = %s"
        val2 = (newPassword, email)
        mycursor.execute(query2, val2)
        print("Password successfully modified.")

        input("Press Enter to return to the homepage.")
        self.dashboard()


   def Deposit(self):
       query = "SELECT account_balance FROM customer WHERE email = %s"
       val = (self.email,)
       mycursor.execute(query, val)
       detail = mycursor.fetchone()
       balance = detail[0]

       depo = float((input('Enter amount to deposit: ')))
       new_balance = balance + depo


       query2 = "UPDATE customer SET account_balance = %s WHERE email = %s"
       val2 = (new_balance, self.email)
       mycursor.execute(query2, val2)
       self.balance = new_balance
       print(f'Deposit of #{depo} is successful\nYour current account balance is #{self.balance}')
       
       query3 = "INSERT INTO transaction (transaction_type, amount, sender, email) VALUES (%s, %s, %s, %s)"
       val3 = ('DEPOSIT', depo, self.fullname, self.email)
       mycursor.execute(query3, val3)

       print(f"Successfully transferred #{depo:.2f} to {self.account_number}.\nYour new balance is #{self.balance:.2f}.")
       self.dashboard2()
       self.option = input('press 1 to continue or 2 to logout: ')
       if self.option == '1':
           self.dashboard2()
       else:
           print("signing out ...")

       

   def Withdraw(self):
    # Step 1: Fetch the current account balance for the user
    query = "SELECT account_balance FROM customer WHERE email = %s"
    val = (self.email,)
    mycursor.execute(query, val)
    detail = mycursor.fetchone()
    if not detail:
        print("Account not found.")
        return
    
    balance = detail[0]

    # Step 2: Ask for withdrawal amount
    try:
        withdraw = float(input('Enter amount to withdraw: '))
    except ValueError:
        print("Invalid input. Please enter a valid amount.")
        return

    # Step 3: Check if the balance is sufficient for withdrawal
    if balance >= withdraw:
        # Step 4: Calculate new balance after withdrawal
        new_balance = balance - withdraw

        # Step 5: Update the account balance in the database
        query2 = "UPDATE customer SET account_balance = %s WHERE email = %s"
        val2 = (new_balance, self.email)
        try:
            mycursor.execute(query2, val2)
            self.balance = new_balance  # Update local balance after withdrawal
        except Exception as e:
            print(f"An error occurred while updating balance: {e}")
            return
        
        # Step 6: Log the transaction in the transaction table
        query3 = "INSERT INTO transaction (transaction_type, amount, sender, receiver,  email) VALUES (%s, %s, %s, %s, %s)"
        val3 = ('Withdraw', withdraw, self.fullname, self.fullname, self.email)

        mycursor.execute(query3, val3)
        
        print(f'Withdrawal of #{withdraw} from account {self.account_number} was successful.')
        print(f'Your current account balance is #{self.balance}')

    else:
        print("Insufficient fund")  
    
    # Step 7: Ask for the next action (continue or logout)
    self.option = input('Press 1 to continue or 2 to logout: ')
    if self.option == '1':
        self.dashboard2()  # Redirect to the dashboard
    else:
        print("Signing out...")

   def Transfer(self):
    # Prompt for the receiver account number
    receiver_acct = input('Enter receiver account number: ')

    # Query to get receiver's fullname and current balance
    query = "SELECT fullname, account_balance FROM customer WHERE account_number = %s"
    val = (receiver_acct,)
    mycursor.execute(query, val)
    detail = mycursor.fetchone() 

    if detail is None:
        print("Receiver account not found.")
          

    receiver_fullname, receiver_balance = detail  # Unpack fullname and balance

    # Prompt for transfer amount
    transfer = float(input('Enter amount to transfer: '))

    if self.balance >= transfer:
        # Calculate the new sender balance first, before using it
        receiver_balance = self.balance - transfer 

        # Update the receiver's account balance
        query_receiver = "UPDATE customer SET account_balance = account_balance + %s WHERE account_number = %s"
        val_receiver = (transfer, receiver_acct)
        mycursor.execute(query_receiver, val_receiver)

        # Update the sender's (current user's) account balance
        query_update_sender = "UPDATE customer SET account_balance = %s WHERE email = %s"
        val_update_sender = (receiver_balance, self.email)
        mycursor.execute(query_update_sender, val_update_sender)

        # Update the current user's balance in the instance attribute
        self.balance = receiver_balance  # Update the instance attribute

        # Print confirmation of the transaction
        print(f'Transfer of #{transfer:.2f} to {receiver_fullname} ({receiver_acct}) is successful.\nYour current account balance is #{self.balance:.2f}')

        query3 = "INSERT INTO transaction (transaction_type, amount, sender, receiver, email) VALUES (%s, %s, %s, %s, %s)"
        val3 = ('Transfer', transfer, self.fullname, receiver_fullname, self.email)
        mycursor.execute(query3, val3)

        print(f"Successfully transferred #{transfer:.2f} to {receiver_fullname}.\nYour new balance is #{self.balance:.2f}.")
        self.dashboard2()
    else:
        print('Insufficient Balance')

    # Ask user to continue or log out
    self.option = input('Press 1 to continue or 2 to logout: ')
    if self.option == '1':
        self.dashboard2()
    else:
        print("Signing out ...")


   def Balance(self):
       query = "SELECT account_balance FROM customer WHERE email = %s"
       val = (self.email,)
       mycursor.execute(query, val)
       detail = mycursor.fetchone()
       balance = detail[0]
       new_balance = balance

       print(f'Dear {self.fullname}, your account balance is: #{new_balance}')


   def Changepassword(self):
    email = input('Email: ').strip()
    prevPassword = input('Old Password: ').strip()
    newPassword = input('New Password: ').strip()

    query = "UPDATE customer SET password = %s WHERE password = %s AND email = %s"
    val = (newPassword, prevPassword, email)
    mycursor.execute(query, val)
    print('Password changed')
    self.dashboard()

   def History(self):
    print(f'Transaction History for {self.fullname}')
    
    # Define the SQL query to fetch transaction history
    query = "SELECT transaction_type, amount, sender, receiver, transaction_date FROM transaction WHERE email = %s"
    val = (self.email,)  # Ensure val is a tuple
    
    try:
        # Execute the query
        mycursor.execute(query, val)
        history = mycursor.fetchall()

        if not history:
            print("No transaction history found")
            
        else:
            print("\nType       Amount     Sender               Receiver     Date/Time")
            print('-' * 75)  # Adjusted to match the width of the columns
            for record in history:
                transaction_type, amount, sender, receiver, transaction_date = record
                receiver = receiver if receiver else "N/A"
                print(f"{transaction_type:<10} {amount:<10} {sender:<20} {receiver:<20} {transaction_date}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    input('\nPress Enter to return to dashboard...')
    self.dashboard2()  # Ensure this method is correctly defined


            
dash = Bankapp()
dash.dashboard()       