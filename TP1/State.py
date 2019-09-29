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
        self.num_blockedCars = []

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

    def find_car_on(self, x, y, rh):
        for car in range(rh.nbcars):
            if not rh.horiz[car]:
                if rh.move_on[car] == y:
                    if x <= self.pos[car] + rh.length[car] - 1 and x >= self.pos[car]:
                        return car if car != 0 else 99
            else:
                if rh.move_on[car] == x:
                    if y <= self.pos[car] + rh.length[car] - 1 and y >= self.pos[car]:
                        return car if car != 0 else 99
        return 0

    def print_game(self, rh):
        game = np.zeros((6, 6))
        for x in range(6):
            for y in range(6):
                game[x][y] = self.find_car_on(x, y, rh)
        return game



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
        for car in self.num_blockedCars:
            if rh.horiz[car] == 0:
                if self.find_car_on(self.pos[car] - 1, rh.move_on[car], rh) !=0 and \
                        self.find_car_on(self.pos[car] + rh.length[car], rh.move_on[car], rh) != 0:
                    blocked_cars += 1

            else:
                if self.find_car_on(rh.move_on[car], self.pos[car] - 1, rh) != 0 and \
                        self.find_car_on(rh.move_on[car], self.pos[car] + rh.length[car], rh) != 0:
                    blocked_cars += 1

        return blocked_cars + blockingCars + 4 - self.pos[0]

    def estimee4(self, rh):

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
        self.num_blockedCars = self.num_blockingCars
        while len(self.num_blockedCars) > 0:
            for index_car, car in enumerate(self.num_blockedCars):
                if rh.horiz[car] == 0:
                    # on regarde si la voiture est bloquée a gauche et a droite,
                    # tout en faisant attention de ne pas sortir des limites de la matrice
                    if self.find_car_on(self.pos[car] - 1, rh.move_on[car], rh) != 0 and \
                            self.find_car_on(self.pos[car] + rh.length[car], rh.move_on[car], rh) != 0:
                        # si elle est bien bloquée des 2 cotées:
                        # on ajoute 1 au nombre de voiture bloqué,
                        blocked_cars += 1

                        # on check maintenant de quelle coté la voiture est bloquée,
                        # et on ajoute la voiture qui s'y trouve a la liste des voitures a traiter
                        if self.find_car_on(self.pos[car] - 1, rh.move_on[car], rh) != 0 and self.pos[car] - 1 >= 0:
                            self.num_blockedCars.append(self.find_car_on(self.pos[car] - 1, rh.move_on[car], rh))

                        elif self.find_car_on(self.pos[car] + rh.length[car], rh.move_on[car], rh) != 0 and \
                                self.pos[car] + rh.length[car] <= 5:
                            self.num_blockedCars.append(self.find_car_on(self.pos[car] + rh.length[car], rh.move_on[car], rh))

                else:
                    # de même, mais cette foit ci dans l'autre sens
                    if self.find_car_on(rh.move_on[car], self.pos[car] - 1, rh) != 0 and \
                            self.find_car_on(rh.move_on[car], self.pos[car] + rh.length[car], rh) != 0:
                        blocked_cars += 1

                        if self.find_car_on(rh.move_on[car], self.pos[car] - 1, rh) != 0 and self.pos[car] - 1 >= 0:
                            self.num_blockedCars.append(self.find_car_on(rh.move_on[car], self.pos[car] - 1, rh))

                        elif self.find_car_on(rh.move_on[car], self.pos[car] + rh.length[car], rh) != 0 and\
                                self.pos[car] + rh.length[car] <= 5:
                            self.num_blockedCars.append(self.find_car_on(rh.move_on[car], self.pos[car] + rh.length[car], rh))

                # on a traité la voiture, on la supprime de la liste de voitures a traiter
                del self.num_blockedCars[index_car]

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
