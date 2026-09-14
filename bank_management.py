import tkinter as tk
from tkinter import messagebox
import json
import os
import shutil
from datetime import datetime

# ==========================================
# BANK MANAGEMENT SYSTEM
# Dynamic Mini Project
# ==========================================

DATA_FILE = "accounts.json"
BACKUP_FILE = "accounts_backup.json"

# Hashing using Python Dictionary
accounts = {}


# ==========================================
# LINKED LIST FOR TRANSACTION HISTORY
# ==========================================

class TransactionNode:

    def __init__(self, data):
        self.data = data
        self.next = None


class TransactionLinkedList:

    def __init__(self):
        self.head = None

    def append(self, data):

        new_node = TransactionNode(data)

        if self.head is None:
            self.head = new_node
            return

        temp = self.head

        while temp.next is not None:
            temp = temp.next

        temp.next = new_node

    def get_all(self):

        result = []
        temp = self.head

        while temp is not None:
            result.append(temp.data)
            temp = temp.next

        return result


# ==========================================
# BST FOR SORTED ACCOUNTS
# ==========================================

class BSTNode:

    def __init__(self, account_no):

        self.account_no = account_no
        self.left = None
        self.right = None


class AccountBST:

    def __init__(self):

        self.root = None

    def insert(self, account_no):

        self.root = self._insert(
            self.root,
            account_no
        )

    def _insert(self, root, account_no):

        if root is None:
            return BSTNode(account_no)

        if account_no < root.account_no:

            root.left = self._insert(
                root.left,
                account_no
            )

        elif account_no > root.account_no:

            root.right = self._insert(
                root.right,
                account_no
            )

        return root

    def inorder(self):

        result = []

        self._inorder(
            self.root,
            result
        )

        return result

    def _inorder(self, root, result):

        if root is not None:

            self._inorder(
                root.left,
                result
            )

            result.append(root.account_no)

            self._inorder(
                root.right,
                result
            )


account_bst = AccountBST()


# ==========================================
# DATA FUNCTIONS
# ==========================================

def load_data():

    global accounts

    if os.path.exists(DATA_FILE):

        try:

            with open(DATA_FILE, "r") as file:

                accounts = json.load(file)

        except:

            accounts = {}

    else:

        accounts = {}

    rebuild_bst()


def save_data():

    with open(DATA_FILE, "w") as file:

        json.dump(
            accounts,
            file,
            indent=4
        )


def rebuild_bst():

    global account_bst

    account_bst = AccountBST()

    for account_no in accounts:

        account_bst.insert(account_no)


# ==========================================
# TRANSACTION FUNCTION
# ==========================================

def add_transaction(account_no, message):

    if "transactions" not in accounts[account_no]:

        accounts[account_no]["transactions"] = []

    date_time = datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )

    transaction = f"{date_time} - {message}"

    accounts[account_no]["transactions"].append(
        transaction
    )


# ==========================================
# GUI HELPERS
# ==========================================

def clear_window():

    for widget in root.winfo_children():

        widget.destroy()


def title_label(parent, text):

    tk.Label(
        parent,
        text=text,
        font=("Arial", 22, "bold"),
        bg="#0B3D91",
        fg="white",
        pady=18
    ).pack(fill="x")


def create_button(parent, text, command, color):

    tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 12, "bold"),
        bg=color,
        fg="white",
        width=32,
        pady=10,
        cursor="hand2"
    ).pack(pady=8)


# ==========================================
# HOME PAGE
# ==========================================

