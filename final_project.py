from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Transaction:
    name: str
    money: float
    percent: float

def get_budget() -> float:
    '''takes a budget float value as an input from the user'''
    budget = float(input("Enter a budget (a float): "))
    return budget

def get_amount() -> float:
    '''prompts the user for a float and returns that float'''
    return float(input("Enter a money amount (float); "))

def get_name() -> str:
    '''prompts the user for a string and returns that string'''
    return str(input("Enter a transaction name (STOP to stop): "))

def make_transactions() -> list[Transaction]:
    '''Takes a name string value and a money float value from the user as inputs
    until the user enters STOP, then turns the values into a list of transactions,
    with 0.0 as a placeholder value for the percent'''
    name = ""
    value = 0.0
    names = []
    values = []
    while name != "STOP":
        name = get_name()
        if name != "STOP":
            value = get_amount()
            names.append(name)
            values.append(value)
    transactions = []
    count = 0
    for name in names:
        transactions.append(Transaction(name, values[count], 0.0))
    return transactions

def check_transactions(transactions: list[Transaction], budget: float) -> str:
    '''takes a list of transactions and a budget (float), returning "No Transactions!" if
    the transaction list is empty, or returning "Budget exceeded!" if the total money
    spent exceeds the budget. Returns an empty string otherwise.'''
    if not transactions:
        return "No Transactions!"
    total_spent = 0.0
    for transaction in transactions:
        total_spent += transaction.money
    if total_spent > budget:
        return "Budget exceeded!"
    return ""
assert_equal(check_transactions([], 1.0), "No Transactions!")
assert_equal(check_transactions([Transaction("poop", 2.0, 0.0)], 1.0), "Budget exceeded!")
assert_equal(check_transactions([Transaction("pee", 1.0, 0.0)], 1.0), "")

def calculate_percents(transactions: list[Transaction], budget: float) -> list[Transaction]:
    '''consumes a list of Transactions and a budget (float), returning a new list of
    Transactions with the 0.0 placeholder precent value replaced with the percent of
    the budget that transaction's money value is'''
    new_list = []
    percent = 0.0
    if budget == 0.0:
        return []
    for transaction in transactions:
        percent = (transaction.money / budget) * 100
        new_list.append(Transaction(transaction.name, transaction.money, percent))
    return new_list
assert_equal(calculate_percents([], 0.0), [])
assert_equal(calculate_percents([Transaction("poop", 10.0, 0.0), Transaction("pee", 20.0, 0.0)], 100.0), [Transaction("poop", 10.0, 10.0), Transaction("pee", 20.0, 20.0)])

def play():
    '''Generates the transaction list and displays it, with the budget'''
    budget = get_budget()
    transactions = calculate_percents(make_transactions(), budget)
    if check_transactions(transactions, budget) == "":
        print("Budget: " + str(budget) + "\n")
        count = 0
        for transaction in transactions:
            count += 1
            print(str(count) + ": Name: " + str(transaction.name) +", Amount: $", str(transaction.money) + ", Percent of budget: " + str(transaction.percent) + "% \n")
    else:
        return check_transactions(transactions, budget)

#play()
#above line would run this code in the shell if uncommented
