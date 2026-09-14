import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime


# ==========================================
# BANK MANAGEMENT SYSTEM
# PROFESSIONAL GUI VERSION
# ==========================================


FILE_NAME = "accounts.json"


# ==========================================
# DATA FUNCTIONS
# ==========================================

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except:
            return {}
    return {}


def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(accounts, file, indent=4)


accounts = load_data()


# ==========================================
# CREATE ACCOUNT
# ==========================================

def create_account():

    window = tk.Toplevel(root)
    window.title("Create New Account")
    window.geometry("450x500")

    tk.Label(
        window,
        text="CREATE NEW ACCOUNT",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    fields = {}

    labels = [
        "Account Number",
        "Account Holder Name",
        "4-Digit PIN",
        "Initial Deposit"
    ]

    for label in labels:

        tk.Label(
            window,
            text=label,
            font=("Arial", 11)
        ).pack()

        entry = tk.Entry(
            window,
            width=35,
            font=("Arial", 11)
        )

        if label == "4-Digit PIN":
            entry.config(show="*")

        entry.pack(pady=6)

        fields[label] = entry


    def save_account():

        acc_no = fields["Account Number"].get().strip()
        name = fields["Account Holder Name"].get().strip()
        pin = fields["4-Digit PIN"].get().strip()
        balance = fields["Initial Deposit"].get().strip()

        if not acc_no or not name or not pin or not balance:
            messagebox.showerror(
                "Error",
                "Please fill all fields!"
            )
            return

        if not acc_no.isdigit():
            messagebox.showerror(
                "Error",
                "Account Number must contain only digits!"
            )
            return

        if acc_no in accounts:
            messagebox.showerror(
                "Error",
                "Account already exists!"
            )
            return

        if len(pin) != 4 or not pin.isdigit():
            messagebox.showerror(
                "Error",
                "PIN must be exactly 4 digits!"
            )
            return

        try:
            balance = float(balance)

            if balance <= 0:
                raise ValueError

        except:
            messagebox.showerror(
                "Error",
                "Enter valid deposit amount!"
            )
            return

        created_time = datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )

        accounts[acc_no] = {
            "name": name,
            "pin": pin,
            "balance": balance,
            "transactions": [
                f"Account Created | {created_time}"
            ]
        }

        save_data()

        messagebox.showinfo(
            "Success",
            "Account Created Successfully!"
        )

        window.destroy()


    tk.Button(
        window,
        text="CREATE ACCOUNT",
        font=("Arial", 11, "bold"),
        width=22,
        height=2,
        command=save_account
    ).pack(pady=25)


# ==========================================
# DEPOSIT MONEY
# ==========================================

def deposit_money():

    window = tk.Toplevel(root)
    window.title("Deposit Money")
    window.geometry("400x400")

    tk.Label(
        window,
        text="DEPOSIT MONEY",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(window, text="Account Number").pack()

    acc_entry = tk.Entry(window, width=30)
    acc_entry.pack(pady=5)

    tk.Label(window, text="PIN").pack()

    pin_entry = tk.Entry(
        window,
        width=30,
        show="*"
    )

    pin_entry.pack(pady=5)

    tk.Label(window, text="Deposit Amount").pack()

    amount_entry = tk.Entry(window, width=30)

    amount_entry.pack(pady=5)


    def deposit():

        acc_no = acc_entry.get().strip()
        pin = pin_entry.get().strip()

        if acc_no not in accounts:
            messagebox.showerror(
                "Error",
                "Account not found!"
            )
            return

        if pin != accounts[acc_no]["pin"]:
            messagebox.showerror(
                "Error",
                "Wrong PIN!"
            )
            return

        try:
            amount = float(amount_entry.get())

            if amount <= 0:
                raise ValueError

        except:
            messagebox.showerror(
                "Error",
                "Enter valid amount!"
            )
            return

        accounts[acc_no]["balance"] += amount

        time = datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )

        accounts[acc_no]["transactions"].append(
            f"Deposited Rs.{amount} | {time}"
        )

        save_data()

        messagebox.showinfo(
            "Success",
            f"Rs.{amount} deposited successfully!"
        )

        window.destroy()


    tk.Button(
        window,
        text="DEPOSIT",
        width=20,
        height=2,
        command=deposit
    ).pack(pady=25)


# ==========================================
# WITHDRAW MONEY
# ==========================================

