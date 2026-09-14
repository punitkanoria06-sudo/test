import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

# ==================================================
# BANK MANAGEMENT SYSTEM - DSA BASED MINI PROJECT
# ==================================================

DATA_FILE = "accounts.json"

# HASHING - Dictionary for fast account search
accounts = {}


# ==================================================
# LINKED LIST - TRANSACTION HISTORY
# ==================================================

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

    def to_list(self):

        result = []
        temp = self.head

        while temp is not None:
            result.append(temp.data)
            temp = temp.next

        return result


# ==================================================
# BINARY SEARCH TREE - SORTED ACCOUNTS
# ==================================================

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

        if str(account_no) < str(root.account_no):

            root.left = self._insert(
                root.left,
                account_no
            )

        elif str(account_no) > str(root.account_no):

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

    def _inorder(
        self,
        root,
        result
    ):

        if root is not None:

            self._inorder(
                root.left,
                result
            )

            result.append(
                root.account_no
            )

            self._inorder(
                root.right,
                result
            )


account_bst = AccountBST()


# ==================================================
# DATA FUNCTIONS
# ==================================================

def load_data():

    global accounts

    if os.path.exists(DATA_FILE):

        try:

            with open(
                DATA_FILE,
                "r"
            ) as file:

                accounts = json.load(file)

        except:

            accounts = {}

    else:

        accounts = {}

    rebuild_bst()


def save_data():

    with open(
        DATA_FILE,
        "w"
    ) as file:

        json.dump(
            accounts,
            file,
            indent=4
        )


def rebuild_bst():

    global account_bst

    account_bst = AccountBST()

    for account_no in accounts:

        account_bst.insert(
            account_no
        )


# ==================================================
# TRANSACTION FUNCTIONS
# ==================================================

def add_transaction(
    account_no,
    text
):

    if "transactions" not in accounts[account_no]:

        accounts[account_no][
            "transactions"
        ] = []

    date_time = datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )

    transaction = (
        date_time
        + " - "
        + text
    )

    accounts[account_no][
        "transactions"
    ].append(transaction)


# ==================================================
# LINKED LIST HISTORY
# ==================================================

def get_linked_history(account_no):

    linked_list = TransactionLinkedList()

    transactions = accounts[
        account_no
    ].get(
        "transactions",
        []
    )

    for transaction in transactions:

        linked_list.append(
            transaction
        )

    return linked_list


# ==================================================
# SLIDING WINDOW
# RECENT 5 TRANSACTIONS
# ==================================================

def get_recent_transactions(
    account_no,
    window_size=5
):

    transactions = accounts[
        account_no
    ].get(
        "transactions",
        []
    )

    start = max(
        0,
        len(transactions) - window_size
    )

    return transactions[start:]


# ==================================================
# GUI FUNCTIONS
# ==================================================

def clear_window():

    for widget in root.winfo_children():

        widget.destroy()


# ==================================================
# FORM WINDOW
# ==================================================

def create_form(
    title,
    fields,
    button_text,
    function,
    color
):

    window = tk.Toplevel(root)

    window.title(title)

    window.geometry(
        "500x550"
    )

    window.configure(
        bg="#EAF4FF"
    )

    tk.Label(

        window,

        text=title,

        font=("Arial", 20, "bold"),

        bg=color,

        fg="white",

        pady=15

    ).pack(
        fill="x"
    )


    frame = tk.Frame(

        window,

        bg="#EAF4FF"

    )

    frame.pack(

        fill="both",

        expand=True,

        padx=40,

        pady=20

    )


    entries = {}


    for label, key, password in fields:


        tk.Label(

            frame,

            text=label,

            font=("Arial", 11, "bold"),

            bg="#EAF4FF"

        ).pack(

            anchor="w",

            pady=(8, 3)

        )


        entry = tk.Entry(

            frame,

            font=("Arial", 12),

            show="*" if password else ""

        )


        entry.pack(

            fill="x",

            ipady=7

        )


        entries[key] = entry


    tk.Button(

        frame,

        text=button_text,

        command=lambda: function(
            entries,
            window
        ),

        bg=color,

        fg="white",

        font=("Arial", 12, "bold"),

        pady=10

    ).pack(

        fill="x",

        pady=20

    )


    tk.Button(

        frame,

        text="CANCEL",

        command=window.destroy,

        bg="#64748B",

        fg="white",

        font=("Arial", 11, "bold"),

        pady=8

    ).pack(
        fill="x"
    )


