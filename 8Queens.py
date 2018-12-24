import copy
import random
from random import randrange

class EightQueens:
    def __init__(self,positions):
        self.positions = positions #Positions is a tuple consisting of row and ool of each queen

    def show(self):
        for i  in range(0,8):
            row = [0] * 8
            for j in self.positions:
                x,y = j
                if(x == i):
                    row[y] = 1
            print(row)
        print("--------------------")




    def  findConflicts(self):
        sum = 0
        for i in self.positions:
            x,y = i
            for j in self.positions:
                m,n = j
                if(i == j): continue
                elif(x - y == m - n or x == m or y == n or x + y == m + n):
                    sum += 1
        return sum

    def getValidMoves(self,queen):
        x,y = queen
        moves = []
        for i in range(0,8):
            for j in range(0,8):
                if (i-j == x-y or i == x or j == y or i+j == x+y):
                    flag = True
                    for z in self.positions:
                        if (z == (i,j)):
                            flag = False
                    if(flag == True):
                        moves.append((i, j))
        return moves

    def moveQuuen(self,move,queenNumber):
        newPositions = copy.deepcopy(self.positions)
        newPositions[queenNumber] = move
        return newPositions



wrongMoves = 0

def LocalBestSearch(positions):
    state = EightQueens(positions)
    threshhold = state.findConflicts()
    random_queen_index = randrange(len(positions))
    childs = []



    if (state.findConflicts() == 0):
        # state.show()
        return state,"Solved"

    for i in (state.getValidMoves(positions[random_queen_index])):
        childs.append(EightQueens(state.moveQuuen(i, random_queen_index)))

    bestChild = random.choice(childs)
    minH = bestChild.findConflicts()

    # bestChild.show()
    # print(minH)

    for j in childs:
        if j.findConflicts() >= minH:
            # print("yas")
            continue
        if j.findConflicts() < minH:
            # print("nas")
            minH = j.findConflicts()
            bestChild = j


    return LocalBestSearch(bestChild.positions)
    # if(bestChild != state):
    # return LocalBestSearch(bestChild.positions)
    # else:
    #     return bestChild,"stuck"


def LocalBetterSearch(positions):
    state = EightQueens(positions)
    threshhold = state.findConflicts()
    random_queen_index = randrange(len(positions))
    childs = []
    if (state.findConflicts() == 0):
        return state,"Solved"

    for i in (state.getValidMoves(positions[random_queen_index])):
        childs.append(EightQueens(state.moveQuuen(i,random_queen_index)))

    bestChild = random.choice(childs)
    minH = bestChild.findConflicts()

    for j in childs:
        if j.findConflicts() >= minH:
            # print("yas")
            continue
        if j.findConflicts() < minH:
            # print("nas")
            minH = j.findConflicts()
            bestChild = j
            break


    return LocalBestSearch(bestChild.positions)

def LocalMASearch(boards):
    bestH = 100
    bestB = boards[0]
    for i in boards:
        board,message = LocalBestSearch(i)
        if (message == "Stuck in local Optima"):
            p = EightQueens(board)
            if(p.findConflicts()<bestH):
                bestH = p.findConflicts()
                bestB = p
        elif (message == "Solved"):
            return board,message
    return bestB,"This was the best we could do."



##############################

board1 = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)]
board2 = [(1,0),(1,2),(5,2),(7,7),(2,4),(6,7),(5,5),(3,2)]
board3 = [(3,0),(5,2),(3,2),(2,1),(4,5),(0,6),(2,7),(7,1)]
board4 = [(5,4),(2,3),(6,1),(0,1),(3,4),(7,7),(1,5),(4,5)]
board5 = [(7,2),(6,2),(5,2),(4,2),(3,2),(2,2),(1,2),(0,2)]
board6 = [(2,2),(5,2),(2,5),(3,6),(1,4),(4,7),(0,3),(5,5)]
board7 = [(4,7),(2,6),(1,3),(5,6),(4,7),(0,1),(0,0),(0,3)]
board8 = [(1,2),(5,4),(7,5),(3,4),(3,3),(6,5),(1,7),(0,2)]
board9 = [(7,0),(0,7),(4,5),(2,4),(3,7),(1,0),(0,1),(6,6)]
board10 = [(3,0),(1,2),(0,1),(2,0),(3,5),(2,2),(6,7),(5,6)]
board11 = [(1,2),(3,4),(5,6),(7,0),(0,1),(3,3),(5,5),(7,7)]
board12 = [(6,0),(4,4),(7,7),(1,2),(3,3),(5,3),(5,2),(6,1)]

boards = [board1,board2,board3,board4,board5,board6,board7,board8,board9,board10,board11,board12]

try:
    board, message = LocalBestSearch(board12)  # LocalBestSearch can solve any board with my tests. but sometimes it may take too long (hence the runtime error)
    print(message)
    # board.show()  #Uncomment to show the final board.
except RuntimeError as re:
    print("Sorry,but this Search Agent wasn't able to complete it's task in time")
#Results on first test run:
#solved board1,board2,board3,board4

try:
    board, message = LocalBetterSearch(board12)  # LocalBestSearch can solve any board with my tests. but sometimes it may take too long (hence the runtime error)
    print(message)
    #board.show() #Uncomment to show the final board.
except RuntimeError as re:
    print("Sorry,but this Search Agent wasn't able to complete it's task in time")
#Only failed on board8


try:
    board, message = LocalMASearch(boards)  # Multi-Agent search using all of the 12 boards.
    print(message) # Since it uses the LocalBestSearch above, it may give runtime error sometimes.
    #board.show() #Uncomment to show the final state
except RuntimeError as re:
    print("Sorry,but this Search Agent wasn't able to complete it's task in time")


#My test results:
#Local Best Search = 100% solve rate.
#Local Better Search = 91.6% solve rate.
#Local MultiAgent Search = 100% solve rate.