def show_home():

    clear_window()

    root.configure(bg="#EAF4FF")

    frame = tk.Frame(
        root,
        bg="white",
        bd=2,
        relief="solid"
    )

    frame.place(
        relx=0.5,
        rely=0.5,
        anchor="center",
        width=650,
        height=600
    )

    tk.Label(
        frame,
        text="🏦 BANK MANAGEMENT SYSTEM",
        font=("Arial", 24, "bold"),
        bg="white",
        fg="#0B3D91"
    ).pack(pady=(45, 10))

    tk.Label(
        frame,
        text="Dynamic Banking Application",
        font=("Arial", 15, "bold"),
        bg="white",
        fg="#555555"
    ).pack()

    tk.Label(
        frame,
        text="Python | JSON | Hashing | Linked List | BST | Sliding Window",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#4F46E5"
    ).pack(pady=25)

    create_button(
        frame,
        "👤 NEW USER REGISTRATION",
        register_user,
        "#2563EB"
    )

    create_button(
        frame,
        "🔐 USER LOGIN",
        user_login,
        "#0891B2"
    )

    create_button(
        frame,
        "👨‍💼 ADMIN LOGIN",
        admin_login,
        "#1E293B"
    )

    create_button(
        frame,
        "❌ EXIT",
        root.destroy,
        "#DC2626"
    )


# ==========================================
# USER REGISTRATION
# ==========================================

def register_user():

    clear_window()

    root.configure(bg="#EAF4FF")

    title_label(root, "👤 NEW USER REGISTRATION")

    frame = tk.Frame(root, bg="#EAF4FF")

    frame.pack(pady=30)

    fields = {}

    for label_text in [
        "Account Number",
        "Full Name",
        "Create 4 Digit PIN",
        "Initial Balance"
    ]:

        tk.Label(
            frame,
            text=label_text,
            font=("Arial", 12, "bold"),
            bg="#EAF4FF"
        ).pack()

        entry = tk.Entry(
            frame,
            font=("Arial", 13),
            width=30
        )

        if label_text == "Create 4 Digit PIN":
            entry.config(show="*")

        entry.pack(pady=7, ipady=6)

        fields[label_text] = entry


    def register():

        account_no = fields["Account Number"].get().strip()
        name = fields["Full Name"].get().strip()
        pin = fields["Create 4 Digit PIN"].get().strip()
        balance = fields["Initial Balance"].get().strip()

        if not account_no or not name or not pin or not balance:

            messagebox.showerror(
                "Error",
                "Please fill all fields!"
            )

            return

        if account_no in accounts:

            messagebox.showerror(
                "Error",
                "Account Number already exists!"
            )

            return

        if not pin.isdigit() or len(pin) != 4:

            messagebox.showerror(
                "Error",
                "PIN must be exactly 4 digits!"
            )

            return

        try:

            balance = float(balance)

            if balance < 0:
                raise ValueError

        except:

            messagebox.showerror(
                "Error",
                "Enter valid initial balance!"
            )

            return

        accounts[account_no] = {

            "name": name,
            "pin": pin,
            "balance": balance,
            "transactions": []

        }

        account_bst.insert(account_no)

        add_transaction(
            account_no,
            "New Account Created"
        )

        save_data()

        messagebox.showinfo(
            "Success",
            f"Account Created Successfully!\n\n"
            f"Welcome {name}!"
        )

        show_home()


    create_button(
        frame,
        "CREATE ACCOUNT",
        register,
        "#16A34A"
    )

    create_button(
        frame,
        "BACK TO HOME",
        show_home,
        "#64748B"
    )


# ==========================================
# USER LOGIN
# ==========================================

def user_login():

    clear_window()

    root.configure(bg="#EAF4FF")

    title_label(root, "🔐 USER LOGIN")

    frame = tk.Frame(root, bg="#EAF4FF")

    frame.pack(pady=60)

    tk.Label(
        frame,
        text="Account Number",
        font=("Arial", 12, "bold"),
        bg="#EAF4FF"
    ).pack()

    account_entry = tk.Entry(
        frame,
        font=("Arial", 13),
        width=30
    )

    account_entry.pack(pady=10, ipady=7)

    tk.Label(
        frame,
        text="PIN",
        font=("Arial", 12, "bold"),
        bg="#EAF4FF"
    ).pack()

    pin_entry = tk.Entry(
        frame,
        font=("Arial", 13),
        show="*",
        width=30
    )

    pin_entry.pack(pady=10, ipady=7)


    def login():

        account_no = account_entry.get().strip()
        pin = pin_entry.get().strip()

        if account_no not in accounts:

            messagebox.showerror(
                "Error",
                "Account not found!"
            )

            return

        if accounts[account_no]["pin"] != pin:

            messagebox.showerror(
                "Error",
                "Wrong PIN!"
            )

            return

        show_user_dashboard(account_no)


    create_button(
        frame,
        "LOGIN",
        login,
        "#0891B2"
    )

    create_button(
        frame,
        "BACK",
        show_home,
        "#64748B"
    )


