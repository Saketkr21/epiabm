import unittest
import pyEpiabm as pe


class TestQueueSweep(unittest.TestCase):
    """Test the Host Progression Sweep function.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up a population we can use throughout the test.
        2 people are located in one microcell.
        """
        cls.pop_factory = pe.ToyPopulationFactory()
        cls.test_population = cls.pop_factory.make_pop(2, 1, 1, 1, True)

        cls.cell = cls.test_population.cells[0]
        cls.person1 = cls.test_population.cells[0].microcells[0].persons[0]
        cls.person1.infection_status = pe.InfectionStatus.InfectMild
        cls.person2 = cls.test_population.cells[0].microcells[0].persons[1]

        cls.time = 1

    def test_bind(self):
        self.test_sweep = pe.QueueSweep()
        self.test_sweep.bind_population(self.test_population)
        self.assertEqual(self.test_sweep._population.cells[0]
                         .persons[0].infection_status,
                         pe.InfectionStatus.InfectMild)

    def test_call(self):
        """Test the main function of the Queue Sweep.
        Person 2 is enqueued.
        Checks the populations updates as expected.
        """
        self.cell.enqueue_person(self.person2)
        test_sweep = pe.QueueSweep()
        test_sweep.bind_population(self.test_population)
        # Test that the queue has one person
        self.assertFalse(self.cell.person_queue.empty())

        # Run the Queue Sweep.
        test_sweep(self.time)

        # Check queue is cleared.
        self.assertTrue(self.cell.person_queue.empty())
        # Check person 2 has updated status
        self.assertEqual(self.person2.infection_status,
                         pe.InfectionStatus.InfectMild)
        # Check person 2 has updated time
        self.assertEqual(self.person2.time_of_status_change,
                         self.time)


if __name__ == '__main__':
    unittest.main()
