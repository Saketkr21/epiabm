#
# Parameters
#

import numpy as np

from pyEpiabm.utility.state_transition_matrix import StateTransitionMatrix
class Parameters:
    """Class for global parameters.

    Following a singleton Pattern.
    """
    class __Parameters:
        """Singleton Parameters Object.
        """
        def __init__(self):
            self.latent_period = 4.59
            self.asympt_infect_period = 14
            self.mean_mild_to_recov = 7
            self.mean_gp_to_recov = 7
            self.mean_gp_to_hosp = 5
            self.mean_gp_to_death = 7
            self.mean_hosp_to_recov = 1
            self.mean_hosp_to_icu = 1
            self.mean_hosp_to_death = 1
            self.mean_icu_to_icurecov = 1
            self.mean_icu_to_death = 1
            self.mean_icurecov_to_recov = 1
            self.latent_period_iCDF = np.array([0, 0.098616903, 0.171170649,
                                                0.239705594, 0.307516598,
                                                0.376194441, 0.446827262,
                                                0.520343677, 0.597665592,
                                                0.679808341, 0.767974922,
                                                0.863671993, 0.968878064,
                                                1.086313899, 1.219915022,
                                                1.37573215, 1.563841395,
                                                1.803041398, 2.135346254,
                                                2.694118208, 3.964172493])
            self.asympt_infect_icdf = np.array([0, 0.171566836, 0.424943468,
                                                0.464725594, 0.50866631,
                                                0.55773764, 0.613298069,
                                                0.67732916, 0.752886568,
                                                0.843151261, 0.895791527,
                                                0.955973422, 1.026225109,
                                                1.110607115, 1.216272375,
                                                1.336349102, 1.487791911,
                                                1.701882384, 1.865779085,
                                                2.126940581, 2.524164972])
            self.mild_to_recov_icdf = np.array([0, 0.341579599, 0.436192391,
                                                0.509774887, 0.574196702,
                                                0.633830053, 0.690927761,
                                                0.74691114, 0.802830695,
                                                0.859578883, 0.918015187,
                                                0.97906363, 1.043815683,
                                                1.113669859, 1.190557274,
                                                1.277356871, 1.378761429,
                                                1.50338422, 1.670195767,
                                                1.938414132, 2.511279379])
            self.gp_to_recov_icdf = np.array([0, 0.341579599, 0.436192391,
                                              0.509774887, 0.574196702,
                                              0.633830053, 0.690927761,
                                              0.74691114, 0.802830695,
                                              0.859578883, 0.918015187,
                                              0.97906363, 1.043815683,
                                              1.113669859, 1.190557274,
                                              1.277356871, 1.378761429,
                                              1.50338422, 1.670195767,
                                              1.938414132, 2.511279379])
            self.gp_to_hosp_icdf = np.array([0, 0.341579599, 0.436192391,
                                             0.509774887, 0.574196702,
                                             0.633830053, 0.690927761,
                                             0.74691114, 0.802830695,
                                             0.859578883, 0.918015187,
                                             0.97906363, 1.043815683,
                                             1.113669859, 1.190557274,
                                             1.277356871, 1.378761429,
                                             1.50338422, 1.670195767,
                                             1.938414132, 2.511279379])
            self.gp_to_death_icdf = np.array([0, 2.257735908, 3.171065856,
                                              3.924183798, 4.608738224,
                                              5.260437017, 5.898728066,
                                              6.53669783, 7.184755068,
                                              7.852438367, 8.549591424,
                                              9.287408763, 10.07967529,
                                              10.94457146, 11.90769274,
                                              13.00769447, 14.3081531,
                                              15.92655201, 18.12320384,
                                              21.71626849, 29.58154704])
            self.hosp_to_recov_icdf = np.array([0, 0.634736097, 1.217461548,
                                                1.805695261, 2.41206761,
                                                3.044551205, 3.71010552,
                                                4.415905623, 5.170067405,
                                                5.982314035, 6.864787504,
                                                7.833196704, 8.908589322,
                                                10.12027655, 11.51100029,
                                                13.14682956, 15.13821107,
                                                17.69183155, 21.27093904,
                                                27.35083955, 41.35442157])
            self.hosp_to_icu_icdf = np.array([0, 0.108407687, 0.220267228,
                                              0.337653773, 0.46159365,
                                              0.593106462, 0.733343356,
                                              0.88367093, 1.045760001,
                                              1.221701998, 1.414175806,
                                              1.62669998, 1.864032461,
                                              2.132837436, 2.442868902,
                                              2.809242289, 3.257272257,
                                              3.834402667, 4.647120033,
                                              6.035113821, 9.253953212])
            self.hosp_to_death_icdf = np.array([0, 1.703470233, 2.39742257,
                                                2.970367222, 3.491567676,
                                                3.988046604, 4.474541783,
                                                4.960985883, 5.455292802,
                                                5.964726999, 6.496796075,
                                                7.06004732, 7.665014091,
                                                8.325595834, 9.061367792,
                                                9.901900127, 10.8958347,
                                                12.133068, 13.81280888,
                                                16.56124574, 22.5803431])
            self.icu_to_icurecov_icdf = np.array([0, 1.308310071, 1.87022015,
                                                  2.338694632, 2.76749788,
                                                  3.177830401, 3.581381361,
                                                  3.986127838, 4.398512135,
                                                  4.824525291, 5.270427517,
                                                  5.743406075, 6.252370864,
                                                  6.809125902, 7.430338867,
                                                  8.141231404, 8.983341913,
                                                  10.03350866, 11.46214198,
                                                  13.80540164, 18.95469153])
            self.icu_to_death_icdf = np.array([0, 1.60649128, 2.291051747,
                                               2.860938008, 3.382077741,
                                               3.880425012, 4.37026577,
                                               4.861330415, 5.361460943,
                                               5.877935626, 6.4183471,
                                               6.991401405, 7.607881726,
                                               8.282065409, 9.034104744,
                                               9.894486491, 10.91341144,
                                               12.18372915, 13.9113346,
                                               16.74394356, 22.96541429])
            self.icurecov_to_recov = np.array([0, 0.133993315, 0.265922775,
                                               0.402188416, 0.544657341,
                                               0.694774487, 0.853984373,
                                               1.023901078, 1.206436504,
                                               1.403942719, 1.619402771,
                                               1.856711876, 2.121118605,
                                               2.419957988, 2.763950408,
                                               3.169692564, 3.664959893,
                                               4.301777536, 5.196849239,
                                               6.7222126, 10.24997697])
            self.CDF_RES = 20
            self.time_steps_per_day = 1
            self.prob_symptomatic = 0.66
            self.sympt_infectiousness = 1.5
            self.asympt_infectiousness = 1
            self.latent_to_sympt_delay = 0.5
            self.prob_gp = 0.3786953814  # From average of by age prop
            self.prob_gp_to_hosp = 0.1628884247  # From average of by age prop
            self.prob_hosp_to_icu = 0.3969284544  # From average of by age prop
            self.mortality_prob_gp = 0  # From average of by age prop
            self.mortality_prob_hosp = 0.2676376  # From average of by age prop
            self.mortality_prob_icu = 0.5234896  # From average of by age 
            
            #Build infection state transition matrix
            matrix_object = StateTransitionMatrix()
            empty_matrix = matrix_object.build_state_transition_matrix()
            self.state_transition_matrix = matrix_object.fill_state_transition_matrix(empty_matrix)
            pass

    _instance = None  # Singleton instance

    @staticmethod
    def instance():
        """Creates singleton instance of __Parameters under
        _instance if one doesn't already exist.

        :return: An instance of the __Parameters class
        :rtype: __Parameters
        """
        if not Parameters._instance:
            Parameters._instance = Parameters.__Parameters()
        return Parameters._instance
