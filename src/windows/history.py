import tkinter as tk
from tkinter import ttk

from database import Database
from entities.record_type import RecordType


class History:
    def __init__(self, master, main_window):
        self._master = master
        self._master.title("History")
        self._main_window = main_window

        self._db = Database()

        self._frame = tk.Frame(self._master)
        self._frame.pack(side="top", fill="both", expand=True)
        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)

        self._render_content()

    def _render_content(self):
        tabControl = ttk.Notebook(self._master)

        self._expenses_tab = ttk.Frame(tabControl)
        self._incomes_tab = ttk.Frame(tabControl)

        tabControl.add(self._expenses_tab, text="Expenses")
        tabControl.add(self._incomes_tab, text="Incomes")
        tabControl.pack(expand=1, fill="both")

        last_expenses = self._db.get_last_records(10, RecordType.EXPENSE)

        tk.Label(self._expenses_tab, text="ID").grid(column=0, row=0)
        tk.Label(self._expenses_tab, text="Category").grid(column=2, row=0)
        tk.Label(self._expenses_tab, text="Year").grid(column=3, row=0)
        tk.Label(self._expenses_tab, text="Month").grid(column=4, row=0)
        tk.Label(self._expenses_tab, text="Day").grid(column=5, row=0)
        tk.Label(self._expenses_tab, text="Amount").grid(column=6, row=0)
        tk.Label(self._expenses_tab, text="Note").grid(column=7, row=0)

        for i, record in enumerate(last_expenses):
            row_i = 1 + i
            tk.Label(self._expenses_tab, text=f"{record[0]}").grid(
                column=0, row=row_i
            )
            tk.Label(self._expenses_tab, text=f"{record[2]}").grid(
                column=2, row=row_i
            )
            tk.Label(self._expenses_tab, text=f"{record[3]}").grid(
                column=3, row=row_i
            )
            tk.Label(self._expenses_tab, text=f"{record[4]}").grid(
                column=4, row=row_i
            )
            tk.Label(self._expenses_tab, text=f"{record[5]}").grid(
                column=5, row=row_i
            )
            tk.Label(self._expenses_tab, text=f"{record[6]}").grid(
                column=6, row=row_i
            )
            tk.Label(self._expenses_tab, text=f"{record[7]}").grid(
                column=7, row=row_i
            )
            tk.Button(
                self._expenses_tab,
                text="Edit record",
                command=lambda row=row_i: self._edit_expense_record(row),
            ).grid(column=8, row=row_i)

        last_incomes = self._db.get_last_records(10, RecordType.INCOME)

        tk.Label(self._incomes_tab, text="ID").grid(column=0, row=0)
        tk.Label(self._incomes_tab, text="Year").grid(column=1, row=0)
        tk.Label(self._incomes_tab, text="Month").grid(column=2, row=0)
        tk.Label(self._incomes_tab, text="Day").grid(column=3, row=0)
        tk.Label(self._incomes_tab, text="Amount").grid(column=4, row=0)
        tk.Label(self._incomes_tab, text="Note").grid(column=5, row=0)

        for i, record in enumerate(last_incomes):
            row_i = 1 + i
            tk.Label(self._incomes_tab, text=f"{record[0]}").grid(
                column=0, row=row_i
            )
            tk.Label(self._incomes_tab, text=f"{record[3]}").grid(
                column=1, row=row_i
            )
            tk.Label(self._incomes_tab, text=f"{record[4]}").grid(
                column=2, row=row_i
            )
            tk.Label(self._incomes_tab, text=f"{record[5]}").grid(
                column=3, row=row_i
            )
            tk.Label(self._incomes_tab, text=f"{record[6]}").grid(
                column=4, row=row_i
            )
            tk.Label(self._incomes_tab, text=f"{record[7]}").grid(
                column=5, row=row_i
            )
            tk.Button(
                self._incomes_tab,
                text="Edit record",
                command=lambda row=row_i: self._edit_icome_record(row),
            ).grid(column=6, row=row_i)

    def _edit_expense_record(self, row: int):
        record_id = int(self._expenses_tab.grid_slaves(row, 0)[0].cget("text"))
        self._main_window._show_edit_form(record_id)

    def _edit_icome_record(self, row: int):
        record_id = int(self._incomes_tab.grid_slaves(row, 0)[0].cget("text"))
        self._main_window._show_edit_form(record_id)
