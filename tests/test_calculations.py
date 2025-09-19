import pytest
from app.calculations import add,sub,multi,div,Bank,InsufficientException

@pytest.fixture
def zero_bank_account():
    return Bank()

@pytest.fixture
def bank_account():
    return Bank(50)

@pytest.mark.parametrize("n1,n2,expected",[
    (3,2,5),
    (4,2,6),
    (7,8,15)
])
def test_add(n1,n2,expected):
    assert  add(n1,n2) == expected

def test_sub():
    assert sub(5,3) == 2

def test_multi():
    assert multi(5,3) == 15

def test_div():
    assert div(6,2) == 3

def test_bank_set_initial_amount(bank_account):
    # bank_account=Bank(50)
    assert bank_account.balance == 50 

def test_bank_default_ammount(zero_bank_account):
    # bank_account = Bank()
    assert zero_bank_account.balance == 0

def test_bank_deposite_amount(bank_account):
    # bank_account = Bank(50)
    bank_account.deposite(50) 
    assert bank_account.balance == 100

def test_bank_withdrawl_amount(bank_account):
    # bank_account = Bank(50)
    bank_account.withdraw(50)
    assert bank_account.balance == 0

def test_bank_collect_interest(bank_account):
    # bank_account =Bank(50)
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 55

@pytest.mark.parametrize("deposited,withdrew,expected",[
    (300,200,100),
    (80,20,60),
    (7000,1000,6000)
])
def test_bank_transaction(zero_bank_account,deposited,withdrew,expected):
    zero_bank_account.deposite(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientException):
        bank_account.withdraw(200)