# ==========================================
# USER DASHBOARD
# ==========================================

def show_user_dashboard(account_no):

    clear_window()

    root.configure(bg="#EAF4FF")

    title_label(root, "🏦 USER BANKING DASHBOARD")

    tk.Label(
        root,
        text=f"Welcome, {accounts[account_no]['name']}",
        font=("Arial", 17, "bold"),
        bg="#EAF4FF",
        fg="#0B3D91"
    ).pack(pady=12)

    balance = accounts[account_no]["balance"]

    tk.Label(
        root,
        text=f"💰 Current Balance: Rs. {balance:.2f}",
        font=("Arial", 15, "bold"),
        bg="#DCFCE7",
        fg="#166534",
        padx=25,
        pady=10
    ).pack(pady=8)

    frame = tk.Frame(root, bg="#EAF4FF")

    frame.pack(pady=10)

    buttons = [

        ("👤 MY PROFILE",
         lambda: show_profile(account_no),
         "#7C3AED"),

        ("📊 ACCOUNT STATISTICS",
         lambda: account_statistics(account_no),
         "#4F46E5"),

        ("💰 DEPOSIT MONEY",
         lambda: deposit_money(account_no),
         "#16A34A"),

        ("💸 WITHDRAW MONEY",
         lambda: withdraw_money(account_no),
         "#DC2626"),

        ("🔄 TRANSFER MONEY",
         lambda: transfer_money(account_no),
         "#DB2777"),

        ("💳 CHECK BALANCE",
         lambda: check_balance(account_no),
         "#0891B2"),

        ("📜 TRANSACTION HISTORY",
         lambda: transaction_history(account_no),
         "#D97706"),

        ("🪟 RECENT 5 TRANSACTIONS",
         lambda: recent_transactions(account_no),
         "#4F46E5"),

        ("🔐 CHANGE PIN",
         lambda: change_pin(account_no),
         "#0284C7"),

        ("🗑️ CLEAR TRANSACTION HISTORY",
         lambda: clear_transaction_history(account_no),
         "#64748B")

    ]

    row = 0
    column = 0

    for text, command, color in buttons:

        tk.Button(
            frame,
            text=text,
            command=command,
            bg=color,
            fg="white",
            font=("Arial", 11, "bold"),
            width=32,
            height=2,
            cursor="hand2"
        ).grid(
            row=row,
            column=column,
            padx=10,
            pady=8
        )

        column += 1

        if column == 2:
            column = 0
            row += 1

    tk.Button(
        root,
        text="🚪 LOGOUT",
        command=show_home,
        bg="#1E293B",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=35,
        pady=10
    ).pack(pady=12)


# ==========================================
# MY PROFILE
# ==========================================

def show_profile(account_no):

    account = accounts[account_no]

    transaction_count = len(
        account.get("transactions", [])
    )

    messagebox.showinfo(

        "MY PROFILE",

        f"👤 Name: {account['name']}\n\n"
        f"🔢 Account Number: {account_no}\n\n"
        f"💰 Current Balance: Rs. {account['balance']:.2f}\n\n"
        f"📜 Total Transactions: {transaction_count}\n\n"
        f"🟢 Account Status: Active"

    )


# ==========================================
# ACCOUNT STATISTICS
# ==========================================

def account_statistics(account_no):

    transactions = accounts[account_no].get(
        "transactions",
        []
    )

    deposited = 0
    withdrawn = 0

    for transaction in transactions:

        try:

            if "Deposited Rs." in transaction:

                amount = transaction.split(
                    "Deposited Rs. "
                )[1]

                deposited += float(amount)

            elif "Withdraw Rs." in transaction:

                amount = transaction.split(
                    "Withdraw Rs. "
                )[1]

                withdrawn += float(amount)

        except:
            pass

    messagebox.showinfo(

        "ACCOUNT STATISTICS",

        f"📊 Total Transactions: {len(transactions)}\n\n"
        f"💰 Total Deposited: Rs. {deposited:.2f}\n\n"
        f"💸 Total Withdrawn: Rs. {withdrawn:.2f}\n\n"
        f"💳 Current Balance: Rs. "
        f"{accounts[account_no]['balance']:.2f}"

    )