def withdraw_money():

    window = tk.Toplevel(root)
    window.title("Withdraw Money")
    window.geometry("400x400")

    tk.Label(
        window,
        text="WITHDRAW MONEY",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(window, text="Account Number").pack()

    acc_entry = tk.Entry(window, width=30)
    acc_entry.pack(pady=5)

    tk.Label(window, text="PIN").pack()

    pin_entry = tk.Entry(
        window,
        width=30,
        show="*"
    )

    pin_entry.pack(pady=5)

    tk.Label(window, text="Withdraw Amount").pack()

    amount_entry = tk.Entry(window, width=30)
    amount_entry.pack(pady=5)


    def withdraw():

        acc_no = acc_entry.get().strip()
        pin = pin_entry.get().strip()

        if acc_no not in accounts:
            messagebox.showerror(
                "Error",
                "Account not found!"
            )
            return

        if pin != accounts[acc_no]["pin"]:
            messagebox.showerror(
                "Error",
                "Wrong PIN!"
            )
            return

        try:
            amount = float(amount_entry.get())

            if amount <= 0:
                raise ValueError

        except:
            messagebox.showerror(
                "Error",
                "Enter valid amount!"
            )
            return

        if amount > accounts[acc_no]["balance"]:

            messagebox.showerror(
                "Error",
                "Insufficient Balance!"
            )
            return

        accounts[acc_no]["balance"] -= amount

        time = datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )

        accounts[acc_no]["transactions"].append(
            f"Withdrawn Rs.{amount} | {time}"
        )

        save_data()

        messagebox.showinfo(
            "Success",
            f"Rs.{amount} withdrawn successfully!"
        )

        window.destroy()


    tk.Button(
        window,
        text="WITHDRAW",
        width=20,
        height=2,
        command=withdraw
    ).pack(pady=25)


# ==========================================
# CHECK BALANCE
# ==========================================

def check_balance():

    acc_no = simple_input(
        "Check Balance",
        "Enter Account Number:"
    )

    if not acc_no:
        return

    if acc_no not in accounts:

        messagebox.showerror(
            "Error",
            "Account not found!"
        )

        return

    pin = simple_input(
        "PIN Verification",
        "Enter PIN:",
        True
    )

    if pin != accounts[acc_no]["pin"]:

        messagebox.showerror(
            "Error",
            "Wrong PIN!"
        )

        return

    messagebox.showinfo(
        "Current Balance",
        f"Account Holder: {accounts[acc_no]['name']}\n\n"
        f"Current Balance: Rs.{accounts[acc_no]['balance']}"
    )


# ==========================================
# SIMPLE INPUT WINDOW
# ==========================================

def simple_input(title, label, password=False):

    result = {"value": None}

    window = tk.Toplevel(root)

    window.title(title)

    window.geometry("350x180")

    tk.Label(
        window,
        text=label,
        font=("Arial", 12)
    ).pack(pady=20)

    entry = tk.Entry(
        window,
        width=30
    )

    if password:
        entry.config(show="*")

    entry.pack(pady=5)


    def submit():

        result["value"] = entry.get().strip()

        window.destroy()


    tk.Button(
        window,
        text="Submit",
        command=submit
    ).pack(pady=15)

    root.wait_window(window)

    return result["value"]


# ==========================================
# ACCOUNT DETAILS
# ==========================================

def account_details():

    acc_no = simple_input(
        "Account Details",
        "Enter Account Number:"
    )

    if acc_no not in accounts:

        messagebox.showerror(
            "Error",
            "Account not found!"
        )

        return

    pin = simple_input(
        "PIN Verification",
        "Enter PIN:",
        True
    )

    if pin != accounts[acc_no]["pin"]:

        messagebox.showerror(
            "Error",
            "Wrong PIN!"
        )

        return

    data = accounts[acc_no]

    messagebox.showinfo(
        "Account Details",
        f"Account Number: {acc_no}\n"
        f"Name: {data['name']}\n"
        f"Balance: Rs.{data['balance']}"
    )


# ==========================================
# TRANSACTION HISTORY
# ==========================================

