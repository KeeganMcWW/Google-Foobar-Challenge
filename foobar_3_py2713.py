import heapq
def solution(xs):
    # The following is taken from on online source on A* Pathfinding, cited below
    # note the code has been modified to run in python 2.7 and unused parts of the original source code have been removed for readability
    # ---------------------------------------------------------------
    # Sample code from https://www.redblobgames.com/pathfinding/a-star/
    # Copyright 2014 Red Blob Games <redblobgames@gmail.com>
    #
    # Feel free to use this code in your own projects, including commercial projects
    # License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>

    # some of these types are deprecated: https://www.python.org/dev/peps/pep-0585/

    T = None
    Location = None

    class Graph():
        def neighbors(self, Location):
            list[Location]

    # utility functions for dealing with square grids
    def from_id_width(id, width):
        return (id % width, id // width)

    GridLocation = []

    class SquareGrid():
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.walls = []

        def in_bounds(self, id):
            (x, y) = id
            return bool(0 <= x < self.width and 0 <= y < self.height)

        def passable(self, id):
            return bool(id not in self.walls)

        def neighbors(self, id):
            (x, y) = id
            neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
            # see "Ugly paths" section for an explanation:
            if (x + y) % 2 == 0: neighbors.reverse()  # S N W E
            results = filter(self.in_bounds, neighbors)
            results = filter(self.passable, results)
            return results

    class WeightedGraph(Graph):
        def cost(self, from_id, to_id): pass

    class GridWithWeights(SquareGrid):
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.weights = {}

        def self(self, width, height, weights):
            super(self.__init__(width, height))

        def cost(self, from_node, to_node):
            return self.weights.get(to_node, 1)

    class PriorityQueue:
        def __init__(self):
            self.elements = []

        def empty(self):
            return bool(not self.elements)

        def put(self, item, priority):
            heapq.heappush(self.elements, (priority, item))

        def get(self):
            return heapq.heappop(self.elements)[1]

    # thanks to @m1sp <Jaiden Mispy> for this simpler version of
    # reconstruct_path that doesn't have duplicate entries

    def reconstruct_path(came_from,
                         start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)  # optional
        path.reverse()  # optional
        return path

    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        return float(abs(x1 - x2) + abs(y1 - y2))

    def a_star_search(graph, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(next, goal)
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far

    # ---------------------------------------------------------------
    # my original code for the foobar coding challenge starts below
    # first we will handle the fringe cases which break the pathfinding algorithm
    if xs == [0]:
        lowest_cost = 1
        return lowest_cost
    # coerce the input data into the format required by the pathfinding functions
    row_num = len(xs)
    col_num = len(xs[0])
    wall_coordinates = [(x, y) for x, val in enumerate(xs)
                        for y, val in enumerate(val) if val == 1]
    start, goal = (0, 0), (row_num - 1, col_num - 1)

    # start off by traversing the first path
    # it is possible the path may return and error, if the goal is obstructed
    try:
        gridwithweights = GridWithWeights(row_num, col_num)
        gridwithweights.walls = wall_coordinates
        came_from, cost_so_far = a_star_search(gridwithweights, start, goal)
        # +1 to account for the first space, which is not counted by this A* implimentation
        lowest_cost = cost_so_far[goal] + 1
        solution_wall_removed = ()
    except KeyError:
        # if no solution is found, set the cost to a large number
        lowest_cost = 1e100
        pass
    # now we remove walls one at a time and check to see if a new lowest_cost is found
    for wall in range(len(wall_coordinates)):
        # again, it is possible the path may return and error, if the goal is obstructed
        # keep trying to remove walls until a solution is found
        try:
            wall_removed = wall_coordinates[wall]
            new_wall_coordinates = [x for x in wall_coordinates if x != wall_removed]
            gridwithweights = GridWithWeights(row_num, col_num)
            gridwithweights.walls = new_wall_coordinates
            came_from, cost_so_far = a_star_search(gridwithweights, start, goal)
            test_cost = cost_so_far[goal] + 1
            if test_cost < lowest_cost:
                lowest_cost = test_cost
                solution_wall_removed = wall_removed
        except KeyError:
            pass
    return lowest_cost

# case 1 and 2 from foobar challenge
print(solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]))
print(solution([[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]))
# other test cases
#print(solution([[0],[0]]))
#print(solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]))
#print(solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 1], [1, 1, 1, 0]]))
#print(solution([[0, 0, 0, 0, 0, 1, 0, 0 , 0, 0]]))
#print(solution([[0]]))
#print(solution([0]))
#print(solution([[0,0],[0,0]]))
#print(solution([[0],[0],[0],[0],[0],[1],[0]]))

print(solution([[0, 1, 1, 1],
                [0, 1, 0, 0],
                [1, 0, 1, 0],
                [1, 1, 0, 0]]))