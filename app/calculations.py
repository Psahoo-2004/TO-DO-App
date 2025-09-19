
def add(n1:int,n2:int):
    return n1+n2
def sub(n1:int,n2:int):
    return n1-n2
def multi(n1:int,n2:int):
    return n1*n2
def div(n1:int,n2:int):
    return n1/n2

class InsufficientException(Exception):
    pass
class Bank:
    def __init__(self,starting_balance = 0):
        self.balance = starting_balance
        
    def deposite(self,amount):
        self.balance += amount
    def withdraw(self,amount):
        if self.balance<amount:
            raise InsufficientException("Insufficient funds in account")
        self.balance -= amount
    def collect_interest(self):
        self.balance *= 1.1
    
                