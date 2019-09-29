import numpy as np
from collections import deque
import heapq
import math


class Rushhour:

    def __init__(self, horiz, length, move_on, color=None):
        self.nbcars = len(horiz)
        self.horiz = horiz
        self.length = length
        self.move_on = move_on
        self.color = color

        self.free_pos = None

    def init_positions(self, state):
        self.free_pos = np.ones((6, 6), dtype=bool)
        for car in range(self.nbcars):
            if self.horiz[car]:
                carPos = (self.move_on[car], state.pos[car])
                for length_idx in range(self.length[car]):
                    self.free_pos[carPos[0], carPos[1] + length_idx] = False
            else:
                carPos = (state.pos[car], self.move_on[car])
                for length_idx in range(self.length[car]):
                    self.free_pos[carPos[0] + length_idx, carPos[1]] = False

    def possible_moves(self, state):
        self.init_positions(state)
        new_states = []
        for car in range(self.nbcars):
            if self.horiz[car]:
                if state.pos[car] != 0:
                    if self.free_pos[self.move_on[car], state.pos[car] - 1] == True:
                        new_states.append(state.move(car, -1))
                if state.pos[car] + self.length[car] <= 5:
                    if self.free_pos[self.move_on[car], state.pos[car] + self.length[car]] == True:
                        new_states.append(state.move(car, 1))
            else:
                if state.pos[car] != 0:
                    if self.free_pos[state.pos[car] - 1, self.move_on[car]] == True:
                        new_states.append(state.move(car, -1))
                if state.pos[car] + self.length[car] <= 5:
                    if self.free_pos[state.pos[car] + self.length[car], self.move_on[car]] == True:
                        new_states.append(state.move(car, 1))
        return new_states

    def solve(self, state):
        visited = set()
        fifo = deque([state])
        visited.add(state)

        # Tant que la queue n'est pas vide
        while fifo:
            currentLeaf = fifo.pop()
            if hash(currentLeaf) not in visited:
                if currentLeaf.success():
                    print('Noeuds visités: ' + str(len(visited)))
                    return currentLeaf
                fifo.extendleft(self.possible_moves(currentLeaf))
                visited.add(hash(currentLeaf))
        return None

    def solve_Astar(self, state):
        visited = set()
        visited.add(state)

        priority_queue = []
        # state.h = state.estimee1()
        # state.h = state.estimee2(self)
        # state.h = state.estimee3(self)
        state.h = state.estimee4(self)

        heapq.heappush(priority_queue, state)

        # Tant que la queue n'est pas vide
        while priority_queue:
            currentLeaf = heapq.heappop(priority_queue)
            if hash(currentLeaf) not in visited:
                if currentLeaf.success():
                    print('Noeuds visités: ' + str(len(visited)))
                    return currentLeaf
                for child in self.possible_moves(currentLeaf):
                    # child.h = child.estimee1()
                    # child.h = child.estimee2(self)
                    # child.h = child.estimee3(self)
                    child.h = child.estimee4(self)
                    heapq.heappush(priority_queue, child)
                visited.add(hash(currentLeaf))

        return None

    def print_solution(self, state):
        s = []
        while state.prev != None:
            if self.horiz:
                if state.d == 1:
                    direction = "la droite"
                else:
                    direction = "la gauche"
            else:
                if state.d == 1:
                    direction = "le bas"
                else:
                    direction = "le haut"

            s.append("Voiture " + self.color[state.c] + " vers " + direction + "\n")
            s.append("voitures bloquant encore la voie: " + str(state.num_blockingCars))
            s.append("\n" + str(state.print_game(self)))

            state = state.prev

        n = 1
        while s:
            print(str(math.ceil(n/3)) + ". " + s.pop())
            n += 1
        return None