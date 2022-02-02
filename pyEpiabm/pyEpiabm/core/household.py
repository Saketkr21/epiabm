#
# Household Class
#

import typing


class Household:
    """Class representing a household,
    a group of people (family or otherwise) who live
    together and share living spaces. This group will
    have a combined susceptability and infectiousness
    different to that of the individuals.
    """
    def __init__(self, loc: typing.Tuple[float, float] = (1.0, 1.0),
                 susceptibility=0, infectiousness=0):
        """Constructor Method.

        :param loc: Location of household
        :type loc: Tuple[float, float]
        :param susceptibility: Household's base susceptibility
            to infection events
        :type susceptibility: float
        :param infectiousness: Household's base infectiousness
        :type infectiousness: float
        """
        self.persons = []
        self.location = loc
        self.susceptibility = susceptibility
        self.infectiousness = infectiousness

    def __repr__(self):
        """Returns a string representation of Household.

        :return: String representation of the household
        :rtype: str
        """
        return "Household at " \
            + f"({self.location[0]:.2f}, {self.location[1]:.2f}) "\
            + f"with {len(self.persons)} people."

    def add_person(self, person):
        """Adds a person to this household.

        :param person: Person to be added
        :type person: Person
        """
        self.persons.append(person)
        person.household = self