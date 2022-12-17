import tkinter as tk
import tkinter.messagebox as messagebox
from datetime import datetime
from hashlib import sha256

from backend import Backend
from database import Database
from entities.categories import CATEGORIES
from entities.months import MONTHS
from entities.record_type import RecordType


class LoginPage(tk.Frame):
    EXPECTED_PWD = (
        "56b1db8133d9eb398aabd376f07bf8ab5fc584ea0b8bd6a1770200cb613ca005"
    )

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self._controller = controller

        label_name = tk.Label(self, text="Username")
        label_name.grid(row=0, column=0, padx=10, pady=10)
        self._entry_name = tk.Entry(self)
        self._entry_name.grid(row=0, column=1, padx=10, pady=10)
        label_pwd = tk.Label(self, text="Password")
        label_pwd.grid(row=1, column=0, padx=10, pady=10)
        self._entry_password = tk.Entry(self)
        self._entry_password.grid(row=1, column=1, padx=10, pady=10)
        button1 = tk.Button(
            self, text="Sign in", width=25, command=self.__verify_login
        )
        button1.grid(row=2, column=1, padx=10, pady=10)

    def __verify_login(self):
        hashed_pwd = sha256(
            f"{self._entry_password.get()}".encode("ascii")
        ).hexdigest()
        if hashed_pwd == self.EXPECTED_PWD:
            self._controller.show_frame(MainPage)
        else:
            messagebox.showerror("Error", "Username or password in invalid")


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self._db = Database()
        self._backend = Backend()

        # ----LABELS------
        row_col1 = 0
        tk.Label(self, text="Welcome to my App").grid(column=0, row=row_col1)

        row_col1 += 1
        tk.Label(self, text="Expenses this month:").grid(
            column=0, row=row_col1
        )

        # Monthly sums
        expenses_sums = self._expenses_sums()

        for i in range(len(CATEGORIES)):
            category_name = CATEGORIES[i]
            category_sum = expenses_sums[i]

            len_name = len(category_name)
            len_sum = len(str(category_sum))
            spacers = " " * (30 - (len_name + len_sum))

            row_col1 += 1
            label_category = tk.Label(
                self, text=f"{category_name}:{spacers}{category_sum} Kč"
            )
            label_category.grid(column=0, row=row_col1)

        # Blank line and sums for expenses and incomes
        row_col1 += 1
        tk.Label(self, text=" ").grid(column=0, row=row_col1)

        expenses_total = sum(expenses_sums)

        row_col1 += 1
        tk.Label(
            self, text=f"Expenses total:        {expenses_total} Kč"
        ).grid(column=0, row=row_col1)

        incomes_total = self._incomes_sum()
        row_col1 += 1
        tk.Label(self, text=f"Incomes total:        {incomes_total} Kč").grid(
            column=0, row=row_col1
        )

        # SHOW GRAPH
        years = self._db.get_list_of_years()
        self._entry_year_graph = tk.StringVar(self)
        tk.OptionMenu(self, self._entry_year_graph, *years).grid(
            column=3, row=3
        )
        tk.Button(
            self, text="Show graph for year: ", command=self._plot_graphs
        ).grid(column=1, row=3)

        # NEW RECORD FORM
        row_col4 = 0
        tk.Label(self, text="### New record form ###").grid(
            column=4, row=row_col4, columnspan=2
        )

        row_col4 += 1
        tk.Label(self, text="Type of record: (*)").grid(column=4, row=row_col4)

        row_col4 += 1
        tk.Label(self, text="Category: (*)").grid(column=4, row=row_col4)

        row_col4 += 1
        tk.Label(self, text="Year: (*)").grid(column=4, row=row_col4)

        row_col4 += 1
        tk.Label(self, text="Month (number): (*)").grid(column=4, row=row_col4)

        row_col4 += 1
        tk.Label(self, text="Day: ").grid(column=4, row=row_col4)

        row_col4 += 1
        tk.Label(self, text="Amount: (*)").grid(column=4, row=row_col4)

        row_col4 += 1
        tk.Label(self, text="Note: ").grid(column=4, row=row_col4)

        # -----ENTRIES------
        row_col5 = 1
        self._entry_record_type = tk.StringVar(self)
        self._entry_record_type.set("Expense")
        tk.OptionMenu(self, self._entry_record_type, "Expense", "Income").grid(
            column=5, row=row_col5
        )

        row_col5 += 1
        self._entry_category = tk.StringVar(self)
        tk.OptionMenu(self, self._entry_category, *CATEGORIES).grid(
            column=5, row=row_col5
        )

        row_col5 += 1
        self._entry_year = tk.Entry(self)
        self._entry_year.insert(tk.END, str(datetime.now().year))
        self._entry_year.grid(column=5, row=row_col5)

        row_col5 += 1
        self._entry_month = tk.StringVar(self)
        currentMonth = MONTHS[datetime.now().month - 1]
        self._entry_month.set(currentMonth)
        tk.OptionMenu(self, self._entry_month, *MONTHS).grid(
            column=5, row=row_col5
        )

        row_col5 += 1
        self._entry_date = tk.Entry(self)
        self._entry_date.insert(tk.END, str(datetime.now().day))
        self._entry_date.grid(column=5, row=row_col5)

        row_col5 += 1
        self._entry_amount = tk.Entry(self)
        self._entry_amount.grid(column=5, row=row_col5)

        row_col5 += 1
        self._entry_note = tk.Entry(self)
        self._entry_note.grid(column=5, row=row_col5)

        row_col5 += 1
        tk.Button(
            self, text="Add a new record", command=self._add_record
        ).grid(column=5, row=row_col5)

    def _plot_graphs(self):
        year = str(self._entry_year_graph.get())

        if year != "":
            self._backend._graph_data(int(year))

    def _expenses_sums(self):
        current_month = datetime.now().month - 1

        all_categories = []
        source_list = self._db.get_sums_expenses(datetime.now().year)
        for category in range(len(CATEGORIES)):
            single_category = source_list[category]
            single_category_single_month = single_category[current_month]
            all_categories.append(single_category_single_month)

        return all_categories

    def _incomes_sum(self):
        current_month = datetime.now().month - 1
        all_months = self._db.get_sums_incomes(datetime.now().year)
        current_month_sum = all_months[current_month]

        return current_month_sum

    def _add_record(self):
        try:
            self._validate_inputs()

            record_type = (
                RecordType.EXPENSE
                if self._entry_record_type.get() == "Expense"
                else RecordType.INCOME
            )
            category = (
                CATEGORIES.index(self._entry_category.get()) + 1
                if record_type == RecordType.EXPENSE
                else 0
            )
            year = int(self._entry_year.get())
            month = (
                MONTHS.index(self._entry_month.get()) + 1
            )  # TODO: magic constant, use list
            date = int(self._entry_date.get())
            amount = int(self._entry_amount.get())
            note = self._entry_note.get()

            self._db.add_record(
                record_type, category, year, month, date, amount, note
            )

            messagebox.showinfo(
                "Add a new record", "New record has been successfully added."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _validate_inputs(self):
        if (
            self._entry_record_type.get() == "Expense"
            and self._entry_category.get() == ""
        ):
            raise Exception("Please, choose a category!")

        if self._entry_year.get() == "":
            raise Exception("Please, insert a year!")

        if self._entry_amount.get() == "":
            raise Exception("Please, insert an amount!")


class Gui(tk.Tk):
    # TODO: move all entries here??
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("My awesome budget app")
        img = tk.PhotoImage(file="wallet.png")
        self.tk.call("wm", "iconphoto", self._w, img)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Frame in (LoginPage, MainPage):
            frame = Frame(container, self)
            self.frames[Frame] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

        self.mainloop()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    gui = Gui()
