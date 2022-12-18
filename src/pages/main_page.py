import tkinter as tk
from datetime import datetime

from backend import Backend
from database import Database
from entities.categories import CATEGORIES
from windows.add_record import AddRecord
from windows.edit_record import EditRecord
from windows.history import History


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self._controller = controller

        self._db = Database()
        self._backend = Backend()

        self._render_content()

    def _render_content(self):
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

        tk.Button(
            self, text="Add new record", command=self._show_record_form
        ).grid(column=1, row=0)
        tk.Button(self, text="Show history", command=self._show_history).grid(
            column=1, row=1
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

    def _plot_graphs(self):
        year = str(self._entry_year_graph.get())

        if year != "":
            self._backend._graph_data(int(year))

    def _expenses_sums(self):
        current_month_index = datetime.now().month - 1

        all_categories = []
        source_list = self._db.get_sums_expenses(datetime.now().year)
        for category in range(len(CATEGORIES)):
            single_category = source_list[category]
            single_category_single_month = single_category[current_month_index]
            all_categories.append(single_category_single_month)

        return all_categories

    def _incomes_sum(self):
        current_month = datetime.now().month - 1
        all_months = self._db.get_sums_incomes(datetime.now().year)
        current_month_sum = all_months[current_month]

        return current_month_sum

    def _show_record_form(self):
        window = self._create_new_window()
        AddRecord(window)

    def _show_history(self):
        window = self._create_new_window()
        History(window, self)

    def _show_edit_form(self, record_id: int):
        window = self._create_new_window()
        EditRecord(window, record_id)
    
    def _create_new_window(self):
        new_window = tk.Toplevel(self.master)
        img = tk.PhotoImage(file=self._controller.icon)
        self._controller.call("wm", "iconphoto", new_window._w, img)
        return new_window
