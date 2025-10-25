import pytest
from app.calculations import add, BankAccount, InsufficientFunds


# This is to stop repeating bank account instance


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [(3, 2, 5)])


# def test_add():
#     print("testing add func")
#     sum = add(4, 4)
#     assert sum == 8


def test_add2(num1, num2, expected):

    sum = add(num1, num2)
    assert sum == expected


def test_bank_set_initial_amount(bank_account):
    # bank_account = BankAccount(50)

    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    #  bank_accounts = BankAccount()

    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    # bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    # bank_account = BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_collect_interest(bank_account):
    # bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55


@pytest.mark.parametrize(
    "deposited, withdrew, expected_amount",
    [
        (200, 100, 100),
        (50, 10, 40),
        (1200, 200, 1000),
        # (10, 50, -40),
    ],
)
# def test_bank_transaction(zero_bank_account):
#     zero_bank_account.deposit(200)
#     zero_bank_account.withdraw(100)

#     assert zero_bank_account.balance == 100


def test_bank_transaction(zero_bank_account, deposited, withdrew, expected_amount):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)

    assert zero_bank_account.balance == expected_amount

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)





#Pytest commands

#pytest tests/ -v  #To run tests
#pytest -s  #To show prints statements
#pytest tests/my_test.py -k test_add2 -v  #To run a specific test function
#pytest --disable-warnings  #To disable warnings
#pytest -x to make the test stop at first failure
#pytest -v -s tests/app_test_users.py To run specific test file with print statements and verbose