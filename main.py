import random

class StartNode:
    def start_node():
        starttrack = random.randint(1, 4)
        startnode_pos = random.randint(1, 8)
        if starttrack == 1:
            startxnode = 0 #0
        if starttrack == 3:
            startxnode = 7 #7
        if starttrack == 2:
            startynode = 0 #0
        if starttrack == 4:
            startynode = 7 #7

        if starttrack == 1 or starttrack == 3:
            startynode = startnode_pos
        if starttrack == 2 or starttrack == 4:
            startxnode = startnode_pos

        return startxnode, startynode


start = StartNode.start_node()
end = StartNode.start_node()

print(start)
print(end)

class Generate_Board:
    #generate an 8x8 board and then put the start and end nodes on the board
    def generate_board():
        board = []
        for i in range(8):
            board.append([])
            for j in range(8):
                board[i].append(0)
        board[start[0]][start[1]] = "S"
        board[end[0]][end[1]] = "E"
        return board
x = Generate_Board.generate_board()
print(x)

