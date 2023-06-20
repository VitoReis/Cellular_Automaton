from individual import *
from scenary import *
import numpy as np
from random import randint, uniform

# Populations
population1 = {}                # Dictionary of each individual in population 1
population2 = {}                # Dictionary of each individual in population 2
initial_population = [10, 10]   # Initial population of each individual
prob_move = [0.5, 0.5]          # Probability to moving
prob_death = [0.1, 0.1]         # Probability of dying of natural causes
prob_breeding = [0.5, 0.5]      # Reproduction probability
prob_inhibition = [0.2, 0.2]    # Probability of not reproducing because there are threats around

# Scenary
size_line = 5
size_col = 5
symbols = ['0', '1', '2']       # Symbols for each space in the scenario

# Time
t = 100                         # Time steps


def print_scenary(scenary):
    for i in range(0, size_line):
        print(f'{i}\t|', end='')
        for j in range(0, size_col):
            print(scenary.map[i][j], end='')
        print('|')
    print('\n')


def move_populations(scenary):
    for i in range(len(population1)):
        population1[f'ind{i}'].move_individual(scenary, symbols[0])
    for j in range(len(population2)):
        population2[f'ind{j}'].move_individual(scenary, symbols[0])


def create_scenary():
    scenary = Scenary(size_line, size_col, symbols[0])
    empty_spaces = [(i, j) for i in range(len(scenary.map)) for j in range(len(scenary.map[i]))]
    # Create the initial populations
    for k in range(0, initial_population[0]):
        position = randint(0, len(empty_spaces)-1)
        population1[f'ind{k}'] = Individual(symbols[1], empty_spaces[position], prob_move[0], prob_breeding[0],
                                            prob_death[0], scenary)
        empty_spaces.remove(empty_spaces[position])

    for l in range(0, initial_population[0]):
        position = randint(0, len(empty_spaces)-1)
        population2[f'ind{l}'] = Individual(symbols[2], empty_spaces[position], prob_move[1], prob_breeding[1],
                                            prob_death[1], scenary)
        empty_spaces.remove(empty_spaces[position])
    return scenary


def reproducing_populations(scenary):
    reproduced = []
    for i in range(len(population1)):
        reproduced = population1[f'ind{i}'].breed(scenary, symbols[0], symbols[2], prob_inhibition[0], reproduced)
    reproduced = []
    for j in range(len(population2)):
        reproduced = population2[f'ind{j}'].breed(scenary, symbols[0], symbols[1], prob_inhibition[1], reproduced)


def main():
    scenary = create_scenary()
    print_scenary(scenary)
    # for i in range(t):
    move_populations(scenary)
    print_scenary(scenary)
    reproducing_populations(scenary)
    print_scenary(scenary)



    # plotScenary(scenary, pdf, 0)
    # for i in range(0, t):
    #     scenary = moving(scenary)
    #     scenary = killings(scenary)
    #     scenary = reproduction(scenary)
    #     scenary = death(scenary)
    #     pop1, pop2 = popCalc(scenary, pop1, pop2)
    #     plotScenary(scenary, pdf, i + 1)
    # plotPop(scenary, time, pop1, pop2)
    # pdf.close()


if __name__ == '__main__':
    main()