# ==================================================
# CREATE ACCOUNT
# ==================================================

def create_account():

    def submit(
        entries,
        window
    ):

        account_no = entries[
            "account"
        ].get().strip()

        name = entries[
            "name"
        ].get().strip()

        pin = entries[
            "pin"
        ].get().strip()

        balance = entries[
            "balance"
        ].get().strip()


        if (
            account_no == ""
            or name == ""
            or pin == ""
            or balance == ""
        ):

            messagebox.showerror(
                "Error",
                "Please fill all fields!"
            )

            return


        if account_no in accounts:

            messagebox.showerror(
                "Error",
                "Account already exists!"
            )

            return


        if (
            not pin.isdigit()
            or len(pin) != 4
        ):

            messagebox.showerror(
                "Error",
                "PIN must be 4 digits!"
            )

            return


        try:

            balance = float(balance)

            if balance < 0:
                raise ValueError

        except:

            messagebox.showerror(
                "Error",
                "Enter valid balance!"
            )

            return


        accounts[account_no] = {

            "name": name,

            "pin": pin,

            "balance": balance,

            "transactions": []

        }


        account_bst.insert(
            account_no
        )


        add_transaction(

            account_no,

            "Account Created with Rs. "
            + str(balance)

        )


        save_data()


        messagebox.showinfo(

            "Success",

            "Account Created Successfully!"

        )


        window.destroy()


        show_dashboard()


    create_form(

        "CREATE ACCOUNT",

        [

            (
                "Account Number",
                "account",
                False
            ),

            (
                "Account Holder Name",
                "name",
                False
            ),

            (
                "4 Digit PIN",
                "pin",
                True
            ),

            (
                "Initial Balance",
                "balance",
                False
            )

        ],

        "CREATE ACCOUNT",

        submit,

        "#2563EB"

    )


# ==================================================
# DEPOSIT MONEY
# ==================================================

def deposit_money():

    def submit(
        entries,
        window
    ):

        account_no = entries[
            "account"
        ].get().strip()

        pin = entries[
            "pin"
        ].get().strip()

        amount = entries[
            "amount"
        ].get().strip()


        if account_no not in accounts:

            messagebox.showerror(
                "Error",
                "Account not found!"
            )

            return


        if accounts[account_no][
            "pin"
        ] != pin:

            messagebox.showerror(
                "Error",
                "Wrong PIN!"
            )

            return


        try:

            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except:

            messagebox.showerror(
                "Error",
                "Enter valid amount!"
            )

            return


        accounts[account_no][
            "balance"
        ] += amount


        add_transaction(

            account_no,

            "Deposited Rs. "
            + str(amount)

        )


        save_data()


        messagebox.showinfo(
            "Success",
            "Money Deposited Successfully!"
        )


        window.destroy()

        show_dashboard()


    create_form(

        "DEPOSIT MONEY",

        [

            (
                "Account Number",
                "account",
                False
            ),

            (
                "PIN",
                "pin",
                True
            ),

            (
                "Deposit Amount",
                "amount",
                False
            )

        ],

        "DEPOSIT MONEY",

        submit,

        "#16A34A"

    )


# ==================================================
# WITHDRAW MONEY
# ==================================================

