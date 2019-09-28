from RushHour import Rushhour
from State import State

def solve46():
    rh = Rushhour([True, False, True, False, False, True, False, True, False, True, False, True],
                 [2, 2, 3, 2, 3, 2, 2, 2, 2, 2, 2, 3],
                 [2, 2, 0, 0, 3, 1, 1, 3, 0, 4, 5, 5],
                 ["rouge", "vert clair", "jaune", "orange", "violet clair", "bleu ciel", "rose", "violet", "vert", "noir", "beige", "bleu"])
    s = State([1, 0, 3, 1, 1, 4, 3, 4, 4, 2, 4, 1])
    #s = rh.solve(s)
    s = rh.solve_Astar(s)
    #rh.print_solution(s)
solve46()
print("\n--------------------------------------------\n")


def solve16():
    rh = Rushhour([True, True, False, False, True, True, False, False],
                  [2, 2, 3, 2, 3, 2, 3, 3],
                  [2, 0, 0, 0, 5, 4, 5, 3],
                  ["rouge", "vert clair", "violet", "orange", "vert", "bleu ciel", "jaune", "bleu"])
    s = State([1, 0, 1, 4, 2, 4, 0, 1])
    # s = rh.solve(s)
    s = rh.solve_Astar(s)
    # n = rh.print_solution(s)


def solve81():
    rh = Rushhour([True, False, True, False, False, False, False, True, False, False, True, True, True],
                  [2, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2],
                  [2, 0, 0, 4, 1, 2, 5, 3, 3, 2, 4, 5, 5],
                  ["rouge", "jaune", "vert clair", "orange", "bleu clair", "rose", "violet clair", "bleu", "violet",
                   "vert", "noir", "beige", "jaune clair"])
    s = State([3, 0, 1, 0, 1, 1, 1, 0, 3, 4, 4, 0, 3])
    # s = rh.solve(s)
    s = rh.solve_Astar(s)
    # n = rh.print_solution(s)


solve16()
print("\n--------------------------------------------\n")
solve81()
print("\n--------------------------------------------\n")