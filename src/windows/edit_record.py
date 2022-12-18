import tkinter as tk
import tkinter.messagebox as messagebox

from database import Database
from entities.categories import CATEGORIES
from entities.months import MONTHS
from entities.record_type import RecordType


class EditRecord:
    def __init__(self, master, id: int):
        self._master = master
        self._master.title("Edit record")
        self._id = id

        self._db = Database()

        self._frame = tk.Frame(self._master)
        self._frame.pack(side="top", fill="both", expand=True)
        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)

        self._render_content()

    def _render_content(self):
        record = self._db.get_record(self._id)

        record_type_value = "Expense" if int(record[1]) == 0 else "Income"

        tk.Label(self._frame, text="Type of record: (*)").grid(column=0, row=0)
        tk.Label(self._frame, text="Category: (*)").grid(column=0, row=1)
        tk.Label(self._frame, text="Year: (*)").grid(column=0, row=2)
        tk.Label(self._frame, text="Month (number): (*)").grid(column=0, row=3)
        tk.Label(self._frame, text="Day: ").grid(column=0, row=4)
        tk.Label(self._frame, text="Amount: (*)").grid(column=0, row=5)
        tk.Label(self._frame, text="Note: ").grid(column=0, row=6)

        # -----ENTRIES------
        self._entry_record_type = tk.StringVar()
        self._entry_record_type.set(record_type_value)
        tk.OptionMenu(
            self._frame, self._entry_record_type, "Expense", "Income"
        ).grid(column=1, row=0)
        self._entry_category = tk.StringVar()
        self._entry_category.set(
            CATEGORIES[int(record[2]) - 1]
        )  # TODO: magic constant, use list
        tk.OptionMenu(self._frame, self._entry_category, *CATEGORIES).grid(
            column=1, row=1
        )

        self._entry_year = tk.Entry(self._frame)
        self._entry_year.insert(tk.END, record[3])
        self._entry_year.grid(column=1, row=2)

        self._entry_month = tk.StringVar()
        currentMonth = MONTHS[record[4] - 1]
        self._entry_month.set(currentMonth)
        tk.OptionMenu(self._frame, self._entry_month, *MONTHS).grid(
            column=1, row=3
        )

        self._entry_date = tk.Entry(self._frame)
        self._entry_date.insert(tk.END, record[5])
        self._entry_date.grid(column=1, row=4)

        self._entry_amount = tk.Entry(self._frame)
        self._entry_amount.insert(tk.END, record[6])
        self._entry_amount.grid(column=1, row=5)

        self._entry_note = tk.Entry(self._frame)
        self._entry_note.insert(tk.END, record[7])
        self._entry_note.grid(column=1, row=6)

        tk.Button(
            self._frame,
            text="Save record",
            bg="green",
            command=self._save_record,
        ).grid(column=1, row=7)

        self.quitButton = tk.Button(
            self._frame,
            text="Cancel",
            width=15,
            bg="red",
            command=self.close_window,
        ).grid(column=0, row=8)

    def _save_record(self):
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
            )  # TODO: magic constant, use list
            year = int(self._entry_year.get())
            month = (
                MONTHS.index(self._entry_month.get()) + 1
            )  # TODO: magic constant, use list
            date = int(self._entry_date.get())
            amount = int(self._entry_amount.get())
            note = self._entry_note.get()

            self._db.update_record(
                self._id,
                record_type,
                category,
                year,
                month,
                date,
                amount,
                note,
            )

            messagebox.showinfo(
                "Add a new record", "Record was successfully updated."
            )
            self.close_window()

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

    def close_window(self):
        self._master.destroy()