def withdraw_money():

    def submit(
        entries,
        window
    ):

        account_no = entries[
            "account"
        ].get().strip()

        pin = entries[
            "pin"
        ].get().strip()

        amount = entries[
            "amount"
        ].get().strip()


        if account_no not in accounts:

            messagebox.showerror(
                "Error",
                "Account not found!"
            )

            return


        if accounts[account_no][
            "pin"
        ] != pin:

            messagebox.showerror(
                "Error",
                "Wrong PIN!"
            )

            return


        try:

            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except:

            messagebox.showerror(
                "Error",
                "Enter valid amount!"
            )

            return


        if amount > accounts[
            account_no
        ][
            "balance"
        ]:

            messagebox.showerror(
                "Error",
                "Insufficient Balance!"
            )

            return


        accounts[account_no][
            "balance"
        ] -= amount


        add_transaction(

            account_no,

            "Withdraw Rs. "
            + str(amount)

        )


        save_data()


        messagebox.showinfo(
            "Success",
            "Money Withdrawn Successfully!"
        )


        window.destroy()

        show_dashboard()


    create_form(

        "WITHDRAW MONEY",

        [

            (
                "Account Number",
                "account",
                False
            ),

            (
                "PIN",
                "pin",
                True
            ),

            (
                "Withdrawal Amount",
                "amount",
                False
            )

        ],

        "WITHDRAW MONEY",

        submit,

        "#DC2626"

    )


# ==================================================
# CHECK BALANCE
# ==================================================

def check_balance():

    def submit(
        entries,
        window
    ):

        account_no = entries[
            "account"
        ].get().strip()

        pin = entries[
            "pin"
        ].get().strip()


        if account_no not in accounts:

            messagebox.showerror(
                "Error",
                "Account not found!"
            )

            return


        if accounts[account_no][
            "pin"
        ] != pin:

            messagebox.showerror(
                "Error",
                "Wrong PIN!"
            )

            return


        balance = accounts[
            account_no
        ][
            "balance"
        ]


        messagebox.showinfo(

            "ACCOUNT BALANCE",

            "Account Holder: "
            + accounts[
                account_no
            ][
                "name"
            ]
            + "\n\nCurrent Balance: Rs. "
            + str(balance)

        )


    create_form(

        "CHECK BALANCE",

        [

            (
                "Account Number",
                "account",
                False
            ),

            (
                "PIN",
                "pin",
                True
            )

        ],

        "CHECK BALANCE",

        submit,

        "#7C3AED"

    )


# ==================================================
# TRANSACTION HISTORY
# LINKED LIST
# ==================================================

def transaction_history():

    def submit(
        entries,
        window
    ):

        account_no = entries[
            "account"
        ].get().strip()

        pin = entries[
            "pin"
        ].get().strip()


        if account_no not in accounts:

            messagebox.showerror(
                "Error",
                "Account not found!"
            )

            return


        if accounts[account_no][
            "pin"
        ] != pin:

            messagebox.showerror(
                "Error",
                "Wrong PIN!"
            )

            return


        linked_history = (
            get_linked_history(
                account_no
            )
        )


        history = (
            linked_history.to_list()
        )


        history_window = tk.Toplevel(
            root
        )

        history_window.title(
            "Transaction History"
        )

        history_window.geometry(
            "700x500"
        )


        tk.Label(

            history_window,

            text="TRANSACTION HISTORY (LINKED LIST)",

            font=(
                "Arial",
                16,
                "bold"
            ),

            bg="#D97706",

            fg="white",

            pady=15

        ).pack(
            fill="x"
        )


        text = tk.Text(

            history_window,

            font=("Arial", 11),

            padx=15,

            pady=15

        )


        text.pack(

            fill="both",

            expand=True

        )


        if history:

            for transaction in history:

                text.insert(
                    "end",
                    transaction
                    + "\n\n"
                )

        else:

            text.insert(
                "end",
                "No Transaction Found!"
            )


        text.config(
            state="disabled"
        )


    create_form(

        "TRANSACTION HISTORY",

        [

            (
                "Account Number",
                "account",
                False
            ),

            (
                "PIN",
                "pin",
                True
            )

        ],

        "VIEW HISTORY",

        submit,

        "#D97706"

    )


# ==================================================
# RECENT TRANSACTIONS
# SLIDING WINDOW
# ==================================================

