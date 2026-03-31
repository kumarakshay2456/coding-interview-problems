class BankAccount:
    def __init__(self, owner) -> None:
        self.owner = owner
        self.__balance = 0
    
    def deposit(self, amount):
        self.__balance += amount
        print(f"Deposited {amount}. New balance is {self.__balance}")
    
    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient funds")
        else:
            self.__balance -= amount
            print(f"Withdrew {amount}. New balance is {self.__balance}")
    
    def get_balance(self):
        return self.__balance

bank = BankAccount("Akshay")
print("Initial Balance:", bank.get_balance())
print("Depositing 1000", bank.deposit(1000))
print("Withdrawing 200", bank.withdraw(200))
print("Final Balance:", bank.get_balance())
print("Trying to access balance directly:", bank.get_balance)


class 



