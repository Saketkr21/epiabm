#
# Sweeps for taking care of the interventions
#

from pyEpiabm.core import Parameters
from pyEpiabm.intervention import CaseIsolation
from pyEpiabm.intervention import PlaceClosure
from pyEpiabm.intervention import HouseholdQuarantine

from .abstract_sweep import AbstractSweep


class InterventionSweep(AbstractSweep):
    """Class to sweep through all possible interventions.
    Check if intervention should take place based on time (and/or threshold).

    Possible interventions:

            * `case_isolation`: Symptomatic case stays home.
            * `household quarantine`: Household quarantine if member
                                      is symptomatic
    """

    def __init__(self):
        """Call in variables from the parameters file and set flags.
        """
        # Implemented interventions and their activity status
        self.intervention_active_status = {}
        self.intervention_params = Parameters.instance().intervention_params

    def bind_population(self, population):
        self._population = population
        intervention_dict = {'case_isolation': CaseIsolation,
                             'place_closure': PlaceClosure,
                             'household_quarantine': HouseholdQuarantine}
        for intervention in self.intervention_params.keys():
            params = self.intervention_params[intervention]
            self.intervention_active_status[(intervention_dict[intervention](
                population=self._population, **params))] = False

    def __call__(self, time):
        """
        Perform interventions that should take place.

        Parameters
        ----------
        time : float
            Simulation time
        """
        for intervention in self.intervention_active_status.keys():
            # TODO:
            # - Include an alternative way of case-count.
            #   Idealy this will be a global parameter that we can plot
            # - Include condition on ICU
            #   Intervention will be activated based on time and cases now.
            #   We would like to implement a threshold based on ICU numbers.
            num_cases = sum(map(lambda cell: cell.number_infectious(),
                            self._population.cells))
            if intervention.is_active(time, num_cases):
                intervention(time)
                if self.intervention_active_status[intervention] is False:
                    self.intervention_active_status[intervention] = True

            elif self.intervention_active_status[intervention] is True:
                # turn off intervention
                self.intervention_active_status[intervention] = False
                intervention.turn_off()