def recent_transactions():

    def submit(
        entries,
        window
    ):

        account_no = entries[
            "account"
        ].get().strip()

        pin = entries[
            "pin"
        ].get().strip()


        if account_no not in accounts:

            messagebox.showerror(
                "Error",
                "Account not found!"
            )

            return


        if accounts[account_no][
            "pin"
        ] != pin:

            messagebox.showerror(
                "Error",
                "Wrong PIN!"
            )

            return


        recent = (
            get_recent_transactions(
                account_no
            )
        )


        recent_window = tk.Toplevel(
            root
        )

        recent_window.title(
            "Recent Transactions"
        )

        recent_window.geometry(
            "700x450"
        )


        tk.Label(

            recent_window,

            text="RECENT 5 TRANSACTIONS (SLIDING WINDOW)",

            font=(
                "Arial",
                15,
                "bold"
            ),

            bg="#4F46E5",

            fg="white",

            pady=15

        ).pack(
            fill="x"
        )


        text = tk.Text(

            recent_window,

            font=("Arial", 11),

            padx=15,

            pady=15

        )


        text.pack(

            fill="both",

            expand=True

        )


        if recent:

            for transaction in recent:

                text.insert(
                    "end",
                    transaction
                    + "\n\n"
                )

        else:

            text.insert(
                "end",
                "No Recent Transaction!"
            )


        text.config(
            state="disabled"
        )


    create_form(

        "RECENT TRANSACTIONS",

        [

            (
                "Account Number",
                "account",
                False
            ),

            (
                "PIN",
                "pin",
                True
            )

        ],

        "SHOW RECENT 5",

        submit,

        "#4F46E5"

    )


# ==================================================
# TRANSFER MONEY
# ==================================================

def transfer_money():

    def submit(
        entries,
        window
    ):

        sender = entries[
            "sender"
        ].get().strip()

        pin = entries[
            "pin"
        ].get().strip()

        receiver = entries[
            "receiver"
        ].get().strip()

        amount = entries[
            "amount"
        ].get().strip()


        if sender not in accounts:

            messagebox.showerror(
                "Error",
                "Sender Account not found!"
            )

            return


        if receiver not in accounts:

            messagebox.showerror(
                "Error",
                "Receiver Account not found!"
            )

            return


        if sender == receiver:

            messagebox.showerror(
                "Error",
                "Cannot transfer to same account!"
            )

            return


        if accounts[sender][
            "pin"
        ] != pin:

            messagebox.showerror(
                "Error",
                "Wrong PIN!"
            )

            return


        try:

            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except:

            messagebox.showerror(
                "Error",
                "Enter valid amount!"
            )

            return


        if amount > accounts[
            sender
        ][
            "balance"
        ]:

            messagebox.showerror(
                "Error",
                "Insufficient Balance!"
            )

            return


        accounts[sender][
            "balance"
        ] -= amount


        accounts[receiver][
            "balance"
        ] += amount


        add_transaction(

            sender,

            "Transferred Rs. "
            + str(amount)
            + " to Account "
            + receiver

        )


        add_transaction(

            receiver,

            "Received Rs. "
            + str(amount)
            + " from Account "
            + sender

        )


        save_data()


        messagebox.showinfo(
            "Success",
            "Money Transferred Successfully!"
        )


        window.destroy()

        show_dashboard()


    create_form(

        "TRANSFER MONEY",

        [

            (
                "Sender Account Number",
                "sender",
                False
            ),

            (
                "PIN",
                "pin",
                True
            ),

            (
                "Receiver Account Number",
                "receiver",
                False
            ),

            (
                "Transfer Amount",
                "amount",
                False
            )

        ],

        "TRANSFER MONEY",

        submit,

        "#DB2777"

    )


# ==================================================
# USER LOGIN
# ==================================================

def user_login():

    def submit(
        entries,
        window
    ):

        account_no = entries[
            "account"
        ].get().strip()

        pin = entries[
            "pin"
        ].get().strip()


        if account_no not in accounts:

            messagebox.showerror(
                "Error",
                "Account not found!"
            )

            return


        if accounts[account_no][
            "pin"
        ] != pin:

            messagebox.showerror(
                "Error",
                "Wrong PIN!"
            )

            return


        messagebox.showinfo(

            "LOGIN SUCCESS",

            "Welcome "
            + accounts[
                account_no
            ][
                "name"
            ]
            + "!"

        )


        window.destroy()

        show_dashboard()


    create_form(

        "USER LOGIN",

        [

            (
                "Account Number",
                "account",
                False
            ),

            (
                "PIN",
                "pin",
                True
            )

        ],

        "LOGIN",

        submit,

        "#0891B2"

    )


