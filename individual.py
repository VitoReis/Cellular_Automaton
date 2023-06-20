from scenary import *
from random import uniform, randint


class Individual:
    def __init__(self, specimen, position, prob_move, prob_breeding, prob_death, scenary):
        self.specimen = specimen
        self.position = position
        self.prob_move = prob_move
        self.prob_breeding = prob_breeding
        self.prob_death = prob_death
        scenary.write_scenary(self.specimen, self.position)

    def move_individual(self, scenary, empty_symbol):
        empty_spaces = scenary.search_surroundings(self.position, empty_symbol)
        will_move = uniform(0, 1)
        if will_move <= self.prob_move and len(empty_spaces) > 0:
            pos = randint(0, len(empty_spaces) - 1)
            scenary.write_scenary(empty_symbol, self.position)
            scenary.write_scenary(self.specimen, empty_spaces[pos])
            self.position = empty_spaces[pos]

    def breed(self, scenary, empty_symbol, threats_symbol, inhibition, reproduced):
        empty_spaces = scenary.search_surroundings(self.position, empty_symbol)
        partners = scenary.search_surroundings(self.position, self.specimen)
        # Inhibits reproduction of individuals more than once per cycle
        # Inhibits puppies too
        for i in reproduced:
            if i in partners:
                partners.remove(i)
        will_breed = uniform(0, 1)
        if will_breed <= self.prob_breeding and len(empty_spaces) > 0 and len(partners) > 0:
            threats = scenary.search_surroundings(self.position, threats_symbol)
            inhibited = uniform(0, 1)
            if len(threats) < 2 and inhibited > inhibition:
                pts = randint(0, len(partners) - 1)
                pos = randint(0, len(empty_spaces) - 1)
                scenary.write_scenary(self.specimen, empty_spaces[pos])
                self.position = empty_spaces[pos]
                print(f'pt1:{self.position} pt2:{partners[pts]} son:{empty_spaces[pos]}')
                reproduced.append(self.position)
                reproduced.append(partners[pts])
                reproduced.append(empty_spaces[pos])
        return reproduced
