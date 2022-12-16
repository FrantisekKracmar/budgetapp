import sqlite3

from entities.categories import CATEGORIES
from entities.months import MONTHS
from entities.record_type import RecordType


class Database:
    _DATABASE_NAME = "records.db"
    _db: sqlite3.Connection

    def __init__(self, database_path=None) -> None:
        database_path = database_path if database_path else self._DATABASE_NAME
        self._db = sqlite3.connect(database_path)
        cursor = self._db.cursor()
        query = (
            "create table"
            " if not exists"
            " records ("
            " id INTEGER PRIMARY KEY,"
            " typ TEXT,"
            " category TEXT,"
            " year INTEGER,"
            " month INTEGER,"
            " day INTEGER,"
            " amount INTEGER,"
            " note TEXT,"
            " indexExp INTEGER,"
            " indexInc INTEGER)"
        )
        cursor.execute(query)
        self._db.commit()

    def __del__(self):
        self._db.commit()
        self._db.close()

    def add_record(
        self,
        record_type: RecordType,
        category: int,
        year: int,
        month: int,
        day: int,
        amount: int,
        note: str,
    ):
        """Adds a new record to the database"""
        if record_type == RecordType.EXPENSE:
            index_exp = self._new_index(RecordType.EXPENSE)
            index_inc = 0
        else:
            index_exp = 0
            index_inc = self._new_index(RecordType.INCOME)

        cursor = self._db.cursor()
        values = (
            record_type.value,
            category,
            year,
            month,
            day,
            amount,
            note,
            index_exp,
            index_inc,
        )
        query = (
            "INSERT INTO records"
            " (typ, category, year, month, day,"
            " amount, note, indexExp, indexInc)"
            " VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        cursor.execute(query, values)
        self._db.commit()

    def _new_index(self, record_type: RecordType) -> int:
        """Gets following index number for respected type of record"""
        cursor = self._db.cursor()
        column = (
            "indexExp" if record_type == RecordType.EXPENSE else "indexInc"
        )
        query = (
            f"SELECT MAX({column}) FROM records WHERE typ=={record_type.value}"
        )
        cursor.execute(query)
        last_index = cursor.fetchone()
        new_index = 1 if last_index[0] is None else last_index[0] + 1

        return new_index

    def get_list_of_years(self) -> list:
        """Return list of years with existing expenses records"""
        cursor = self._db.cursor()
        cursor.row_factory = lambda cursor, row: row[0]
        query = "SELECT DISTINCT(year) FROM records"
        cursor.execute(query)
        list_of_years = cursor.fetchall()

        return list_of_years

    def get_sums_expenses(self, year: int) -> list:
        "Get sums of expenses for given year"
        all_categories = []
        cursor = self._db.cursor()

        for category in range(1, len(CATEGORIES) + 1):  # TODO: values are 1-7
            singleCategory = []

            for month in range(1, len(MONTHS) + 1):  # TODO: values are 1-12
                query = (
                    "SELECT SUM(amount)"
                    " FROM records"
                    " WHERE typ = " + str(RecordType.EXPENSE.value) + " AND"
                    " year = " + str(year) + " AND"
                    " month = " + str(month) + " AND"
                    " category = " + str(category)
                )
                cursor.execute(query)
                sum = cursor.fetchone()
                sum = sum[0] if sum[0] is not None else 0

                singleCategory.append(sum)

            all_categories.append(singleCategory)

        return all_categories

    def get_sums_incomes(self, year: int) -> list:
        "Get sums of incomes for given year"
        all_months = []
        cursor = self._db.cursor()

        for month in range(1, len(MONTHS) + 1):  # TODO: values are 1-12
            query = (
                "SELECT SUM(amount)"
                " FROM records"
                " WHERE typ = " + str(RecordType.INCOME.value) + " AND"
                " year = " + str(year) + " AND"
                " month = " + str(month)
            )
            cursor.execute(query)
            sum = cursor.fetchone()
            sum = sum[0] if sum[0] is not None else 0

            all_months.append(sum)

        return all_months


if __name__ == "__main__":
    pass
