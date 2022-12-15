import tkinter as tk
import tkinter.messagebox
from datetime import datetime

import backend as backend

window = tk.Tk()
window.title("My awesome budget app")

# magic for icon
img = tk.PhotoImage(file="wallet.png")
window.tk.call("wm", "iconphoto", window._w, img)

# Define lists
categories = [
    "Living",
    "Travel",
    "Food",
    "Shopping",
    "Services",
    "Household",
    "Misc",
]
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def expenses_sums():
    # Define actual month
    month = datetime.now().month - 1

    all_categories = []

    # Get tuple of 7 individual categories
    source_list = backend.updateExpSums(datetime.now().year)

    for category in range(7):
        # Get single category list from tuple
        single_category = source_list[category]
        # Get single month from category list
        single_category_single_month = single_category[month]

        # Make final list of sums
        all_categories.append(single_category_single_month)

    return all_categories


def incomes_sum():
    # Define actual month
    actual_month = datetime.now().month - 1

    # Get list of monthly sums
    all_months = backend.updateIncSums(2018)
    # Get actual month sum
    actual_month_sum = all_months[actual_month]

    return actual_month_sum


def graphs():
    year = str(entry_year_graph.get())

    if year != "":
        backend.graph_data(int(year), categories)

    else:
        pass


def add_record():
    error = 0

    # Get type of record entry (Expense/Income)
    if entry_expinc.get() == "Expense":
        expinc = 0

    elif entry_expinc.get() == "Income":
        expinc = 1

    else:
        pass

    # Handle empty category entry for expense and income record
    if entry_category.get() == "" and expinc == 0:
        tk.messagebox.showerror("Error", "Please, choose a category!")
        error += 1

    elif expinc == 1:
        category = 0
        error += 0

    else:
        category = categories.index(entry_category.get()) + 1
        error += 0

    # Handle enpty year entry
    if entry_year.get() == "":
        tk.messagebox.showerror("Error", "Please, insert a year!")
        error += 1

    else:
        year = entry_year.get()
        error += 0

    # Get month entry
    month = months.index(entry_month.get()) + 1
    # Get date entry
    date = entry_date.get()

    # Handle empty amount entry
    if entry_amount.get() == "":
        tk.messagebox.showerror("Error", "Please, insert an amount!")
        error += 1

    else:
        amount = entry_amount.get()
        error += 0

    # Get note entry
    note = entry_note.get()

    # Add a new record when all required entries filled
    if error == 0:
        # backend.addRecord(expinc, category, year, month, date, amount, note)

        print("ready to add")
        print(
            f"expinc: {expinc}  category: {category}  year: {year}  month: {month}  date: {date}  amount: {amount} note: {note}"  # noqa: E501
        )

        tk.messagebox.showinfo(
            "Add a new record", "New record has been successfully added."
        )
    else:
        pass


# ----LABELS------
row_col1 = 0
tk.Label(text="Welcome to my App").grid(column=0, row=row_col1)

row_col1 += 1
tk.Label(text="Expenses this month:").grid(column=0, row=row_col1)

# Monthly sums
expenses_sums = expenses_sums()

for i in range(len(categories)):
    category_name = categories[i]
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

incomes_total = incomes_sum()

row_col1 += 1
tk.Label(text=f"Incomes total:        {incomes_total} Kč").grid(
    column=0, row=row_col1
)

# SHOW GRAPH

# ----ENTRIES----
years = backend.listOfYears()
entry_year_graph = tk.StringVar(window)

entr_year_graph = tk.OptionMenu(window, entry_year_graph, *years).grid(
    column=3, row=3
)

# ----BUTTONS----
# Show graph for given year
button2 = tk.Button(text="Show graph for year: ", command=graphs).grid(
    column=1, row=3
)

# NEW RECORD FORM

# -----LABELS------
# Header
row_col4 = 0
tk.Label(window, text="### New record form ###").grid(
    column=4, row=row_col4, columnspan=2
)

# Type of record
row_col4 += 1
tk.Label(window, text="Type of record: (*)").grid(column=4, row=row_col4)

# Category
row_col4 += 1
tk.Label(window, text="Category: (*)").grid(column=4, row=row_col4)

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
entry_expinc = tk.StringVar(window)
entry_expinc.set("Expense")

entr_expinc = tk.OptionMenu(window, entry_expinc, "Expense", "Income")
entr_expinc.grid(column=5, row=row_col5)

# Category
row_col5 += 1
entry_category = tk.StringVar(window)

entr_category = tk.OptionMenu(window, entry_category, *categories)
entr_category.grid(column=5, row=row_col5)

# Year
row_col5 += 1

entry_year = tk.Entry()
entry_year.insert(tk.END, datetime.now().year)
entry_year.grid(column=5, row=row_col5)

# Month
row_col5 += 1

entry_month = tk.StringVar(window)
currentMonth = months[datetime.now().month - 1]  # datetime.now().month
entry_month.set(currentMonth)

entr_month = tk.OptionMenu(window, entry_month, *months)
entr_month.grid(column=5, row=row_col5)

# Date
row_col5 += 1
entry_date = tk.Entry()
entry_date.insert(tk.END, datetime.now().day)
entry_date.grid(column=5, row=row_col5)

# Amount
row_col5 += 1
entry_amount = tk.Entry()
entry_amount.grid(column=5, row=row_col5)

# Note
row_col5 += 1
entry_note = tk.Entry()
entry_note.grid(column=5, row=row_col5)

# ----BUTTONS-----
# Add a new record
row_col5 += 1
button1 = tk.Button(text="Add a new record", command=add_record).grid(
    column=5, row=row_col5
)


window.mainloop()
