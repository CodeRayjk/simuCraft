

import argparse
import logging

import Engine.simulation as sim
from model.character import Character

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')




def parse():
    parser = argparse.ArgumentParser(description="simuCraft the best wow simu ever!")
    parser.add_argument("-g", "--gui", action="store_true",
                        help="Activates GUI")
    parser.add_argument("-i", "--iterations", help="Number of iterations to run in simulation")
    parser.add_argument("-p", "--player", help="Player config")
    parser.add_argument("-e", "--enemy", help="Enemy config")

    return parser.parse_args()


def run(args):


    logging.debug('INSIDE RUN')

    gurkis = Character("Gurkis")
    rayjk = Character("Rayjk")
    simulation = sim.Simulation(20000, None, [gurkis, rayjk])
    # simulation = sim.Simulation(10000, None, [rayjk])
    # simulation = sim.Simulation(17000, None, [gurkis])
    simulation.run()

    return 0

if __name__ == '__main__':

    logging.debug('INSIDE MAIN')
    args = parse()
    run(args)
