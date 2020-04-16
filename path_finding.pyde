w = 30
fiter = True

wall_open = [48, 49, 50, 51, 52, 53, 54]
all_cells_open_path = []

open_set = {}
closed_set = {}
goal_path = []

class Cell:

    def __init__(self, current, previous):
        self.current = current
        self.previous = previous

    def ravel_index(self):
        return self.current[0] * 20 + self.current[1]

def setup():
    global img, w, all_cells_open_path, goal_path
    size(600, 600)
    background(51)
    img = loadImage('maze2.jpg')
    image(img, 0, 0)
    for r in range(img.height / w):
        for c in range(img.width / w):
            all_cells_open_path.append(get_open_wall(r, c))
    goal_path = main([0, 0])


def draw():
    global fiter, goal_path
    if fiter:
        fiter = False
        
        for i in range(len(goal_path) - 1):
            centerf = center_of_cell(goal_path[i][0], goal_path[i][1])
            centers = center_of_cell(goal_path[i + 1][0], goal_path[i + 1][1])
            stroke(20,200,185)
            strokeWeight(2)
            line(centerf[0], centerf[1], centers[0], centers[1])
            
        fill(255,10,105)
        ellipse(15, 15, 15, 15)
        ellipse(585, 585, 15, 15)


def get_open_wall(r, c):
    global img, w, wall
    center = center_of_cell(r, c)
    diro = []
    if red(img.get(center[0] + w / 2, center[1])) in wall_open:
        diro.append('r')
    if red(img.get(center[0] - w / 2, center[1])) in wall_open:
        diro.append('l')
    if red(img.get(center[0], center[1] - w / 2)) in wall_open:
        diro.append('t')
    if red(img.get(center[0], center[1] + w / 2)) in wall_open:
        diro.append('b')

    return diro

def center_of_cell(r, c):
    global w
    x = c * w + w / 2
    y = r * w + w / 2
    return [x, y]

def main(current):
    global all_cells_open_path, closed_set, open_set
    open_set[str(current)] = Cell(current, current)
    while True:
        new_open_set = {}
        for cell in open_set.values():
            closed_set[str(cell.current)] = cell
            for op in all_cells_open_path[cell.ravel_index()]:
                if op == 'r':
                    next = [cell.current[0], cell.current[1] + 1]
                elif op == 'b':
                    next = [cell.current[0] + 1, cell.current[1]]
                elif op == 'l':
                    next = [cell.current[0], cell.current[1] - 1]
                elif op == 't':
                    next = [cell.current[0] - 1, cell.current[1]]

                if str(next) in closed_set.keys() or str(next) in open_set.keys():
                    continue
                new_open_set[str(next)] = Cell(next, cell.current)
        del open_set
        open_set = new_open_set.copy()
        if check_goal(open_set):
            return goal_path(open_set, closed_set)

def check_goal(open_set):
    if str([19, 19]) in open_set.keys():
        return True
    else:
        return False

def goal_path(open_set, closed_set):
    path = []
    cell = open_set[str([19, 19])]

    while cell.current != [0, 0]:
        path.insert(0, cell.current)
        cell = closed_set[str(cell.previous)]
    path.insert(0, cell.current)
    return path