# ==========================================
# DEPOSIT MONEY
# ==========================================

def deposit_money(account_no):

    window = tk.Toplevel(root)

    window.title("Deposit Money")

    window.geometry("400x300")

    tk.Label(
        window,
        text="💰 DEPOSIT MONEY",
        font=("Arial", 18, "bold")
    ).pack(pady=30)

    tk.Label(
        window,
        text="Enter Amount",
        font=("Arial", 12)
    ).pack()

    amount_entry = tk.Entry(
        window,
        font=("Arial", 13)
    )

    amount_entry.pack(pady=10)


    def deposit():

        try:

            amount = float(
                amount_entry.get()
            )

            if amount <= 0:
                raise ValueError

        except:

            messagebox.showerror(
                "Error",
                "Enter valid amount!"
            )

            return

        accounts[account_no]["balance"] += amount

        add_transaction(
            account_no,
            f"Deposited Rs. {amount}"
        )

        save_data()

        messagebox.showinfo(
            "Success",
            "Money Deposited Successfully!"
        )

        window.destroy()

        show_user_dashboard(account_no)


    tk.Button(
        window,
        text="DEPOSIT",
        command=deposit,
        bg="#16A34A",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=30,
        pady=10
    ).pack(pady=20)


# ==========================================
# WITHDRAW MONEY
# ==========================================

def withdraw_money(account_no):

    window = tk.Toplevel(root)

    window.title("Withdraw Money")

    window.geometry("400x300")

    tk.Label(
        window,
        text="💸 WITHDRAW MONEY",
        font=("Arial", 18, "bold")
    ).pack(pady=30)

    tk.Label(
        window,
        text="Enter Amount",
        font=("Arial", 12)
    ).pack()

    amount_entry = tk.Entry(
        window,
        font=("Arial", 13)
    )

    amount_entry.pack(pady=10)


    def withdraw():

        try:

            amount = float(
                amount_entry.get()
            )

            if amount <= 0:
                raise ValueError

        except:

            messagebox.showerror(
                "Error",
                "Enter valid amount!"
            )

            return

        if amount > accounts[account_no]["balance"]:

            messagebox.showerror(
                "Error",
                "Insufficient Balance!"
            )

            return

        accounts[account_no]["balance"] -= amount

        add_transaction(
            account_no,
            f"Withdraw Rs. {amount}"
        )

        save_data()

        messagebox.showinfo(
            "Success",
            "Money Withdrawn Successfully!"
        )

        window.destroy()

        show_user_dashboard(account_no)


    tk.Button(
        window,
        text="WITHDRAW",
        command=withdraw,
        bg="#DC2626",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=30,
        pady=10
    ).pack(pady=20)


# ==========================================
# TRANSFER MONEY
# ==========================================

def transfer_money(sender):

    window = tk.Toplevel(root)

    window.title("Transfer Money")

    window.geometry("450x400")

    tk.Label(
        window,
        text="🔄 TRANSFER MONEY",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text="Receiver Account Number"
    ).pack()

    receiver_entry = tk.Entry(
        window,
        font=("Arial", 13)
    )

    receiver_entry.pack(pady=10)

    tk.Label(
        window,
        text="Amount"
    ).pack()

    amount_entry = tk.Entry(
        window,
        font=("Arial", 13)
    )

    amount_entry.pack(pady=10)


    def transfer():

        receiver = receiver_entry.get().strip()

        if receiver not in accounts:

            messagebox.showerror(
                "Error",
                "Receiver Account not found!"
            )

            return

        if receiver == sender:

            messagebox.showerror(
                "Error",
                "Cannot transfer to same account!"
            )

            return

        try:

            amount = float(
                amount_entry.get()
            )

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

        add_transaction(
            sender,
            f"Transferred Rs. {amount} to {receiver}"
        )

        add_transaction(
            receiver,
            f"Received Rs. {amount} from {sender}"
        )

        save_data()

        messagebox.showinfo(
            "Success",
            "Money Transferred Successfully!"
        )

        window.destroy()

        show_user_dashboard(sender)


    tk.Button(
        window,
        text="TRANSFER",
        command=transfer,
        bg="#DB2777",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=30,
        pady=10
    ).pack(pady=20)


