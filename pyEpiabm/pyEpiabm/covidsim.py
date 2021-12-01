from .person import Person

class Covidsim:
    @staticmethod
    def calc_house_inf(infector: Person, timestep: int):
        """Calculate the infectiveness of a household

        :param infector: Infector.
        :type infector: Person
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: infectiveness
        :rtype: float
        """
        return 1

    @staticmethod
    def calc_house_susc(infector: Person, infectee: Person, timestep: int):
        """Calculate the susceptibility of a household
        
        :param infector: Infector.
        :type infector: Person
        :param infectee: Infectee.
        :type infectee: Person
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: susceptibility
        :rtype: float
        """
        return Covidsim.calc_person_susc(infector, infectee, timestep)
        
    @staticmethod
    def calc_person_susc(infector:Person, infectee: Person, timestep: int):
        """Calculate the susceptibility of a person
        
        :param infector: Infector.
        :type infector: Person
        :param infectee: Infectee.
        :type infectee: Person
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: susceptibility
        :rtype: float
        """
        return 1
