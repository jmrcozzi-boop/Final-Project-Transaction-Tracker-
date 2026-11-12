from dataclasses import dataclass
from drafter import *

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
#^would run code outside of drafter if uncmmented 

'''DRAFTER CODE'''
@dataclass
class State:
    """Store the information used by the Budget Tracker website."""
    budget: float
    transactions: list[final_project.Transaction]
    names: list[str]
    money_amounts: list[float]
    percents: list[float]
    entry_finished: bool


def get_total_spent(state: State) -> float:
    """Calculate the total amount spent on all transactions."""
    total_spent = 0.0
    for transaction in state.transactions:
        total_spent += transaction.money
    return total_spent


def get_remaining_budget(state: State) -> float:
    """Calculate the amount of money remaining in the budget."""
    return state.budget - get_total_spent(state)


def update_percentages(state: State) -> None:
    """Calculate and save the percentage for each transaction."""
    state.transactions = final_project.calculate_percents(
        state.transactions,
        state.budget
    )
    state.percents = []
    for transaction in state.transactions:
        state.percents.append(transaction.percent)


def make_summary(state: State) -> list:
    """Create the content for the transaction summary page."""
    content = [
        Header("Budget Summary"),
        "Starting budget: $" + format(state.budget, ".2f"),
        Header("Your Transactions")
    ]

    count = 0
    for transaction in state.transactions:
        count += 1
        content.append(
            str(count) + ". " + transaction.name +
            " - $" + format(transaction.money, ".2f") +
            " (" + format(transaction.percent, ".2f") + "%)"
        )

    total_spent = get_total_spent(state)
    remaining = get_remaining_budget(state)

    content.extend([
        Header("Financial Summary"),
        "Total spent: $" + format(total_spent, ".2f"),
        "Remaining budget: $" + format(remaining, ".2f")
    ])
    return content


def transaction_entry_page(state: State, message: str = "") -> Page:
    """Create the page where users enter their transactions."""
    content = [
        Header("Enter Your Transactions"),
        "Current budget: $" + format(state.budget, ".2f"),
        "Enter the name and amount of your transaction.",
        "Enter STOP as the name when you are finished."
    ]

    if message != "":
        content.append(message)

    content.extend([
        "Transaction name:",
        TextBox("transaction_name", ""),
        "Transaction amount:",
        TextBox("amount_text", ""),
        Button("Add Transaction", "add_transaction")
    ])

    return Page(state, content)


@route
def index(state: State) -> Page:
    """Display the welcome page."""
    return Page(state, [
        Header("Budget Tracker"),
        "A simple way to keep track of your spending.",
        "Enter your budget and transactions to see how "
        "your money is being used.",
        Button("Get Started", "get_budget")
    ])


@route
def get_budget(state: State) -> Page:
    """Display the page where users enter their budget."""
    return Page(state, [
        Header("Set Your Budget"),
        "Enter the total amount of money you have available.",
        "Budget:",
        TextBox("budget_text", ""),
        Button("Continue", "save_budget")
    ])


@route
def save_budget(state: State, budget_text: str) -> Page:
    """Validate and save the user's budget."""
    try:
        budget = float(budget_text)
    except ValueError:
        return Page(state, [
            Header("Invalid Budget"),
            "Please enter a valid numerical budget.",
            TextBox("budget_text", budget_text),
            Button("Try Again", "save_budget")
        ])

    if budget <= 0:
        return Page(state, [
            Header("Invalid Budget"),
            "Your budget must be greater than zero.",
            TextBox("budget_text", budget_text),
            Button("Try Again", "save_budget")
        ])

    state.budget = budget
    state.transactions = []
    state.names = []
    state.money_amounts = []
    state.percents = []
    state.entry_finished = False

    return get_transactions(state)


@route
def get_transactions(state: State) -> Page:
    """Display the transaction entry page."""
    return transaction_entry_page(state)


@route
def add_transaction(
    state: State,
    transaction_name: str,
    amount_text: str
) -> Page:
    """Validate and add a transaction to the transaction list."""
    if state.entry_finished:
        return display_transactions(state)

    name = transaction_name.strip()

    if name.upper() == "STOP":
        return finish_transactions(state)

    if name == "":
        return transaction_entry_page(
            state, "Please enter a transaction name."
        )

    try:
        amount = float(amount_text)
    except ValueError:
        return transaction_entry_page(
            state, "Please enter a valid transaction amount."
        )

    if amount <= 0:
        return transaction_entry_page(
            state, "Transaction amounts must be greater than zero."
        )

    transaction = final_project.Transaction(name, amount, 0.0)
    state.transactions.append(transaction)
    state.names.append(name)
    state.money_amounts.append(amount)
    state.percents.append(0.0)

    return transaction_entry_page(
        state, "Transaction added successfully!"
    )


