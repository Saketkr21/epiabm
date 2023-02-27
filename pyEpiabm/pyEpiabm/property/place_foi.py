#
# Calculate place force of infection based on Covidsim code
#

from pyEpiabm.core import Parameters

from .personal_foi import PersonalInfection


class PlaceInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, within places.
    """

    @staticmethod
    def place_inf(place, infector, time: float):
        """Calculate the infectiousness of a place. Does not include
        interventions such as isolation, or whether individual is a
        carehome resident.

        Does not yet differentiate between places as we have not decided which
        places to implement, and what transmission to give them.

        Parameters
        ----------
        place : Place
            Place
        infector : Person
            Infectious person
        time : float
            Current simulation time

        Returns
        -------
        float
            Infectiousness parameter of place

        """
        params = Parameters.instance().place_params
        transmission = params["place_transmission"]
        place_idx = place.place_type.value - 1
        try:
            num_groups = params["mean_group_size"][place_idx]
        except IndexError:  # For place types not in parameters
            num_groups = 1
        # Use group-wise capacity not max_capacity once implemented
        place_inf = 0 if infector.microcell. \
            closure_start_time is not None else \
            (transmission / num_groups
                * PersonalInfection.person_inf(infector, time))
        return place_inf

    @staticmethod
    def place_susc(place, infector, infectee,
                   time: float):
        """Calculate the susceptibility of a place.
        Does not include interventions such as isolation,
        or whether individual is a carehome resident.

        Parameters
        ----------
        infector : Person
            Infector
        infectee : Person
            Infectee
        place : Place
            Place
        time : float
            Current simulation time

        Returns
        -------
        float
            Susceptibility parameter of place

        """
        place_susc = 1.0
        place_idx = place.place_type.value - 1
        if infector.microcell.distancing_start_time is not None:
            if infector.distancing_enhanced is True:
                distancing = Parameters.instance().\
                             intervention_params[
                             'social_distancing'][
                             'distancing_place_enhanced_susc'][place_idx]
            else:
                distancing = Parameters.instance().\
                             intervention_params[
                             'social_distancing'][
                             'distancing_place_susc'][place_idx]
        else:
            distancing = 1
        return place_susc * distancing

    @staticmethod
    def place_foi(place, infector, infectee,
                  time: float):
        """Calculate the force of infection of a place, for a particular
        infector and infectee.

        Parameters
        ----------
        infector : Person
            Infector
        infectee : Person
            Infectee
        place : Place
            Place
        time : float
            Current simulation time

        Returns
        -------
        float
            Force of infection parameter of place

        """
        isolating = Parameters.instance().\
            intervention_params['case_isolation']['isolation_effectiveness']\
            if infector.isolation_start_time is not None else 1
        place_idx = place.place_type.value - 1
        quarantine = Parameters.instance().\
            intervention_params['household_quarantine'][
                'quarantine_place_effectiveness'][place_idx]\
            if infector.quarantine_start_time is not None else 1
        infectiousness = (PlaceInfection.place_inf(place, infector, time)
                          * isolating * quarantine)
        susceptibility = (PlaceInfection.place_susc(place, infector, infectee,
                          time) * quarantine)
        return (infectiousness * susceptibility)
