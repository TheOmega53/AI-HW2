from aenum import Enum
import copy


class Actions(Enum):
    Right = 1
    Left = 2
    Up = 3
    Down = 4
#
def findZero(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if (puzzle[i][j] == 0):
                return (i,j)
#
def getValidActions(puzzle):
    ActionList = ()
    x,y = findZero(puzzle)
    if (x==0):
        if(y==0): ActionList = (Actions.Right,Actions.Down)
        if(y==1): ActionList= (Actions.Right,Actions.Left,Actions.Down)
        if(y==2): ActionList = (Actions.Left,Actions.Down)

    elif(x==1):
        if(y==0): ActionList = (Actions.Right,Actions.Up,Actions.Down)
        if(y==1): ActionList = (Actions.Right,Actions.Left,Actions.Up,Actions.Down)
        if(y==2): ActionList = (Actions.Left,Actions.Up,Actions.Down)

    elif(x==2):
        if(y==0): ActionList = (Actions.Right,Actions.Up)
        if(y==1): ActionList = (Actions.Right,Actions.Left,Actions.Up)
        if(y==2): ActionList = (Actions.Left,Actions.Up)

    return ActionList
#
def doAction(action,puzzle):

    newPuzzle = copy.deepcopy(puzzle)
    x,y = findZero(newPuzzle)
    if action.value == 1: newPuzzle[x][y], newPuzzle[x][y+1] = newPuzzle[x][y+1] , newPuzzle[x][y]
    if action.value == 2: newPuzzle[x][y], newPuzzle[x][y-1] = newPuzzle[x][y-1] , newPuzzle[x][y]
    if action.value == 3: newPuzzle[x][y], newPuzzle[x-1][y] = newPuzzle[x-1][y] , newPuzzle[x][y]
    if action.value == 4: newPuzzle[x][y], newPuzzle[x+1][y] = newPuzzle[x+1][y] , newPuzzle[x][y]
    return newPuzzle


class state:
    def __init__(self, puzzle, childs, parent):
        self.puzzle = puzzle
        self.childs = childs
        self.parent = parent

    def getChilds(self):
        childs = []
        for i,j in enumerate(getValidActions(self.puzzle)):
            childs.append(state(doAction(j,self.puzzle),0,self))
        self.childs = childs
        return childs

    def show(self):
        for i in range(len(self.puzzle)):
            print (self.puzzle[i])
        print('-----------------')

    def calculateManhattan(self):
        Manhattan = 0
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                # print(abs(int(self.puzzle[i][j]%3)-(j)))
                if(self.puzzle[i][j] != 0):
                    Manhattan += (abs(int(self.puzzle[i][j]/3) - i) + abs(int(self.puzzle[i][j]%3)- j))

        return Manhattan

    def isGoal(self):
        if (self.puzzle == [[0, 1, 2],
                            [3, 4, 5],
                            [6, 7, 8]]):
            return True
        else:
            return False




def localBestSearch(puzzle):
    p = state(puzzle, -1, -1)
    if(p.isGoal()):
        return (p.puzzle,"Solved")
    elif(not p.isGoal()):
            minH = p.calculateManhattan()
            best = p
            p.getChilds()
            for i in p.childs:
                if(i.calculateManhattan() <= minH):
                    minH = i.calculateManhattan()
                    best = i
            if(minH < p.calculateManhattan()):
                return localBestSearch(best.puzzle)
            else:
                return (p.puzzle,"Stuck in Local Optima")

def localBetterSearch(puzzle):
    p = state(puzzle, -1, -1)
    if(p.isGoal()):
        return (p.puzzle,"Solved")
    elif(not p.isGoal()):
            h = p.calculateManhattan()
            best = p
            p.getChilds()
            for i in p.childs:
                if(i.calculateManhattan() <= h):
                    h = i.calculateManhattan()
                    best = i
                    break
            if(h < p.calculateManhattan()):
                return localBetterSearch(best.puzzle)
            else:
                return (p.puzzle,"Stuck in Local Optima")

def localMASearch(puzzles):
    bestH = 100
    bestP = puzzles[0]
    for i in puzzles:
        puzzle,message = localBestSearch(i)
        if(message == "Stuck in Local Optima"):
            p = state(puzzle,0,0)
            if (p.calculateManhattan() < bestH):
                bestH = p.calculateManhattan()
                bestP = puzzle
        elif(message == "Solved"):
            return (puzzle,message)
    return bestP,"This is the best we could reach"



#####################TEST###################
puzzle1 = [[1, 2, 0],  
           [3, 4, 5],
           [6, 7, 8]]

puzzle2 = [[1, 4, 0],
           [6, 5, 2],
           [7, 3, 8]]

puzzle3 = [[4, 5, 6],
           [1, 3, 2],
           [8, 7, 0]]

puzzle4 = [[3, 2, 5],
           [6, 1, 8],
           [7, 4, 0]]

puzzle5 = [[7, 2, 0],
           [4, 3, 1],
           [5, 6, 8]]

puzzle6 = [[4, 5, 6],
           [2, 1, 0],
           [3, 8, 7]]

puzzle7 = [[1, 5, 4],
           [6, 2, 8],
           [7, 3, 0]]

puzzle8 = [[1, 5, 4],
           [6, 3, 0],
           [7, 2, 8]]

puzzle9 = [[0, 2, 1],
           [3, 5, 4],
           [6, 7, 8]]

puzzle10 = [[3, 4, 2],
            [6, 7, 5],
            [0, 1, 8]]

puzzle11 = [[2, 3, 6],
            [0, 5, 1],
            [7, 4, 8]]

puzzle12 = [[0, 1, 2],
            [6, 7, 8],
            [5, 4, 3]]

p = [puzzle1,puzzle2,puzzle3,puzzle4,puzzle5,puzzle6,puzzle7,puzzle8,puzzle9,puzzle10,puzzle11,puzzle12]


print("\n Results for Local Best Search:\n")
for i in p:
    finalState,Message = localBestSearch(i)
    print(Message)

    #We can see that Local Best Search solves 4 out of 12 puzzles. hence 33.3% solve ratio.

print("\n Results for Local Better Search:\n")
for i in p:
    finalState,Message = localBetterSearch(i)
    print(Message)

    #We can see that Local Better search solves 2 out of 12 puzzles. hence 16.6% solve ratio.

print("\n Results for Local Multi-Agent Search:\n")
finalState,Message = localMASearch(p)
print(Message)

    #We can see that multi-agent search solves the puzzle because one of it's agents was able to solve the puzzle.


#Obviously, the best solution for this problem would require us to do a
# A* search first to get all the most accurate heuristics and then do a search on that
# Which would be very inefficient.

#Results:
#Local Best(Steepest) search: 33% Solve rate
#Local Better(First steeper point) search: 16.6% solve rate.
#Local Multi-agent search using 12 agents : 100% solve rate.