@route
def finish_transactions(state: State) -> Page:
    """Finish transaction entry and calculate percentages."""
    state.entry_finished = True
    return calculate_percents(state)


@route
def calculate_percents(state: State) -> Page:
    """Calculate transaction percentages and choose a result page."""
    if not state.transactions:
        return no_transactions(state)

    update_percentages(state)

    if final_project.check_transactions(
        state.transactions, state.budget
    ) == "Budget exceeded!":
        return too_much_spent(state)

    return display_transactions(state)


@route
def display_transactions(state: State) -> Page:
    """Display all transactions and the remaining budget."""
    if not state.transactions:
        return no_transactions(state)

    content = make_summary(state)
    content.append(Button("Start a New Budget", "restart"))
    return Page(state, content)


@route
def too_much_spent(state: State) -> Page:
    """Display a warning when spending exceeds the budget."""
    content = [
        Header("Budget Exceeded!"),
        "Your total spending is greater than your budget.",
        "You have spent more money than you planned."
    ]

    content.extend(make_summary(state))
    content.append(Button("Start a New Budget", "restart"))
    return Page(state, content)


@route
def no_transactions(state: State) -> Page:
    """Display a message when no transactions were entered."""
    return Page(state, [
        Header("No Transactions!"),
        "You did not enter any transactions.",
        "You can add transactions or start over.",
        Button("Add Transactions", "get_transactions"),
        Button("Start Over", "restart")
    ])


@route
def restart(state: State) -> Page:
    """Reset all application information and return home."""
    state.budget = 0.0
    state.transactions = []
    state.names = []
    state.money_amounts = []
    state.percents = []
    state.entry_finished = False

    return index(state)


# Unit tests

def test_get_total_spent() -> None:
    """Test that the total spending is calculated correctly."""
    state = State(
        100.0,
        [
            final_project.Transaction("Food", 20.0, 0.0),
            final_project.Transaction("Gas", 30.0, 0.0)
        ],
        ["Food", "Gas"],
        [20.0, 30.0],
        [0.0, 0.0],
        False
    )
    assert get_total_spent(state) == 50.0


def test_get_remaining_budget() -> None:
    """Test that the remaining budget is calculated correctly."""
    state = State(
        100.0,
        [final_project.Transaction("Food", 25.0, 0.0)],
        ["Food"],
        [25.0],
        [0.0],
        False
    )
    assert get_remaining_budget(state) == 75.0


def test_update_percentages() -> None:
    """Test that transaction percentages are updated correctly."""
    state = State(
        100.0,
        [
            final_project.Transaction("Food", 25.0, 0.0),
            final_project.Transaction("Gas", 50.0, 0.0)
        ],
        ["Food", "Gas"],
        [25.0, 50.0],
        [0.0, 0.0],
        False
    )

    update_percentages(state)

    assert state.transactions[0].percent == 25.0
    assert state.transactions[1].percent == 50.0
    assert state.percents == [25.0, 50.0]


def test_transaction_calculations() -> None:
    """Test the transaction functions from final_project.py."""
    transactions = [
        final_project.Transaction("Food", 25.0, 0.0),
        final_project.Transaction("Gas", 50.0, 0.0)
    ]

    assert final_project.check_transactions(
        transactions, 100.0
    ) == ""

    assert final_project.check_transactions(
        transactions, 50.0
    ) == "Budget exceeded!"

    assert final_project.check_transactions(
        [], 100.0
    ) == "No Transactions!"

    assert final_project.calculate_percents(
        transactions, 100.0
    ) == [
        final_project.Transaction("Food", 25.0, 25.0),
        final_project.Transaction("Gas", 50.0, 50.0)
    ]


def run_unit_tests() -> None:
    """Run the unit tests before starting the website."""
    test_get_total_spent()
    test_get_remaining_budget()
    test_update_percentages()
    test_transaction_calculations()
    print("All unit tests passed!")


# Run tests before launching Drafter.
run_unit_tests()


# Configure and launch the website.
set_website_title("Budget Tracker")
set_website_style("default")

set_site_information(
    "Replace with your name",
    "A simple website for tracking budgets and transactions.",
    "Original student code and the Drafter library.",
    "See the CS1 Final Project planning document in the repository.",
    []
)

start_server(
    State(0.0, [], [], [], [], False),
    open_browser=True,
    site_title="Budget Tracker",
    port=8000
)