# ==========================================
# CHECK BALANCE
# ==========================================

def check_balance(account_no):

    balance = accounts[account_no]["balance"]

    messagebox.showinfo(

        "CURRENT BALANCE",

        f"Account Number: {account_no}\n\n"
        f"Current Balance: Rs. {balance:.2f}"

    )


# ==========================================
# TRANSACTION HISTORY - LINKED LIST
# ==========================================

def transaction_history(account_no):

    linked_list = TransactionLinkedList()

    transactions = accounts[account_no].get(
        "transactions",
        []
    )

    for transaction in transactions:

        linked_list.append(transaction)

    history = linked_list.get_all()

    window = tk.Toplevel(root)

    window.title("Transaction History")

    window.geometry("700x500")

    tk.Label(
        window,
        text="📜 TRANSACTION HISTORY (LINKED LIST)",
        font=("Arial", 16, "bold"),
        bg="#D97706",
        fg="white",
        pady=15
    ).pack(fill="x")

    text = tk.Text(
        window,
        font=("Arial", 11)
    )

    text.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    if history:

        for transaction in history:

            text.insert(
                "end",
                transaction + "\n\n"
            )

    else:

        text.insert(
            "end",
            "No Transaction Found!"
        )

    text.config(state="disabled")


# ==========================================
# RECENT TRANSACTIONS - SLIDING WINDOW
# ==========================================

def recent_transactions(account_no):

    transactions = accounts[account_no].get(
        "transactions",
        []
    )

    recent = transactions[-5:]

    window = tk.Toplevel(root)

    window.title("Recent Transactions")

    window.geometry("650x450")

    tk.Label(
        window,
        text="🪟 RECENT 5 TRANSACTIONS (SLIDING WINDOW)",
        font=("Arial", 15, "bold"),
        bg="#4F46E5",
        fg="white",
        pady=15
    ).pack(fill="x")

    text = tk.Text(
        window,
        font=("Arial", 11)
    )

    text.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    if recent:

        for transaction in recent:

            text.insert(
                "end",
                transaction + "\n\n"
            )

    else:

        text.insert(
            "end",
            "No Recent Transactions!"
        )

    text.config(state="disabled")


# ==========================================
# CHANGE PIN - BETTER SECURITY
# ==========================================

def change_pin(account_no):

    window = tk.Toplevel(root)

    window.title("Change PIN")

    window.geometry("400x450")

    tk.Label(
        window,
        text="🔐 CHANGE PIN",
        font=("Arial", 18, "bold")
    ).pack(pady=25)

    tk.Label(
        window,
        text="Current PIN"
    ).pack()

    current_pin_entry = tk.Entry(
        window,
        show="*",
        font=("Arial", 13)
    )

    current_pin_entry.pack(pady=8)

    tk.Label(
        window,
        text="New 4 Digit PIN"
    ).pack()

    new_pin_entry = tk.Entry(
        window,
        show="*",
        font=("Arial", 13)
    )

    new_pin_entry.pack(pady=8)

    tk.Label(
        window,
        text="Confirm New PIN"
    ).pack()

    confirm_pin_entry = tk.Entry(
        window,
        show="*",
        font=("Arial", 13)
    )

    confirm_pin_entry.pack(pady=8)


    def change():

        current_pin = current_pin_entry.get().strip()
        new_pin = new_pin_entry.get().strip()
        confirm_pin = confirm_pin_entry.get().strip()

        if current_pin != accounts[account_no]["pin"]:

            messagebox.showerror(
                "Error",
                "Current PIN is incorrect!"
            )

            return

        if not new_pin.isdigit() or len(new_pin) != 4:

            messagebox.showerror(
                "Error",
                "New PIN must be exactly 4 digits!"
            )

            return

        if new_pin != confirm_pin:

            messagebox.showerror(
                "Error",
                "New PIN and Confirm PIN do not match!"
            )

            return

        accounts[account_no]["pin"] = new_pin

        add_transaction(
            account_no,
            "PIN Changed Successfully"
        )

        save_data()

        messagebox.showinfo(
            "Success",
            "PIN Changed Successfully!"
        )

        window.destroy()


    tk.Button(
        window,
        text="CHANGE PIN",
        command=change,
        bg="#0284C7",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=30,
        pady=10
    ).pack(pady=20)


