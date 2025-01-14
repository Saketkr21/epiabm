import unittest

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.mocked_logging_tests import TestMockedLogs


class TestPopulation(TestMockedLogs):
    """Test the 'Population' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        super(TestPopulation, cls).setUpClass()  # Sets up patch on logging
        cls.population = pe.Population()

    def test__init__(self):
        self.assertEqual(self.population.cells, [])

    def test_repr(self):
        self.assertEqual(repr(self.population),
                         "Population with 0 cells.")

    def test_add_cells(self, n=4):
        population = pe.Population()
        self.assertEqual(len(population.cells), 0)
        population.add_cells(n)
        self.assertEqual(len(population.cells), n)

    def test_total_people(self):
        self.assertEqual(self.population.total_people(), 0)


if __name__ == '__main__':
    unittest.main()