# ==================================================
# SEARCH ACCOUNT - HASHING
# ==================================================

def search_account():

    window = tk.Toplevel(root)

    window.title(
        "Search Account"
    )

    window.geometry(
        "450x300"
    )

    window.configure(
        bg="#EAF4FF"
    )


    tk.Label(

        window,

        text="SEARCH ACCOUNT (HASHING)",

        font=("Arial", 16, "bold"),

        bg="#2563EB",

        fg="white",

        pady=15

    ).pack(
        fill="x"
    )


    tk.Label(

        window,

        text="Enter Account Number",

        font=("Arial", 12, "bold"),

        bg="#EAF4FF"

    ).pack(
        pady=20
    )


    entry = tk.Entry(

        window,

        font=("Arial", 13)

    )

    entry.pack(
        ipady=6
    )


    def search():

        account_no = entry.get().strip()


        # HASHING LOOKUP

        if account_no in accounts:

            account = accounts[
                account_no
            ]


            messagebox.showinfo(

                "Account Found",

                "Account Number: "
                + account_no
                + "\nName: "
                + account["name"]
                + "\nBalance: Rs. "
                + str(
                    account["balance"]
                )

            )

        else:

            messagebox.showerror(
                "Error",
                "Account not found!"
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

    ).pack(
        pady=25
    )


# ==================================================
# DELETE ACCOUNT
# ==================================================

def delete_account():

    def submit(
        entries,
        window
    ):

        account_no = entries[
            "account"
        ].get().strip()

        pin = entries[
            "pin"
        ].get().strip()


        if account_no not in accounts:

            messagebox.showerror(
                "Error",
                "Account not found!"
            )

            return


        if accounts[account_no][
            "pin"
        ] != pin:

            messagebox.showerror(
                "Error",
                "Wrong PIN!"
            )

            return


        confirm = messagebox.askyesno(

            "Confirm",

            "Are you sure you want to delete this account?"

        )


        if confirm:

            del accounts[
                account_no
            ]


            save_data()

            rebuild_bst()


            messagebox.showinfo(
                "Success",
                "Account Deleted Successfully!"
            )


            window.destroy()


    create_form(

        "DELETE ACCOUNT",

        [

            (
                "Account Number",
                "account",
                False
            ),

            (
                "PIN",
                "pin",
                True
            )

        ],

        "DELETE ACCOUNT",

        submit,

        "#DC2626"

    )


# ==================================================
# SORTED ACCOUNTS - BST
# ==================================================

def sorted_accounts():

    account_list = (
        account_bst.inorder()
    )


    window = tk.Toplevel(root)

    window.title(
        "Sorted Accounts"
    )

    window.geometry(
        "700x500"
    )


    tk.Label(

        window,

        text="SORTED ACCOUNTS (BST INORDER TRAVERSAL)",

        font=("Arial", 15, "bold"),

        bg="#059669",

        fg="white",

        pady=15

    ).pack(
        fill="x"
    )


    text = tk.Text(

        window,

        font=("Arial", 11),

        padx=15,

        pady=15

    )


    text.pack(

        fill="both",

        expand=True

    )


    if account_list:

        for account_no in account_list:

            account = accounts[
                account_no
            ]


            text.insert(

                "end",

                "Account Number: "
                + account_no
                + "\nName: "
                + account["name"]
                + "\nBalance: Rs. "
                + str(
                    account["balance"]
                )
                + "\n"
                + "-" * 45
                + "\n"

            )

    else:

        text.insert(
            "end",
            "No Accounts Found!"
        )


    text.config(
        state="disabled"
    )


# ==================================================
# ADMIN LOGIN
# ==================================================

