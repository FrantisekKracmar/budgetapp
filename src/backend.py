import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
from database import Database
from entities.categories import CATEGORIES
from entities.months import MONTHS
from entities.record_type import RecordType
from matplotlib import style

style.use("seaborn-bright")


class Backend:
    """
    Co to vlastne umi:
        1)Vlozit zaznam z prikazove radky
        2)Sumy nad vsemi zaznamy
        3)Seznam roku pro uzivatelsky vyber
        4)Vytvoreni seznamu kategorii
        5)Uzivatelske rozhrani - shell
        6)Grafy pro zvoleny rok z nabidky
    """

    def __init__(self):
        self._db = Database()

    def show_user_interface(self):
        """Main menu in shell"""

        print("Welcome to my Awesome app")
        print(" ")
        print("Main menu:")
        print("1...Add a new record")
        print("2...Show some graphs")
        print("3...settings")

        user_input = int(input("What would you like to do?(1-3): "))

        if user_input == 1:
            self._add_new_record()
        elif user_input == 2:
            print(" ")
            print("Existing data for years: ")

            # Lets user choose for which year do sumups
            available_years = self._db.get_list_of_years()
            for year in range(len(available_years)):
                print(available_years[year])
            chosen_year = int(input("Which year do you want to see the sums for?: "))

            if chosen_year in available_years:
                self._graph_data(chosen_year)
            else:
                print(f"Sorry, there are no available data for year {chosen_year}")

        elif user_input == 3:
            print("Sorry, you this feature is not implemented yet :(")
        else:
            print("Please input number from 1 to 3")

    def _add_new_record(self):
        print("--------------------------")
        print("You are adding a new record")
        record_type = RecordType(int(input("0 for expense, 1 for income: ")))
        print("--------------------------")

        if record_type == RecordType.EXPENSE:
            for i in range(len(CATEGORIES)):
                print("%s...%s" % (i + 1, CATEGORIES[i]))
            category = int(input("Number of category: "))
        else:
            category = int()

        year = int(input("Year: "))
        month = int(input("Month: "))
        date = int(input("Day: "))
        amount = int(input("Amount: "))
        note = input("Note: ")
        self._db.add_record(
            record_type, category, year, month, date, amount, note
        )

    def _graph_data(self, year: int):
        """Show expenses for whole year for each category"""
        colors = ["b", "g", "r", "c", "m", "y", "k"]

        all_categories = self._db.get_sums_expenses(year)

        months = []
        for month in range(1, len(MONTHS) + 1):  # TODO: values are 1-12
            months.append(dt.datetime(year=year, month=month, day=1))

        y_max = np.max(all_categories)

        plt.title("Monthly sums of categories during the year %s" % year)
        plt.xlabel("Month")
        plt.ylabel("Amount [Kc]")
        plt.axis([months[0], months[11], 0, y_max])
        plt.xticks(rotation=45)

        for category in range(0, 7):
            plt.plot(months, all_categories[category], colors[category])

        plt.legend(
            CATEGORIES, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0
        )

        plt.show(block=True)

if __name__ == "__main__":
    "Show shell interface"
    backend = Backend()
    backend.show_user_interface()
