#
# Calculate household force of infection based on Covidsim code
#

from pyEpiabm.core import Parameters
import pyEpiabm.core

from .personal_foi import PersonalInfection


class HouseholdInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, within households.

    """
    @staticmethod
    def household_inf(infector, time: float):
        """Calculate the infectiousness of a person in a given
        household. Does not include interventions such as isolation,
        or whether individual is a carehome resident.

        Parameters
        ----------
        infector : Person
            Infector
        time : float
            Current simulation time

        Returns
        -------
        float
            Infectiousness parameter of household

        """
        household_infectiousness = PersonalInfection.person_inf(
            infector, time)
        if ('place_closure' in Parameters.instance().intervention_params.keys()
            ) and (infector.close_place(Parameters.instance().
                   intervention_params['place_closure'][
                    'closure_place_type'])):
            household_infectiousness *= Parameters.instance().\
                intervention_params['place_closure'][
                'closure_household_infectiousness']
        return household_infectiousness

    @staticmethod
    def household_susc(infector, infectee, time: float):
        """Calculate the susceptibility of one person to another in a given
        household. Does not include interventions such as isolation,
        or whether individual is a carehome resident.

        Parameters
        ----------
        infector : Person
            Infector
        infectee : Person
            Infectee
        time : float
            Current simulation time

        Returns
        -------
        float
            Susceptibility parameter of household

        """
        household_susceptibility = PersonalInfection.person_susc(
            infector, infectee, time)
        if (hasattr(infector.microcell, 'distancing_start_time')) and (
                infector.microcell.distancing_start_time is not None):
            if infector.distancing_enhanced is True:
                household_susceptibility *= Parameters.instance().\
                    intervention_params['social_distancing'][
                        'distancing_house_enhanced_susc']
            else:
                household_susceptibility *= Parameters.instance().\
                    intervention_params['social_distancing'][
                        'distancing_house_susc']
        return household_susceptibility

    @staticmethod
    def household_foi(infector, infectee, time: float):
        """Calculate the force of infection parameter of a household,
        for a particular infector and infectee.

        Parameters
        ----------
        infector : Person
            Infector
        infectee : Person
            Infectee
        time : float
            Current simulation time

        Returns
        -------
        float
            Force of infection parameter of household

        """
        seasonality = 1.0  # Not yet implemented
        isolating = Parameters.instance().\
            intervention_params['case_isolation']['isolation_house'
                                                  '_effectiveness'] \
            if (hasattr(infector, 'isolation_start_time')) and (
                infector.isolation_start_time is not None) else 1
        quarantine = Parameters.instance().\
            intervention_params['household_quarantine']['quarantine_house'
                                                        '_effectiveness'] \
            if (hasattr(infector, 'quarantine_start_time')) and (
                infector.quarantine_start_time is not None) else 1
        false_pos = 1 / (1 - pyEpiabm.core.Parameters.instance().
                         false_positive_rate)
        infectiousness = (HouseholdInfection.household_inf(infector, time)
                          * seasonality * false_pos
                          * pyEpiabm.core.Parameters.instance().
                          household_transmission
                          * isolating * quarantine)
        susceptibility = HouseholdInfection.household_susc(infector, infectee,
                                                           time)
        return (infectiousness * susceptibility)
