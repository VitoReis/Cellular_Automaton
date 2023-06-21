from random import uniform, randint


class Individual:
    def __init__(self, specimen, position, prob_move, prob_breeding, prob_inhibition, prob_killed, prob_death, scenery):
        self.specimen = specimen
        self.position = position
        self.prob_move = prob_move
        self.prob_breeding = prob_breeding
        self.prob_inhibition = prob_inhibition
        self.prob_killed = prob_killed
        self.prob_death = prob_death
        scenery.write_scenery(self.specimen, self.position)

    def move_individual(self, scenery, empty_symbol):
        empty_spaces = scenery.search_surroundings(self.position, empty_symbol)
        will_move = uniform(0, 1)
        if will_move <= self.prob_move and len(empty_spaces) > 0:
            pos = randint(0, len(empty_spaces) - 1)
            # print(f'MOVED: from {self.position} to {empty_spaces[pos]}')
            scenery.write_scenery(empty_symbol, self.position)
            scenery.write_scenery(self.specimen, empty_spaces[pos])
            self.position = empty_spaces[pos]

    def breed(self, scenery, empty_symbol, threats_symbol, population, reproduced):
        empty_spaces = scenery.search_surroundings(self.position, empty_symbol)
        partners = scenery.search_surroundings(self.position, self.specimen)
        # Inhibits reproduction of individuals more than once per cycle
        # Inhibits puppies too
        for i in reproduced:
            if i in partners:
                partners.remove(i)
        if self.position in partners:
            partners.remove(self.position)
        will_breed = uniform(0, 1)
        if will_breed <= self.prob_breeding and len(empty_spaces) > 0 and len(partners) > 0:
            threats = scenery.search_surroundings(self.position, threats_symbol)
            inhibited = uniform(0, 1)
            if len(threats) < 2 and inhibited > self.prob_inhibition:
                pts = randint(0, len(partners) - 1)
                pos = randint(0, len(empty_spaces) - 1)
                scenery.write_scenery(self.specimen, empty_spaces[pos])
                population.append(Individual(self.specimen, empty_spaces[pos], self.prob_move, self.prob_breeding, self.prob_inhibition, self.prob_killed,self.prob_death, scenery))
                # print(f'REPRODUCED: PT1 {self.position} PT2 {partners[pts]} SON {empty_spaces[pos]}')
                reproduced.append(self.position)
                reproduced.append(partners[pts])
                reproduced.append(empty_spaces[pos])
        return population, reproduced
    
    def was_killed(self, scenery, threats_symbol, empty_symbol):
        threats = scenery.search_surroundings(self.position, threats_symbol)
        kill = uniform(0, 1)
        if len(threats) >= 3 and kill <= self.prob_killed:
            # print(f'KILLED: {self.position}')
            scenery.write_scenery(empty_symbol, self.position)
            return True
        return False

