#
# Progression of infection within individuals
#

import random
import numpy as np
from collections import defaultdict

import pyEpiabm as pe
from pyEpiabm.core import Parameters, Person
from pyEpiabm.property import InfectionStatus
from pyEpiabm.utility import StateTransitionMatrix, TransitionTimeMatrix

from .abstract_sweep import AbstractSweep


class HostProgressionSweep(AbstractSweep):
    """Class for sweeping through population and updating host infection status
    and time to next infection status change.

    """

    def __init__(self):
        """Initialise parameters to be used in class methods. State
        transition matrix is set where each row of the matrix corresponds
        to a current infection status of a person. The columns of that
        row then indicate the transition probabilities to the remaining
        infection statuses. Number of infection states is set by
        taking the size of the InfectionStatus enum. Transition time matrix
        is also initialised and associated parameters are called from the
        parameters class.

        """
        # Instantiate state transition matrix
        use_ages = Parameters.instance().use_ages
        coefficients = defaultdict(int, Parameters.instance()
                                   .host_progression_lists)
        matrix_object = StateTransitionMatrix(coefficients, use_ages)
        self.state_transition_matrix = matrix_object.matrix

        self.number_of_states = len(InfectionStatus)
        assert self.state_transition_matrix.shape == \
            (self.number_of_states, self.number_of_states),\
            'Matrix dimensions must match number of infection states'

        # Instantiate transmission time matrix
        time_matrix_object = TransitionTimeMatrix()
        self.transition_time_matrix =\
            time_matrix_object.create_transition_time_matrix()

        # Instantiate parameters to be used in update transition time
        # method
        self.latent_to_symptom_delay =\
            pe.Parameters.instance().latent_to_sympt_delay
        self.model_time_step = 1 / pe.Parameters.instance().time_steps_per_day
        self.delay = np.floor(self.latent_to_symptom_delay
                              / self.model_time_step)

    @staticmethod
    def set_infectiousness(person: Person):
        """Assigns the infectiousness of a person for when they go from
        the exposed infection state to the next state, either InfectAsympt,
        InfectMild or InfectGP.
        Called right after an exposed person has been given its
        new infection status in the call method below.
        This static method is non private as it is also used by the initial
        infected sweep to give new infected individuals an infectiousness.

        Parameters
        ----------
        Person : Person
            Instance of person class with infection status attributes

        Returns
        -------
        float
            Infectiousness of a person

        """
        init_infectiousness = np.random.gamma(1, 1)
        if person.infection_status == InfectionStatus.InfectASympt:
            infectiousness = (init_infectiousness
                              * pe.Parameters.instance().asympt_infectiousness)
        elif (person.infection_status == InfectionStatus.InfectMild or
              person.infection_status == InfectionStatus.InfectGP):
            infectiousness = (init_infectiousness
                              * pe.Parameters.instance().sympt_infectiousness)
        person.infectiousness = infectiousness

    def _update_next_infection_status(self, person: Person):
        """Assigns next infection status based on current infection status
        and on probabilities of transition to different statuses. Weights
        are taken from row in state transition matrix that corresponds to
        the person's current infection status. Weights are then used in
        random.choices method to select person's next infection status.

        Parameters
        ----------
        Person : Person
            Instance of person class with infection status attributes

        """
        if person.infection_status in [InfectionStatus.Recovered,
                                       InfectionStatus.Dead]:
            person.next_infection_status = None
        else:
            row_index = person.infection_status.name
            weights = self.state_transition_matrix.loc[row_index].to_numpy()
            weights = [w[person.age_group] if isinstance(w, list) else w
                       for w in weights]
            outcomes = range(1, self.number_of_states + 1)

            if len(weights) != len(outcomes):
                raise AssertionError('The number of infection statuses must' +
                                     'match the number of transition' +
                                     'probabilities')

            next_infection_status_number = random.choices(outcomes, weights)[0]
            next_infection_status =\
                InfectionStatus(next_infection_status_number)
            person.next_infection_status = next_infection_status

    def _update_time_status_change(self, person, time):
        """Calculates transition time as calculated in CovidSim,
        and updates the time_of_status_change for the given
        Person, given as the time until next infection status
        for a person who has a new infection status. If it is expected that
        the person will not transition again (for example in Recovered or Dead
        statuses), then the time of status change is set to infinity.

        Parameters
        ----------
        Person : Person
            Instance of Person class with :class:`InfectionStatus` attributes
        time : float
            Current simulation time

        """
        # Defines the transition time. If the person will not transition again,
        # the transition time is set to infinity. Else, the transition time is
        # defined using the TransitionTimeMatrix class, with the method
        # `choose` from the InverseCdf class.
        if person.infection_status in [InfectionStatus.Recovered,
                                       InfectionStatus.Dead]:
            transition_time = np.inf
        else:
            row_index = person.infection_status.name
            column_index = person.next_infection_status.name
            transition_time_icdf_object =\
                self.transition_time_matrix.loc[row_index, column_index]
            # Checks for susceptible to exposed case
            # where transition time is zero
            try:
                transition_time =\
                    transition_time_icdf_object.icdf_choose_noexp()
            except AttributeError as e:
                if "object has no attribute 'icdf_choose_noexp'" in str(e):
                    transition_time = transition_time_icdf_object
                    assert isinstance(
                        transition_time_icdf_object,
                        (float, int)), \
                        ("Entries of transition time matrix" +
                         "must either be ICDF" + " objects or numbers")
                else:
                    raise

        # Adds delay to transition time for first level symptomatic infection
        # statuses (InfectMild or InfectGP), as is done in CovidSim.
        if person.infection_status in [InfectionStatus.InfectMild,
                                       InfectionStatus.InfectGP]:
            time += self.delay
        # Assigns the time of status change using current time and transition
        # time:
        person.time_of_status_change = time + transition_time

    def __call__(self, time: float):
        """Sweeps through all people in the population, updates
        their infection status if it is time and assigns them their
        next infection status and the time of their next status change.

        Parameters
        ----------
        time : float
            Current simulation time

        """
        for cell in self._population.cells:
            for person in cell.persons:
                if person.time_of_status_change is None:
                    assert person.infection_status \
                                    in [InfectionStatus.Susceptible]
                    continue  # pragma: no cover
                while person.time_of_status_change <= time:
                    person.update_status(person.next_infection_status)
                    if person.infection_status in \
                            [InfectionStatus.InfectASympt,
                             InfectionStatus.InfectMild,
                             InfectionStatus.InfectGP]:
                        self.set_infectiousness(person)
                    self._update_next_infection_status(person)
                    self._update_time_status_change(person, time)
