def solution(xs):  
    # The following is taken from on online source on A* Pathfinding, cited below
    # note the code has been modified to run in python 2.7 and unused parts of the orginal source code have been removed for readability
    #---------------------------------------------------------------
    # Sample code from https://www.redblobgames.com/pathfinding/a-star/
    # Copyright 2014 Red Blob Games <redblobgames@gmail.com>
    #
    # Feel free to use this code in your own projects, including commercial projects
    # License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>
    
    # some of these types are deprecated: https://www.python.org/dev/peps/pep-0585/
    from typing import Protocol, Dict, List, Iterator, Tuple, TypeVar, Optional
    T = TypeVar('T')
    
    Location = TypeVar('Location')
    class Graph(Protocol):
        def neighbors(self, id: Location) -> List[Location]: pass
    
    # utility functions for dealing with square grids
    def from_id_width(id, width):
        return (id % width, id // width)
    
    def draw_tile(graph, id, style):
        r = " . "
        if 'number' in style and id in style['number']: r = " %-2d" % style['number'][id]
        if 'point_to' in style and style['point_to'].get(id, None) is not None:
            (x1, y1) = id
            (x2, y2) = style['point_to'][id]
            if x2 == x1 + 1: r = " > "
            if x2 == x1 - 1: r = " < "
            if y2 == y1 + 1: r = " v "
            if y2 == y1 - 1: r = " ^ "
        if 'path' in style and id in style['path']:   r = " @ "
        if 'start' in style and id == style['start']: r = " A "
        if 'goal' in style and id == style['goal']:   r = " Z "
        if id in graph.walls: r = "###"
        return r
    
    def draw_grid(graph, **style):
        print("___" * graph.width)
        for y in range(graph.height):
            for x in range(graph.width):
                print("%s" % draw_tile(graph, (x, y), style), end="")
            print()
        print("~~~" * graph.width)
    
    GridLocation = Tuple[int, int]
    
    class SquareGrid:
        def __init__(self, width: int, height: int):
            self.width = width
            self.height = height
            self.walls: List[GridLocation] = []
        
        def in_bounds(self, id: GridLocation) -> bool:
            (x, y) = id
            return 0 <= x < self.width and 0 <= y < self.height
        
        def passable(self, id: GridLocation) -> bool:
            return id not in self.walls
        
        def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
            (x, y) = id
            neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
            # see "Ugly paths" section for an explanation:
            if (x + y) % 2 == 0: neighbors.reverse() # S N W E
            results = filter(self.in_bounds, neighbors)
            results = filter(self.passable, results)
            return results
    
    class WeightedGraph(Graph):
        def cost(self, from_id: Location, to_id: Location) -> float: pass
    
    class GridWithWeights(SquareGrid):
        def __init__(self, width: int, height: int):
            super().__init__(width, height)
            self.weights: Dict[GridLocation, float] = {}
        
        def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
            return self.weights.get(to_node, 1)
    
    import heapq
    
    class PriorityQueue:
        def __init__(self):
            self.elements: List[Tuple[float, T]] = []
        
        def empty(self) -> bool:
            return not self.elements
        
        def put(self, item: T, priority: float):
            heapq.heappush(self.elements, (priority, item))
        
        def get(self) -> T:
            return heapq.heappop(self.elements)[1]
    
    # thanks to @m1sp <Jaiden Mispy> for this simpler version of
    # reconstruct_path that doesn't have duplicate entries
    
    def reconstruct_path(came_from: Dict[Location, Location],
                         start: Location, goal: Location) -> List[Location]:
        current: Location = goal
        path: List[Location] = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start) # optional
        path.reverse() # optional
        return path
    
    def heuristic(a: GridLocation, b: GridLocation) -> float:
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)
    
    def a_star_search(graph: WeightedGraph, start: Location, goal: Location):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from: Dict[Location, Optional[Location]] = {}
        cost_so_far: Dict[Location, float] = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while not frontier.empty():
            current: Location = frontier.get()
            
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
    #---------------------------------------------------------------
    #my orginal code for the foobar coding challenge starts below
    #coerce the input data into the format required by the pathfinding functions
    row_num = len(xs)
    col_num = len(xs[0])
    wall_coordinates = [(x,y) for x,val in enumerate(xs)
                        for y, val in enumerate(val) if val==1]
    start, goal = (0, 0), (row_num-1, col_num-1)
    
    #start off by traversing the first path
    gridwithweights = GridWithWeights(row_num, col_num)
    gridwithweights.walls = wall_coordinates
    came_from, cost_so_far = a_star_search(gridwithweights, start, goal)
    #+1 to account for the first space, which is not counted by this A* implimentation
    lowest_cost = cost_so_far[goal] + 1
    wall_removed = None
    #now we remove walls one at a time and check to see if a new lowest_cost is found
    for wall in range(len(wall_coordinates)):
        wall_removed = wall_coordinates[wall]
        new_wall_coordinates = [x for x in wall_coordinates if x != wall_removed]
        gridwithweights = GridWithWeights(row_num, col_num)
        gridwithweights.walls = new_wall_coordinates
        came_from, cost_so_far = a_star_search(gridwithweights, start, goal)
        test_cost = cost_so_far[goal] + 1
        if test_cost < lowest_cost:
            lowest_cost = test_cost
            wall_removed = wall_removed
            
    return print(lowest_cost)
#challenge test cases
solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]])    
solution([[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]])
#frigne test cases
solution([[0,0],[1,0]])  
solution([[0,0,0],[0,0,0],[0,0,0]])  