def transaction_history():

    acc_no = simple_input(
        "Transaction History",
        "Enter Account Number:"
    )

    if acc_no not in accounts:

        messagebox.showerror(
            "Error",
            "Account not found!"
        )

        return

    pin = simple_input(
        "PIN Verification",
        "Enter PIN:",
        True
    )

    if pin != accounts[acc_no]["pin"]:

        messagebox.showerror(
            "Error",
            "Wrong PIN!"
        )

        return

    history = accounts[acc_no]["transactions"]

    if not history:

        messagebox.showinfo(
            "History",
            "No transactions found!"
        )

        return

    window = tk.Toplevel(root)

    window.title("Transaction History")

    window.geometry("600x400")

    tk.Label(
        window,
        text="TRANSACTION HISTORY",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    text_box = tk.Text(
        window,
        width=65,
        height=18
    )

    text_box.pack(pady=10)

    for transaction in history:

        text_box.insert(
            tk.END,
            transaction + "\n"
        )

    text_box.config(state="disabled")


# ==========================================
# TRANSFER MONEY
# ==========================================

def transfer_money():

    window = tk.Toplevel(root)

    window.title("Transfer Money")

    window.geometry("450x450")

    tk.Label(
        window,
        text="TRANSFER MONEY",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    labels = [
        "Sender Account Number",
        "Sender PIN",
        "Receiver Account Number",
        "Amount"
    ]

    entries = []

    for label in labels:

        tk.Label(
            window,
            text=label
        ).pack()

        entry = tk.Entry(
            window,
            width=30
        )

        if label == "Sender PIN":
            entry.config(show="*")

        entry.pack(pady=5)

        entries.append(entry)


    def transfer():

        sender = entries[0].get().strip()
        pin = entries[1].get().strip()
        receiver = entries[2].get().strip()

        if sender not in accounts:

            messagebox.showerror(
                "Error",
                "Sender account not found!"
            )

            return

        if receiver not in accounts:

            messagebox.showerror(
                "Error",
                "Receiver account not found!"
            )

            return

        if sender == receiver:

            messagebox.showerror(
                "Error",
                "Cannot transfer to same account!"
            )

            return

        if pin != accounts[sender]["pin"]:

            messagebox.showerror(
                "Error",
                "Wrong PIN!"
            )

            return

        try:

            amount = float(entries[3].get())

            if amount <= 0:
                raise ValueError

        except:

            messagebox.showerror(
                "Error",
                "Enter valid amount!"
            )

            return

        if amount > accounts[sender]["balance"]:

            messagebox.showerror(
                "Error",
                "Insufficient Balance!"
            )

            return

        accounts[sender]["balance"] -= amount

        accounts[receiver]["balance"] += amount

        time = datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )

        accounts[sender]["transactions"].append(
            f"Transferred Rs.{amount} to {receiver} | {time}"
        )

        accounts[receiver]["transactions"].append(
            f"Received Rs.{amount} from {sender} | {time}"
        )

        save_data()

        messagebox.showinfo(
            "Success",
            "Money transferred successfully!"
        )

        window.destroy()


    tk.Button(
        window,
        text="TRANSFER",
        width=20,
        height=2,
        command=transfer
    ).pack(pady=25)


# ==========================================
# ACCOUNT SUMMARY
# ==========================================

def account_summary():

    acc_no = simple_input(
        "Account Summary",
        "Enter Account Number:"
    )

    if acc_no not in accounts:

        messagebox.showerror(
            "Error",
            "Account not found!"
        )

        return

    pin = simple_input(
        "PIN Verification",
        "Enter PIN:",
        True
    )

    if pin != accounts[acc_no]["pin"]:

        messagebox.showerror(
            "Error",
            "Wrong PIN!"
        )

        return

    data = accounts[acc_no]

    messagebox.showinfo(
        "Account Summary",
        f"Account Number: {acc_no}\n"
        f"Name: {data['name']}\n"
        f"Current Balance: Rs.{data['balance']}\n"
        f"Total Transactions: "
        f"{len(data['transactions'])}"
    )


# ==========================================
# MAIN APPLICATION
# ==========================================

root = tk.Tk()

root.title("Bank Management System")

root.geometry("850x650")

root.resizable(False, False)


# HEADER

header = tk.Frame(
    root,
    height=120
)

header.pack(
    fill="x"
)


tk.Label(
    header,
    text="🏦 BANK MANAGEMENT SYSTEM",
    font=("Arial", 26, "bold")
).pack(pady=20)


tk.Label(
    header,
    text="Secure • Fast • Simple Banking",
    font=("Arial", 12)
).pack()


# MAIN DASHBOARD

dashboard = tk.Frame(root)

dashboard.pack(
    pady=30
)


features = [

    ("Create Account", create_account),

    ("Deposit Money", deposit_money),

    ("Withdraw Money", withdraw_money),

    ("Check Balance", check_balance),

    ("Account Details", account_details),

    ("Transaction History", transaction_history),

    ("Transfer Money", transfer_money),

    ("Account Summary", account_summary)

]


row = 0
col = 0


for text, command in features:

    button = tk.Button(
        dashboard,
        text=text,
        font=("Arial", 12, "bold"),
        width=24,
        height=3,
        command=command
    )

    button.grid(
        row=row,
        column=col,
        padx=15,
        pady=12
    )

    col += 1

    if col == 2:

        col = 0

        row += 1


# EXIT BUTTON

tk.Button(
    root,
    text="EXIT APPLICATION",
    font=("Arial", 12, "bold"),
    width=25,
    height=2,
    command=root.destroy
).pack(pady=10)


# FOOTER

tk.Label(
    root,
    text="© 2026 Bank Management System | Python Mini Project",
    font=("Arial", 10)
).pack(pady=10)


root.mainloop()