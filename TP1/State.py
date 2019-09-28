import numpy as np


class State:
    """
    Contructeur d'un état initial
    """

    def __init__(self, pos):
        """
        pos donne la position de la voiture i (première case occupée par la voiture);
        """
        self.pos = np.array(pos)

        """
        c, d et prev premettent de retracer l'état précédent et le dernier mouvement effectué
        """
        self.c = self.d = self.prev = None

        self.nb_moves = 0
        self.h = 0
        self.num_blockingCars = []

    """
    Constructeur d'un état à partir mouvement (c,d)
    """

    def move(self, c, d):
        newS = State(self.pos)
        newS.pos[c] = newS.pos[c] + d
        newS.c = c
        newS.d = d
        newS.prev = self
        newS.nb_moves = self.nb_moves + 1
        return newS

    """ est il final? """

    def success(self):
        """
        on ne peut déplacer à chaque coup une voiture que d'une case :
        donc l'état ne peut être final que si la voiture rouge est juste devant la porte de sorie
        """
        if self.pos[0] == 4:
            return True
        else:
            return False

    """
    Estimation du nombre de coup restants 
    """

    def estimee1(self):
        """
        estimee1 renvoie la distance entre la position actuelle de la voiture rouge
        et l'état succès
        """
        return 4 - self.pos[0]

    def estimee2(self, rh):
        blockingCars = 0
        for car in range(rh.nbcars):
            if rh.horiz[car] == 0:
                if rh.move_on[car] > self.pos[0] + 1:
                    if self.pos[car] <= 2:
                        if rh.length[car] == 3:
                            blockingCars += 1
                            self.num_blockingCars.append(car)
                        elif self.pos[car] >= 1:
                            blockingCars += 1
                            self.num_blockingCars.append(car)
        return blockingCars + 4 - self.pos[0]

    def estimee3(self, rh):

        # nous allons regarder si les voitures qui bloquent sont elles aussi bloquées.
        # Si elle le sont, on ajoute 1 ou 2 à la valeur de l'heuristique
        blockingCars = 0
        for car in range(rh.nbcars):
            if rh.horiz[car] == 0:
                if rh.move_on[car] > self.pos[0] + 1:
                    if self.pos[car] <= 2:
                        if rh.length[car] == 3:
                            blockingCars += 1
                            self.num_blockingCars.append(car)
                        elif self.pos[car] >= 1:
                            blockingCars += 1
                            self.num_blockingCars.append(car)
        blocked_cars = 0
        for car in self.num_blockingCars:
            if rh.horiz[car] == 0:
                # print("\n\ndevant la voiture: ")
                # print("position_x = " + str(self.pos[car] - 1))
                # print("position_y = " + str(rh.move_on[car]))
                # print("value = " + str(rh.free_pos[self.pos[car] - 1][rh.move_on[car]]))
                #
                # print("\nderrier la voiture:")
                # print("position_x = " + str(self.pos[car] + rh.length[car]))
                # print("position_y = " + str(rh.move_on[car]))
                #
                # print("value = " + str(rh.free_pos[self.pos[car] + rh.length[car]][rh.move_on[car]]))

                if not rh.free_pos[self.pos[car] - 1][rh.move_on[car]]:
                    blocked_cars += 4
                elif not rh.free_pos[self.pos[car] + rh.length[car]][rh.move_on[car]]:
                    blocked_cars += 4
            else:
                if not rh.free_pos[rh.move_on[car]][self.pos[car] - 1]:
                    blocked_cars += 4
                elif not rh.free_pos[rh.move_on[car]][self.pos[car] + rh.length[car]]:
                    blocked_cars += 4

        return blocked_cars + blockingCars + 4 - self.pos[0]


    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        if len(self.pos) != len(other.pos):
            print("les états n'ont pas le même nombre de voitures")

        return np.array_equal(self.pos, other.pos)

    def __hash__(self):
        h = 0
        for i in range(len(self.pos)):
            h = 37 * h + self.pos[i]
        return int(h)

    def __lt__(self, other):
        return (self.nb_moves + self.h) < (other.nb_moves + other.h)
