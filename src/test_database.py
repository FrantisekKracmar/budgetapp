from database import Database
from entities.record_type import RecordType


class TestDatabase:
    database = Database("./src/test_data/test_records.db")

    def test__new_index(self):
        assert self.database._new_index(RecordType.EXPENSE) == 763
        assert self.database._new_index(RecordType.INCOME) == 745

    def test_get_list_of_years(self):
        assert self.database.get_list_of_years() == [2018, 2019]

    def test_get_sums_expenses(self):
        expected = [
            [
                25655,
                23365,
                13132,
                11998,
                27660,
                14422,
                29858,
                48683,
                24301,
                38375,
                32382,
                28577,
            ],
            [
                19168,
                4786,
                24611,
                46135,
                45971,
                44297,
                26011,
                50795,
                9156,
                38104,
                48454,
                13910,
            ],
            [
                50103,
                16244,
                36219,
                21406,
                29981,
                9895,
                28971,
                16732,
                19760,
                17086,
                17773,
                35375,
            ],
            [
                41393,
                49687,
                2427,
                49208,
                20827,
                34516,
                33834,
                12659,
                31270,
                40969,
                18822,
                16384,
            ],
            [
                54993,
                10764,
                20009,
                18064,
                31121,
                28992,
                44852,
                37466,
                16253,
                30843,
                24432,
                24388,
            ],
            [
                48103,
                40677,
                15168,
                36791,
                33828,
                34538,
                28064,
                17493,
                12130,
                20737,
                19827,
                28115,
            ],
            [
                22493,
                5696,
                9818,
                35905,
                30742,
                36081,
                25625,
                23257,
                26985,
                25214,
                16887,
                28184,
            ],
        ]
        assert self.database.get_sums_expenses(2018) == expected

    def test_get_sums_incomes(self):
        expected = [
            227439,
            223858,
            180269,
            143433,
            150324,
            159288,
            229267,
            116162,
            198059,
            160075,
            228118,
            243918,
        ]
        assert self.database.get_sums_incomes(2018) == expected
