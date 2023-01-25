#
# Example simulation script with intervention data output and visualisation
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

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                       "intervention_parameters.json"))

# Method to set the seed at the start of the simulation, for reproducibility
pe.routine.Simulation.set_random_seed(seed=30)

# Generate population from input file
file_loc = os.path.join(os.path.dirname(__file__), "input.csv")
population = pe.routine.FilePopulationFactory.make_pop(file_loc,
                                                       random_seed=42)

# Configure population with input data
pe.routine.ToyPopulationFactory.add_places(population, 1)

# sim_ and file_params give details for the running of the simulations and
# where output should be written to.
sim_params = {"simulation_start_time": 0, "simulation_end_time": 25,
              "initial_infected_number": 1, "initial_infect_cell": True}

file_params = {"output_file": "output.csv",
               "output_dir": os.path.join(os.path.dirname(__file__),
                                          "intervention_outputs"),
               "spatial_output": True}

# Create a simulation object, configure it with the parameters given, then
# run the simulation.
sim = pe.routine.Simulation()
sim.configure(
    population,
    [pe.sweep.InitialInfectedSweep(), pe.sweep.InitialisePlaceSweep()],
    [
        pe.sweep.InterventionSweep(),
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

# Creation of a plot of results
logging.getLogger("matplotlib").setLevel(logging.WARNING)
filename = os.path.join(os.path.dirname(__file__), "intervention_outputs",
                        "output.csv")
df = pd.read_csv(filename)


df = df.pivot(index="time", columns="cell",
              values="InfectionStatus.InfectMild")
df.plot()

plt.legend(labels=(range(len(df.columns))), title="Cell")
plt.title("Infection curves for multiple cells")
plt.ylabel("Infected Population")
plt.savefig(
    os.path.join(os.path.dirname(__file__),
                 "intervention_outputs", "intervention_flow_Icurve_plot.png")
)