def admin_login():

    window = tk.Toplevel(root)

    window.title(
        "Admin Login"
    )

    window.geometry(
        "450x380"
    )

    window.configure(
        bg="#F1F5F9"
    )


    tk.Label(

        window,

        text="ADMIN LOGIN",

        font=("Arial", 20, "bold"),

        bg="#1E293B",

        fg="white",

        pady=18

    ).pack(
        fill="x"
    )


    frame = tk.Frame(

        window,

        bg="#F1F5F9"

    )

    frame.pack(
        fill="both",
        expand=True,
        padx=50,
        pady=30
    )


    tk.Label(

        frame,

        text="Username",

        font=("Arial", 11, "bold"),

        bg="#F1F5F9"

    ).pack(
        anchor="w"
    )


    username = tk.Entry(

        frame,

        font=("Arial", 12)

    )

    username.pack(
        fill="x",
        ipady=7,
        pady=(5, 20)
    )


    tk.Label(

        frame,

        text="Password",

        font=("Arial", 11, "bold"),

        bg="#F1F5F9"

    ).pack(
        anchor="w"
    )


    password = tk.Entry(

        frame,

        font=("Arial", 12),

        show="*"

    )

    password.pack(
        fill="x",
        ipady=7,
        pady=(5, 25)
    )


    def login():

        if (

            username.get() == "admin"

            and

            password.get() == "admin123"

        ):

            window.destroy()

            admin_panel()

        else:

            messagebox.showerror(
                "Error",
                "Invalid Username or Password!"
            )


    tk.Button(

        frame,

        text="LOGIN",

        command=login,

        bg="#1E293B",

        fg="white",

        font=("Arial", 12, "bold"),

        pady=10

    ).pack(
        fill="x"
    )


# ==================================================
# ADMIN PANEL
# ==================================================

def admin_panel():

    window = tk.Toplevel(root)

    window.title(
        "Admin Panel"
    )

    window.geometry(
        "800x600"
    )

    window.configure(
        bg="#EAF4FF"
    )


    tk.Label(

        window,

        text="ADMIN CONTROL PANEL",

        font=("Arial", 22, "bold"),

        bg="#1E293B",

        fg="white",

        pady=18

    ).pack(
        fill="x"
    )


    total_accounts = len(
        accounts
    )


    total_balance = sum(

        account["balance"]

        for account

        in accounts.values()

    )


    tk.Label(

        window,

        text="Total Accounts: "
        + str(total_accounts),

        font=("Arial", 16, "bold"),

        bg="#EAF4FF"

    ).pack(
        pady=15
    )


    tk.Label(

        window,

        text="Total Bank Balance: Rs. "
        + str(total_balance),

        font=("Arial", 16, "bold"),

        bg="#EAF4FF"

    ).pack(
        pady=10
    )


    tk.Button(

        window,

        text="SEARCH ACCOUNT",

        command=search_account,

        bg="#2563EB",

        fg="white",

        font=("Arial", 11, "bold"),

        width=35,

        pady=10

    ).pack(
        pady=8
    )


    tk.Button(

        window,

        text="DELETE ACCOUNT",

        command=delete_account,

        bg="#DC2626",

        fg="white",

        font=("Arial", 11, "bold"),

        width=35,

        pady=10

    ).pack(
        pady=8
    )


    tk.Button(

        window,

        text="SHOW SORTED ACCOUNTS (BST)",

        command=sorted_accounts,

        bg="#059669",

        fg="white",

        font=("Arial", 11, "bold"),

        width=35,

        pady=10

    ).pack(
        pady=8
    )


# ==================================================
# HOME PAGE
# ==================================================

