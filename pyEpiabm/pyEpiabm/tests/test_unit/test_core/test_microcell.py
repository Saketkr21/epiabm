import unittest
from unittest import mock

import pyEpiabm as pe
from pyEpiabm.property import PlaceType, InfectionStatus
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestMicrocell(TestPyEpiabm):
    """Test the 'Microcell' class.
    """
    def setUp(self) -> None:
        self.cell = pe.Cell()
        self.microcell = pe.Microcell(self.cell)

    def test__init__(self):
        self.assertEqual(self.microcell.persons, [])
        self.assertEqual(self.microcell.cell, self.cell)
        self.assertEqual(self.microcell.places, [])

    def test_repr(self):
        self.assertEqual(repr(self.microcell),
                         "Microcell with 0 people at location (0, 0).")

    def test_set_id(self):
        self.assertEqual(self.microcell.id, hash(self.microcell))
        self.microcell.set_id(2.0)
        self.assertEqual(self.microcell.id, 2.0)

    def test_add_person(self):
        self.assertEqual(len(self.microcell.persons), 0)
        self.assertEqual(len(self.cell.persons), 0)

        sus_person = pe.Person(self.microcell)
        self.microcell.add_person(sus_person)
        self.assertEqual(len(self.microcell.persons), 1)
        self.assertEqual(len(self.cell.persons), 1)
        self.assertEqual(self.cell.number_infectious(), 0)
        self.assertEqual(self.microcell.persons[0].age, sus_person.age)

        inf_person = pe.Person(self.microcell)
        inf_person.infection_status = InfectionStatus.InfectASympt
        self.microcell.add_person(inf_person)
        self.assertEqual(len(self.microcell.persons), 2)
        self.assertEqual(len(self.cell.persons), 2)
        self.assertEqual(self.cell.number_infectious(), 1)

    def test_add_people(self, n=4):
        self.assertEqual(len(self.microcell.persons), 0)
        self.assertEqual(len(self.cell.persons), 0)
        self.microcell.add_people(n)
        self.assertEqual(len(self.microcell.persons), n)
        self.assertEqual(self.cell.number_infectious(), 0)
        self.assertEqual(len(self.cell.persons), n)
        self.microcell.add_people(n + 1,
                                  InfectionStatus.InfectASympt)
        self.assertEqual(len(self.microcell.persons), 2 * n + 1)
        self.assertEqual(len(self.cell.persons), 2 * n + 1)
        self.assertEqual(self.cell.number_infectious(), n + 1)

    def test_add_place(self, n=3):
        self.assertEqual(len(self.microcell.places), 0)
        self.microcell.add_place(n, (1.0, 1.0), PlaceType.Workplace)
        self.assertEqual(len(self.microcell.places), n)

    def test_setup(self, n=5):
        self.assertEqual(len(self.cell.microcells), 0)
        self.cell.add_microcells(n)
        self.assertEqual(len(self.cell.microcells), n)

    def test_add_household(self):
        self.microcell.add_people(1)
        self.microcell.add_household(self.microcell.persons)
        self.assertEqual(len(self.microcell.households), 1)
        household = self.microcell.households[0]
        self.assertEqual(len(household.persons), 1)

    @mock.patch('logging.info')
    def test_logging(self, mock_log):
        self.microcell.add_household(self.microcell.persons)
        mock_log.assert_called_once()

    def test_report(self):
        self.microcell.add_people(5)
        self.microcell.notify_person_status_change(
            pe.property.InfectionStatus.Susceptible,
            pe.property.InfectionStatus.Recovered,
            self.microcell.persons[0].age_group)

    def test_set_location(self):
        local_cell = pe.Cell(loc=(-2, 3.2))
        microcell = pe.Microcell(local_cell)
        self.assertEqual(microcell.location[0], -2)
        self.assertEqual(microcell.location[1], 3.2)
        self.assertRaises(ValueError, microcell.set_location, (1, 1, 1))
        self.assertRaises(ValueError, microcell.set_location, (1, (8, 6)))
        self.assertRaises(ValueError, microcell.set_location, ('1', 1))

    def test_count_icu(self):
        self.microcell.add_people(6)
        for person in self.microcell.persons[:4]:
            person.update_status(InfectionStatus(7))
        self.assertEqual(self.microcell.count_icu(), 4)

    def test_count_infectious(self):
        self.microcell.add_people(6)
        for i in range(4):
            person = self.microcell.persons[i]
            person.update_status(InfectionStatus(i+3))
        self.assertEqual(self.microcell.count_infectious(), 4)


if __name__ == '__main__':
    unittest.main()