# ==========================================
# CLEAR TRANSACTION HISTORY
# ==========================================

def clear_transaction_history(account_no):

    confirm = messagebox.askyesno(
        "Confirm",
        "Clear all transaction history?"
    )

    if confirm:

        accounts[account_no]["transactions"] = []

        save_data()

        messagebox.showinfo(
            "Success",
            "Transaction History Cleared!"
        )


# ==========================================
# ADMIN LOGIN
# ==========================================

def admin_login():

    clear_window()

    root.configure(bg="#EAF4FF")

    title_label(root, "👨‍💼 ADMIN LOGIN")

    frame = tk.Frame(root, bg="#EAF4FF")

    frame.pack(pady=60)

    tk.Label(
        frame,
        text="Username",
        font=("Arial", 12, "bold"),
        bg="#EAF4FF"
    ).pack()

    username_entry = tk.Entry(
        frame,
        font=("Arial", 13),
        width=30
    )

    username_entry.pack(pady=10, ipady=7)

    tk.Label(
        frame,
        text="Password",
        font=("Arial", 12, "bold"),
        bg="#EAF4FF"
    ).pack()

    password_entry = tk.Entry(
        frame,
        show="*",
        font=("Arial", 13),
        width=30
    )

    password_entry.pack(pady=10, ipady=7)


    def login():

        if (
            username_entry.get() == "admin"
            and password_entry.get() == "admin123"
        ):

            admin_dashboard()

        else:

            messagebox.showerror(
                "Error",
                "Invalid Admin Login!"
            )


    create_button(
        frame,
        "ADMIN LOGIN",
        login,
        "#1E293B"
    )

    create_button(
        frame,
        "BACK",
        show_home,
        "#64748B"
    )


# ==========================================
# ADMIN DASHBOARD
# ==========================================

def admin_dashboard():

    clear_window()

    root.configure(bg="#EAF4FF")

    title_label(root, "📊 ADMIN DASHBOARD")

    total_accounts = len(accounts)

    total_balance = sum(
        account["balance"]
        for account in accounts.values()
    )

    cards = tk.Frame(
        root,
        bg="#EAF4FF"
    )

    cards.pack(pady=25)

    tk.Label(
        cards,
        text=f"👥 TOTAL ACCOUNTS\n\n{total_accounts}",
        font=("Arial", 16, "bold"),
        bg="#DBEAFE",
        fg="#1E3A8A",
        width=25,
        height=5
    ).grid(
        row=0,
        column=0,
        padx=20
    )

    tk.Label(
        cards,
        text=f"💰 TOTAL BANK BALANCE\n\nRs. {total_balance:.2f}",
        font=("Arial", 16, "bold"),
        bg="#DCFCE7",
        fg="#166534",
        width=25,
        height=5
    ).grid(
        row=0,
        column=1,
        padx=20
    )

    frame = tk.Frame(root, bg="#EAF4FF")

    frame.pack(pady=10)

    buttons = [

        ("🔍 SEARCH ACCOUNT",
         search_account,
         "#2563EB"),

        ("❌ DELETE ACCOUNT",
         delete_account,
         "#DC2626"),

        ("🌳 SHOW SORTED ACCOUNTS (BST)",
         sorted_accounts,
         "#059669"),

        ("💾 CREATE DATA BACKUP",
         create_backup,
         "#7C3AED"),

        ("🔄 REFRESH DASHBOARD",
         admin_dashboard,
         "#0891B2"),

        ("🚪 LOGOUT",
         show_home,
         "#1E293B")

    ]

    for text, command, color in buttons:

        create_button(
            frame,
            text,
            command,
            color
        )


