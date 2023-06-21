from individual import *
from scenery import *
from random import randint, uniform, choice             # Used to set odds
import matplotlib.pyplot as plt                         # Used to plot results
from matplotlib.backends.backend_pdf import PdfPages    # Used to create the PDF scenario
from matplotlib.patches import Patch                    # Used to set the subtitle color
from PIL import Image           # Used to plot the scenery
from numpy import array, uint8         # Used for the color array

# Populations
population1 = []                # List of each individual in population 1
population2 = []                # List of each individual in population 2
population_one_size = []        # List of population one sizes through cycles
population_two_size = []        # List of population two sizes through cycles

# Parameters
initial_population = [100, 100]   # Initial population of each individual
prob_move = [0.5, 0.5]          # Probability to moving
prob_breeding = [0.5, 0.5]      # Reproduction probability
prob_killed = [0.2, 0.2]        # Probability to be killed by other species
prob_death = [0.05, 0.05]       # Probability of dying of natural causes
prob_inhibition = [0.2, 0.2]    # Probability of not reproducing because there are threats around

# Scenery
scenery = None
size_line = 40
size_col = 40
symbols = [0, 1, 2]         # Symbols for each space in the scenario

# Time
t = 100         # Time steps


def create_scenery():
    global scenery, population1, population2, symbols, prob_move, prob_breeding, prob_inhibition, prob_killed, prob_death
    scenery = Scenery(size_line, size_col, symbols[0])
    empty_spaces = [(i, j) for i in range(len(scenery.map)) for j in range(len(scenery.map[i]))]
    # Create the initial populations
    for k in range(0, initial_population[0]):
        position = randint(0, len(empty_spaces)-1)
        population1.append(Individual(symbols[1], empty_spaces[position], prob_move[0], prob_breeding[0], prob_inhibition[0], prob_killed[0], prob_death[0], scenery))
        empty_spaces.remove(empty_spaces[position])

    for l in range(0, initial_population[0]):
        position = randint(0, len(empty_spaces)-1)
        population2.append(Individual(symbols[2], empty_spaces[position], prob_move[1], prob_breeding[1], prob_inhibition[1], prob_killed[1], prob_death[1], scenery))
        empty_spaces.remove(empty_spaces[position])


def move_populations(population):
    global scenery, symbols
    for i in range(len(population)):
        population[i].move_individual(scenery, symbols[0])
    return population


def reproducing_populations(population):
    global scenery, symbols, prob_inhibition
    reproduced = []
    for i in range(len(population)):
        population, reproduced = population[i].breed(scenery, symbols[0], symbols[1] if symbols[1] != population[i].specimen else symbols[2], population, reproduced)
    return population


def killings(population):
    global scenery, symbols
    for i in range(len(population)):
        if population[i].was_killed(scenery, symbols[1] if symbols[1] != population[i].specimen else symbols[2], symbols[0]):
            population[i] = None
    population = [ind for ind in population if ind is not None]
    return population


def populations_deaths(population):
    global scenery, prob_death
    for i in range(len(population)):
        died = uniform(0, 1)
        if died <= population[i].prob_death:
            scenery.write_scenery(symbols[0], population[i].position)
            # print(f'DIED: {population[i].position}')
            population[i] = None
    population = [ind for ind in population if ind is not None]
    return population


def plot_populations():
    global population_one_size, population_two_size
    time = range(t)
    plt.title('Populations')
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.plot(time, population_one_size, label=f'{symbols[1]}')
    plt.plot(time, population_two_size, label=f'{symbols[2]}')
    plt.legend()
    plt.savefig('Population_Graph.pdf')
    plt.clf()


def plot_scenarios(pdf, time):
    global scenery, symbols
    fig, ax = plt.subplots()
    fig.suptitle(f'Scenary {time}')
    # Defining the colors
    colors = array([[255, 255, 255], [255, 0, 0], [0, 255, 0]], dtype=uint8)
    # Creating an image from the matrix
    image = Image.fromarray(colors[scenery.map.astype(int)])
    # Ploting the image
    ax.imshow(image)
    # Setting legend
    legend_patches = [Patch(facecolor=colors[i] / 255, label=i) for i in range(len(symbols))]
    ax.legend(handles=legend_patches)
    # Removing size marks
    ax.set_xticks([])
    ax.set_yticks([])
    # Saving figure
    pdf.savefig(fig)
    plt.close()


def main():
    global population1, population2, population_one_size, population_two_size, scenery
    create_scenery()
    pdf = PdfPages('Scenerys.pdf')
    plot_scenarios(pdf, 0)
    for i in range(t):
        # print(f'CYCLE {i}')
        # Randomly chooses a population to be checked first
        chosen_population = choice([population1, population2])
        if chosen_population is population1:
            population1 = move_populations(population1)
            population2 = move_populations(population2)
            population1 = reproducing_populations(population1)
            population2 = reproducing_populations(population2)
            population1 = killings(population1)
            population2 = killings(population2)
            population1 = populations_deaths(population1)
            population2 = populations_deaths(population2)
            population_one_size.append(len(population1))
            population_two_size.append(len(population2))
        else:
            population2 = move_populations(population2)
            population1 = move_populations(population1)
            population2 = reproducing_populations(population2)
            population1 = reproducing_populations(population1)
            population2 = killings(population2)
            population1 = killings(population1)
            population2 = populations_deaths(population2)
            population1 = populations_deaths(population1)
            population_one_size.append(len(population1))
            population_two_size.append(len(population2))
        plot_scenarios(pdf, i+1)
    plot_populations()
    pdf.close()


if __name__ == '__main__':
    main()
