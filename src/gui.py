import tkinter as tk
import tkinter.messagebox as messagebox
from datetime import datetime

from backend import Backend
from database import Database
from entities.categories import CATEGORIES
from entities.months import MONTHS


class Gui:
    # TODO: move all entries here??
    def __init__(self):
        self._db = Database()
        self._backend = Backend()
        self._window = tk.Tk()
        self._window.title("My awesome budget app")

        # magic for icon
        img = tk.PhotoImage(file="wallet.png")
        self._window.tk.call("wm", "iconphoto", self._window._w, img)

        self._render()

    def _add_record(self):
        error = 0  # Todo: rework to Exception
        expinc = 0
        # Get type of record entry (Expense/Income)
        if self._entry_expinc.get() == "Expense":
            expinc = 0

        elif self._entry_expinc.get() == "Income":
            expinc = 1

        else:
            pass

        # Handle empty category entry for expense and income record
        if self._entry_category.get() == "" and expinc == 0:
            messagebox.showerror("Error", "Please, choose a category!")
            error += 1

        elif expinc == 1:
            category = 0
            error += 0

        else:
            category = CATEGORIES.index(self._entry_category.get()) + 1
            error += 0

        # Handle empty year entry
        if self._entry_year.get() == "":
            messagebox.showerror("Error", "Please, insert a year!")
            error += 1

        else:
            year = self._entry_year.get()
            error += 0

        # Get month entry
        month = (
            MONTHS.index(self._entry_month.get()) + 1
        )  # TODO: magic constant, use list
        # Get date entry
        date = self._entry_date.get()

        # Handle empty amount entry
        if self._entry_amount.get() == "":
            messagebox.showerror("Error", "Please, insert an amount!")
            error += 1

        else:
            amount = self._entry_amount.get()
            error += 0

        # Get note entry
        note = self._entry_note.get()

        # Add a new record when all required entries filled
        if error == 0:
            # backend.addRecord(expinc, category, year, month, date, amount, note)  # noqa: E501
            print(
                f"expinc: {expinc}  category: {category}  year: {year}  month: {month}  date: {date}  amount: {amount} note: {note}"  # noqa: E501
            )

            messagebox.showinfo(
                "Add a new record", "New record has been successfully added."
            )
        else:
            pass

    def _render(self):
        # ----LABELS------
        row_col1 = 0
        tk.Label(text="Welcome to my App").grid(column=0, row=row_col1)

        row_col1 += 1
        tk.Label(text="Expenses this month:").grid(column=0, row=row_col1)

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
                text=f"{category_name}:{spacers}{category_sum} Kč"
            )
            label_category.grid(column=0, row=row_col1)

        # Blank line and sums for expenses and incomes
        row_col1 += 1
        tk.Label(text=" ").grid(column=0, row=row_col1)

        expenses_total = sum(expenses_sums)

        row_col1 += 1
        tk.Label(text=f"Expenses total:        {expenses_total} Kč").grid(
            column=0, row=row_col1
        )

        incomes_total = self._incomes_sum()
        row_col1 += 1
        tk.Label(text=f"Incomes total:        {incomes_total} Kč").grid(
            column=0, row=row_col1
        )

        # SHOW GRAPH

        # ----ENTRIES----
        years = self._db.get_list_of_years()
        self._entry_year_graph = tk.StringVar(self._window)

        tk.OptionMenu(self._window, self._entry_year_graph, *years).grid(
            column=3, row=3
        )

        # ----BUTTONS----
        # Show graph for given year
        tk.Button(
            text="Show graph for year: ", command=self._plot_graphs
        ).grid(column=1, row=3)

        # NEW RECORD FORM

        # -----LABELS------
        # Header
        row_col4 = 0
        tk.Label(self._window, text="### New record form ###").grid(
            column=4, row=row_col4, columnspan=2
        )

        # Type of record
        row_col4 += 1
        tk.Label(self._window, text="Type of record: (*)").grid(
            column=4, row=row_col4
        )

        # Category
        row_col4 += 1
        tk.Label(self._window, text="Category: (*)").grid(
            column=4, row=row_col4
        )

        # Year
        row_col4 += 1
        tk.Label(text="Year: (*)").grid(column=4, row=row_col4)

        # Month
        row_col4 += 1
        tk.Label(text="Month (number): (*)").grid(column=4, row=row_col4)

        # Day
        row_col4 += 1
        tk.Label(text="Day: ").grid(column=4, row=row_col4)

        # Amount
        row_col4 += 1
        tk.Label(text="Amount: (*)").grid(column=4, row=row_col4)

        # Note
        row_col4 += 1
        tk.Label(text="Note: ").grid(column=4, row=row_col4)

        # -----ENTRIES------
        # Type of record
        row_col5 = 1
        self._entry_expinc = tk.StringVar(self._window)
        self._entry_expinc.set("Expense")

        entr_expinc = tk.OptionMenu(
            self._window, self._entry_expinc, "Expense", "Income"
        )
        entr_expinc.grid(column=5, row=row_col5)

        # Category
        row_col5 += 1
        self._entry_category = tk.StringVar(self._window)

        entr_category = tk.OptionMenu(
            self._window, self._entry_category, *CATEGORIES
        )
        entr_category.grid(column=5, row=row_col5)

        # Year
        row_col5 += 1

        self._entry_year = tk.Entry()
        self._entry_year.insert(tk.END, str(datetime.now().year))
        self._entry_year.grid(column=5, row=row_col5)

        # Month
        row_col5 += 1

        self._entry_month = tk.StringVar(self._window)
        currentMonth = MONTHS[datetime.now().month - 1]  # datetime.now().month
        self._entry_month.set(currentMonth)

        entr_month = tk.OptionMenu(self._window, self._entry_month, *MONTHS)
        entr_month.grid(column=5, row=row_col5)

        # Date
        row_col5 += 1
        self._entry_date = tk.Entry()
        self._entry_date.insert(tk.END, str(datetime.now().day))
        self._entry_date.grid(column=5, row=row_col5)

        # Amount
        row_col5 += 1
        self._entry_amount = tk.Entry()
        self._entry_amount.grid(column=5, row=row_col5)

        # Note
        row_col5 += 1
        self._entry_note = tk.Entry()
        self._entry_note.grid(column=5, row=row_col5)

        # ----BUTTONS-----
        # Add a new record
        row_col5 += 1
        tk.Button(text="Add a new record", command=self._add_record).grid(
            column=5, row=row_col5
        )

        self._window.mainloop()

    def _plot_graphs(self):
        year = str(self._entry_year_graph.get())

        if year != "":
            self._backend._graph_data(int(year))

    def _expenses_sums(self):
        current_month = datetime.now().month - 1

        all_categories = []
        source_list = self._db.get_sums_expenses(datetime.now().year)
        for category in range(7):  # TODO: use categories list
            single_category = source_list[category]
            single_category_single_month = single_category[current_month]
            all_categories.append(single_category_single_month)

        return all_categories

    def _incomes_sum(self):
        current_month = datetime.now().month - 1
        all_months = self._db.get_sums_incomes(datetime.now().year)
        current_month_sum = all_months[current_month]

        return current_month_sum


if __name__ == "__main__":
    gui = Gui()
