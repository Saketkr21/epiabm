#
# Example simulation script with travelling
#

import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

import pyEpiabm as pe

# Setup output for logging file
logging.basicConfig(filename='sim.log', filemode='w+', level=logging.DEBUG,
                    format=('%(asctime)s - %(name)s'
                            + '- %(levelname)s - %(message)s'))

# Set population input file
file_loc = os.path.join(os.path.dirname(__file__), "input.csv")

# sim_params give details for the running of the simulations
sim_params = {"simulation_start_time": 0, "simulation_end_time": 50,
              "initial_infected_number": 1, "initial_infect_cell": True}

# Set parameter file
name_parameter_file = 'travelling_parameters.json'

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                       name_parameter_file))

# Parameter to change
to_modify_parameter_values = {'ratio_introduce_cases': [0.0, 0.05, 0.1],
                              'constant_introduce_cases': [[0],
                                                           [0]*4+[100]+[0]*46]}
for to_modify_parameter, parameter_values in to_modify_parameter_values.\
        items():
    # Only study one way to introduce cases
    if to_modify_parameter == 'ratio_introduce_cases':
        pe.Parameters.instance().travel_params['constant_introduce_cases'] = \
            [0]
    else:
        pe.Parameters.instance().travel_params['ratio_introduce_cases'] = 0.0
    for parameter_value in parameter_values:
        if isinstance(parameter_value, float):
            parameter_value_name = parameter_value
        else:
            parameter_value_name = sum(parameter_value)
        name_output_file = 'output_{}_{}.csv'.format(
            to_modify_parameter, parameter_value_name)

        pe.Parameters.instance().travel_params[
            to_modify_parameter] = parameter_value
        print('Set {} to: {}'.format(to_modify_parameter,
                                     pe.Parameters.instance(
                                     ).travel_params[
                                        to_modify_parameter]))

        # Method to set the seed at the start of the simulation,
        # for reproducibility
        pe.routine.Simulation.set_random_seed(seed=30)

        # Create population
        population = pe.routine.FilePopulationFactory.make_pop(
            file_loc, random_seed=42)

        # Configure population with input data
        pe.routine.ToyPopulationFactory.add_places(population, 1)

        # file_params give details for where output should be written to.
        file_params = {"output_file": name_output_file,
                       "output_dir": os.path.join(os.path.dirname(__file__),
                                                  "travelling_outputs"),
                       "spatial_output": True,
                       "age_stratified": True}

        # Create a simulation object, configure it with the parameters given,
        # then run the simulation.
        sim = pe.routine.Simulation()
        sim.configure(
            population,
            [pe.sweep.InitialInfectedSweep(), pe.sweep.InitialisePlaceSweep()],
            [
                pe.sweep.TravelSweep(),
                pe.sweep.UpdatePlaceSweep(),
                pe.sweep.HouseholdSweep(),
                pe.sweep.PlaceSweep(),
                pe.sweep.SpatialSweep(),
                pe.sweep.QueueSweep(),
                pe.sweep.HostProgressionSweep(),
            ],
            sim_params,
            file_params,
        )
        sim.run_sweeps()

        # Need to close the writer object at the end of each simulation.
        del sim.writer
        del sim

###############################
# Creation of a plot of results
logging.getLogger("matplotlib").setLevel(logging.WARNING)

for to_modify_parameter, parameter_values in to_modify_parameter_values.\
        items():
    for parameter_value in parameter_values:
        if isinstance(parameter_value, float):
            parameter_value_name = parameter_value
        else:
            parameter_value_name = sum(parameter_value)
        file_name = os.path.join(os.path.dirname(__file__),
                                 "travelling_outputs",
                                 'output_{}_{}.csv'.format(
                                    to_modify_parameter, parameter_value_name))
        df = pd.read_csv(file_name)
        total_df = \
            df[list(df.filter(regex='InfectionStatus.Infect'))]
        df["Infected"] = total_df.sum(axis=1)
        df = df.groupby(["time"]).agg(
                    {"InfectionStatus.Susceptible": 'sum',
                     "Infected": 'sum',
                     "InfectionStatus.Recovered": 'sum',
                     "InfectionStatus.Dead": 'sum'})
        df = df.reset_index(level=0)

        plt.plot(df['time'], df['Infected'], label='{}: {}'.format(
            to_modify_parameter, parameter_value_name))

    plt.legend()
    plt.title("Infection curves for different {}".format(
        to_modify_parameter))
    plt.ylabel("Infected Population")
    plt.savefig(
        os.path.join(os.path.dirname(__file__),
                     "travelling_outputs",
                     "travelling_{}_Icurve_plot.png".format(
                        to_modify_parameter))
    )
    plt.clf()
