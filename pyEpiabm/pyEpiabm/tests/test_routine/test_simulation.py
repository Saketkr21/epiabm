import os
import unittest
import pyEpiabm as pe
from unittest.mock import patch, mock_open


class TestSimulation(unittest.TestCase):
    """Tests the 'Simulation' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.pop_factory = pe.routine.ToyPopulationFactory()
        cls.test_population = cls.pop_factory.make_pop(0, 1, 1, 1)
        pe.core.Parameters.instance().time_steps_per_day = 1
        cls.sim_params = {"simulation_start_time": 0,
                          "simulation_end_time": 2,
                          "initial_infected_number": 0}

        cls.file_params = {"output_file": "test_file.csv",
                           "output_dir": "pyEpiabm/pyEpiabm/tests"}

        cls.initial_sweeps = [pe.sweep.InitialInfectedSweep()]
        cls.sweeps = [pe.sweep.PlaceSweep()]

    def test_configure(self):
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):

            filename = os.path.join(os.getcwd(),
                                    self.file_params["output_dir"],
                                    self.file_params["output_file"])
            test_sim = pe.routine.Simulation()

            # Test configure binds parameters as expected.
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params)
            self.assertEqual(len(test_sim.initial_sweeps), 1)
            self.assertEqual(len(test_sim.sweeps), 1)
            self.assertIsInstance(test_sim.population, pe.core.Population)
            del(test_sim.writer)
        mo.assert_called_with(filename, 'w')

    @patch('pyEpiabm.sweep.PlaceSweep.__call__')
    @patch('pyEpiabm.sweep.InitialInfectedSweep.__call__')
    @patch('pyEpiabm.routine.Simulation.write_to_file')
    def test_run_sweeps(self, patch_write, patch_initial, patch_sweep):
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):

            time_sweep = self.sim_params["simulation_start_time"] + 1
            time_write = self.sim_params["simulation_end_time"] - 1
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params)
            test_sim.run_sweeps()
            patch_initial.assert_called_with(self.sim_params)
            patch_sweep.assert_called_with(time_sweep)
            patch_write.assert_called_with(time_write)

    def test_write_to_file(self):
        mo = mock_open()
        with patch('pyEpiabm.output._csv_dict_writer.open', mo):
            time = 1
            test_sim = pe.routine.Simulation()
            test_sim.configure(self.test_population, self.initial_sweeps,
                               self.sweeps, self.sim_params, self.file_params)
            data = {s: 0 for s in list(pe.property.InfectionStatus)}
            data["time"] = time

            with patch.object(test_sim.writer, 'write') as mock:
                test_sim.write_to_file(time)
                mock.assert_called_with(data)


if __name__ == '__main__':
    unittest.main()