# ==========================================
# CREATE DATA BACKUP
# ==========================================

def create_backup():

    try:

        save_data()

        shutil.copy(
            DATA_FILE,
            BACKUP_FILE
        )

        messagebox.showinfo(

            "Backup Success",

            f"Backup Created Successfully!\n\n"
            f"File: {BACKUP_FILE}"

        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Backup Failed!\n{e}"
        )


# ==========================================
# SEARCH ACCOUNT - HASHING
# ==========================================

def search_account():

    window = tk.Toplevel(root)

    window.title("Search Account")

    window.geometry("450x300")

    tk.Label(
        window,
        text="🔍 SEARCH ACCOUNT (HASHING)",
        font=("Arial", 16, "bold")
    ).pack(pady=30)

    entry = tk.Entry(
        window,
        font=("Arial", 13)
    )

    entry.pack(pady=10)


    def search():

        account_no = entry.get().strip()

        if account_no in accounts:

            account = accounts[account_no]

            transaction_count = len(
                account.get(
                    "transactions",
                    []
                )
            )

            messagebox.showinfo(

                "Account Found",

                f"Account Number: {account_no}\n\n"
                f"Name: {account['name']}\n\n"
                f"Balance: Rs. {account['balance']:.2f}\n\n"
                f"Total Transactions: {transaction_count}\n\n"
                f"Status: Active"

            )

        else:

            messagebox.showerror(
                "Error",
                "Account Not Found!"
            )


    tk.Button(
        window,
        text="SEARCH",
        command=search,
        bg="#2563EB",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=30,
        pady=10
    ).pack(pady=20)


# ==========================================
# DELETE ACCOUNT
# ==========================================

def delete_account():

    window = tk.Toplevel(root)

    window.title("Delete Account")

    window.geometry("400x300")

    tk.Label(
        window,
        text="❌ DELETE ACCOUNT",
        font=("Arial", 18, "bold")
    ).pack(pady=30)

    tk.Label(
        window,
        text="Enter Account Number"
    ).pack()

    entry = tk.Entry(
        window,
        font=("Arial", 13)
    )

    entry.pack(pady=10)


    def delete():

        account_no = entry.get().strip()

        if account_no not in accounts:

            messagebox.showerror(
                "Error",
                "Account Not Found!"
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete account {account_no}?"
        )

        if confirm:

            del accounts[account_no]

            rebuild_bst()

            save_data()

            messagebox.showinfo(
                "Success",
                "Account Deleted Successfully!"
            )

            window.destroy()

            admin_dashboard()


    tk.Button(
        window,
        text="DELETE ACCOUNT",
        command=delete,
        bg="#DC2626",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=30,
        pady=10
    ).pack(pady=20)


# ==========================================
# SORTED ACCOUNTS - BST
# ==========================================

def sorted_accounts():

    account_list = account_bst.inorder()

    window = tk.Toplevel(root)

    window.title("Sorted Accounts")

    window.geometry("700x500")

    tk.Label(
        window,
        text="🌳 SORTED ACCOUNTS (BST)",
        font=("Arial", 16, "bold"),
        bg="#059669",
        fg="white",
        pady=15
    ).pack(fill="x")

    text = tk.Text(
        window,
        font=("Arial", 11)
    )

    text.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    if account_list:

        for account_no in account_list:

            account = accounts[account_no]

            text.insert(

                "end",

                f"Account Number: {account_no}\n"
                f"Name: {account['name']}\n"
                f"Balance: Rs. {account['balance']:.2f}\n"
                + "-" * 45
                + "\n\n"

            )

    else:

        text.insert(
            "end",
            "No Accounts Found!"
        )

    text.config(state="disabled")


# ==========================================
# START APPLICATION
# ==========================================

load_data()

root = tk.Tk()

root.title("Bank Management System - Dynamic")

root.geometry("1000x750")

root.minsize(900, 650)

show_home()

root.mainloop()