def show_home():

    clear_window()


    root.configure(
        bg="#EAF4FF"
    )


    main_frame = tk.Frame(

        root,

        bg="white"

    )

    main_frame.place(

        relx=0.5,

        rely=0.5,

        anchor="center",

        width=550,

        height=520

    )


    tk.Label(

        main_frame,

        text="BANK MANAGEMENT SYSTEM",

        font=("Arial", 21, "bold"),

        bg="white",

        fg="#0B3D91"

    ).pack(
        pady=(55, 10)
    )


    tk.Label(

        main_frame,

        text="DSA Based Banking Mini Project",

        font=("Arial", 12),

        bg="white",

        fg="#64748B"

    ).pack()


    tk.Label(

        main_frame,

        text="Hashing | Linked List | BST | Sliding Window",

        font=("Arial", 10, "bold"),

        bg="white",

        fg="#4F46E5"

    ).pack(
        pady=25
    )


    tk.Button(

        main_frame,

        text="USER LOGIN",

        command=user_login,

        bg="#0891B2",

        fg="white",

        font=("Arial", 12, "bold"),

        width=35,

        pady=12

    ).pack(
        pady=7
    )


    tk.Button(

        main_frame,

        text="ADMIN LOGIN",

        command=admin_login,

        bg="#1E293B",

        fg="white",

        font=("Arial", 12, "bold"),

        width=35,

        pady=12

    ).pack(
        pady=7
    )


    tk.Button(

        main_frame,

        text="OPEN BANKING DASHBOARD",

        command=show_dashboard,

        bg="#2563EB",

        fg="white",

        font=("Arial", 12, "bold"),

        width=35,

        pady=12

    ).pack(
        pady=7
    )


    tk.Button(

        main_frame,

        text="EXIT",

        command=root.destroy,

        bg="#DC2626",

        fg="white",

        font=("Arial", 11, "bold"),

        width=35,

        pady=9

    ).pack(
        pady=7
    )


# ==================================================
# BANKING DASHBOARD
# ==================================================

def show_dashboard():

    clear_window()


    root.configure(
        bg="#EAF4FF"
    )


    header = tk.Frame(

        root,

        bg="#0B3D91",

        height=100

    )

    header.pack(
        fill="x"
    )


    tk.Label(

        header,

        text="BANK MANAGEMENT DASHBOARD",

        font=("Arial", 24, "bold"),

        bg="#0B3D91",

        fg="white"

    ).pack(
        pady=20
    )


    frame = tk.Frame(

        root,

        bg="#EAF4FF"

    )


    frame.pack(

        fill="both",

        expand=True,

        padx=80,

        pady=30

    )


    buttons = [

        (
            "CREATE ACCOUNT",
            create_account,
            "#2563EB"
        ),

        (
            "DEPOSIT MONEY",
            deposit_money,
            "#16A34A"
        ),

        (
            "WITHDRAW MONEY",
            withdraw_money,
            "#DC2626"
        ),

        (
            "CHECK BALANCE",
            check_balance,
            "#7C3AED"
        ),

        (
            "TRANSACTION HISTORY",
            transaction_history,
            "#D97706"
        ),

        (
            "RECENT 5 TRANSACTIONS",
            recent_transactions,
            "#4F46E5"
        ),

        (
            "TRANSFER MONEY",
            transfer_money,
            "#DB2777"
        )

    ]


    row = 0
    column = 0


    for text, command, color in buttons:


        button = tk.Button(

            frame,

            text=text,

            command=command,

            bg=color,

            fg="white",

            font=("Arial", 12, "bold"),

            width=32,

            height=2

        )


        button.grid(

            row=row,

            column=column,

            padx=10,

            pady=10

        )


        column += 1


        if column == 2:

            column = 0

            row += 1


    bottom = tk.Frame(

        root,

        bg="#EAF4FF"

    )

    bottom.pack(
        pady=10
    )


    tk.Button(

        bottom,

        text="HOME",

        command=show_home,

        bg="#64748B",

        fg="white",

        font=("Arial", 11, "bold"),

        padx=30,

        pady=10

    ).pack(
        side="left",
        padx=10
    )


    tk.Button(

        bottom,

        text="EXIT",

        command=root.destroy,

        bg="#DC2626",

        fg="white",

        font=("Arial", 11, "bold"),

        padx=30,

        pady=10

    ).pack(
        side="left",
        padx=10
    )


    tk.Label(

        root,

        text="Python | Tkinter | JSON | Hashing | Linked List | BST | Sliding Window",

        bg="#0B3D91",

        fg="white",

        font=("Arial", 10, "bold"),

        pady=8

    ).pack(
        fill="x",
        side="bottom"
    )


# ==================================================
# START PROGRAM
# ==================================================

load_data()


root = tk.Tk()


root.title(
    "Bank Management System"
)


root.geometry(
    "1000x750"
)


root.minsize(
    900,
    650
)


show_home()


root.mainloop()