#
# Progression of infection within individuals
#
import random

import pyEpiabm as pe

import math

from pyEpiabm.property import InfectionStatus

from .abstract_sweep import AbstractSweep


class HostProgressionSweep(AbstractSweep):
    """Class for sweeping through population and updating host infection status
    and time to next infection status change.
    """

    def _update_time_to_status_change(self):
        """Assigns time until next infection status update,
         given as a random integer between 1 and 10.

        :return: Time until next infection status update
        :rtype: int
        """
        # This is left as a random integer for now but will be made more
        # complex later.
        new_time = random.randint(1, 10)
        return new_time

    def _set_latent_time(self):
        """Calculates and returns latency period as calculated in
        covid-sim to be given as time until next infection status
        for a person who has been set as exposed.
        """

        latent_period = pe.Parameters.instance().latent_period
        latent_period_iCDF = pe.Parameters.instance().latent_period_iCDF
        time_steps_per_day = pe.Parameters.instance().time_steps_per_day
        q = random.random() * pe.Parameters.instance().CDF_RES
        i = math.floor(q)
        q -= float(i)
        latent_time = 0.5 +\
            latent_period*( q * latent_period_iCDF[i + 1] +
                (1.0 - q) * latent_period_iCDF[i] *
                time_steps_per_day)

        latent_time = math.floor(latent_time)
        if latent_time < 0:
            raise AssertionError('Negative latent time')
        return latent_time

    def _update_next_infection_status(self, person):
        """Assigns next infection status based on
        current infection status.

        :param Person: Person class with infection status attributes
        :type Person: Person
        """
        # More infection statuses will be incorporated in future.
        if person.infection_status == InfectionStatus.InfectMild:
            person.next_infection_status = InfectionStatus.Recovered
        elif person.infection_status == InfectionStatus.Exposed:
            person.next_infection_status = InfectionStatus.InfectMild
        else:
            raise TypeError('update_next_infection_status should only ' +
                            'be applied to individuals with mild ' +
                            'infection status, or exposed')

    def __call__(self, time: int):
        """Sweeps through all people in the population and updates
        their infection status if it is time and assigns them their
        next infection status and a new time of next status change.

        :param time: Current simulation time
        :type time: int
        """

        for cell in self._population.cells:
            for person in cell.persons:
                if person.time_of_status_change == time:
                    person.update_status(person.next_infection_status)
                    if person.infection_status != InfectionStatus.Recovered:
                        self._update_next_infection_status(person)
                        if person.infection_status == InfectionStatus.Exposed:
                            person.time_of_status_change = time +\
                                 self._set_latent_time()
                        else:
                            person.time_of_status_change = time +\
                                 self._update_time_to_status_change()
