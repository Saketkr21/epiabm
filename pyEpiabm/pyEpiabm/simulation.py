#
# Simulates a complete pandemic
#
from .abstract_sweep import AbstractSweep
from .infection_status import InfectionStatus
from ._csv_dict_writer import _CsvDictWriter
from .population import Population
import os
import typing


class Simulation:
    """Class to run a full simulation.
    """
    def configure(self,
                  population: Population,
                  initial_sweeps: typing.List[AbstractSweep],
                  sweeps: typing.List[AbstractSweep],
                  sim_params: typing.Dict,
                  file_params: typing.Dict):
        """Initialise a population structure for use in the simulation.

        :param population: Population structure for the model.
        :type population: Population
        :param pop_params: Dictionary of parameter specific to the population
        :type pop_params: dict
        :param initial_sweeps: List of abstract sweep used to initialise the
            simulation
        :type initial_sweeps: list
        :param sweeps: List of abstract sweeps used in the simulation. Queue
            sweep and host progression sweep must appear at the end of the
            list
        :type sweeps: list
        :param sim_params: Dictionary of parameters specific to the simulation
            used
        :type sim_params: dict
        :param file_params: Dictionary of parameters specific to the output
            file
        :type file_params: dict
        """
        self.sim_params = sim_params
        self.population = population
        self.initial_sweeps = initial_sweeps
        self.sweeps = sweeps
        # Initial sweeps configure the population by changing the type,
        # infection status, infectiveness or susceptibility of people
        # or places. Only implemented once.
        for s in initial_sweeps + sweeps:
            assert isinstance(s, AbstractSweep)
            s.bind_population(self.population)

        # General sweeps run through the population on every timestep, and
        # include host progression and spatial infections.

        filename = os.path.join(os.getcwd(),
                                file_params["output_dir"],
                                file_params["output_file"])

        self.writer = _CsvDictWriter(
            filename,
            ["time"] + [s for s in InfectionStatus])

    def run_sweeps(self):
        """Iteration step of the simulation. First the initialisation sweeps
        configure people and plarces within the population. Then at each
        timestep the update sweeps run first, updating the population. Then
        the required spatial infections sweeps are run, which enqueue
        people who have been in an infection event. Queue sweep runs next,
        updating the enqueued people to infected. Finally, host progression
        sweep runs through individuals and updates their infection status
        at pre-determined timepoints. At each timepoint, a count of each
        infection status is written to file.
        """

        # Initialise on the time step before starting.
        t = self.sim_params["simulation_start_time"]
        for sweep in self.initial_sweeps:
            sweep(self.sim_params)
        # First entry of the data file is the initial state
        self.write_to_file(t)
        t += 1

        while t < self.sim_params["simulation_end_time"]:
            for sweep in self.sweeps:
                sweep(t)
            self.write_to_file(t)
            t += 1

    def write_to_file(self, time):
        """Records the count number of a given list of infection statuses
        and writes these to file.
        """
        data = {s: 0 for s in list(InfectionStatus)}
        for cell in self.population.cells:
            for k in data:
                data[k] += cell.compartment_counter.retrieve()[k]
        data["time"] = time

        self.writer.write(data)
