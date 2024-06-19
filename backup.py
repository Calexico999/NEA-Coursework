import random

#character set: \/-|
#boxdrawing characters: ┌ ┐ └ ┘ ─ │ ┬ ┴ ├ ┤ ┼

class StartNode:
    def start_node():
        startxnode = startynode = 0
        starttrack = random.randint(0, 3)
        startnode_pos = random.randint(0, 7)
        if starttrack == 1:
            startxnode = 0
        if starttrack == 3:
            startxnode = 7
        if starttrack == 2:
            startynode = 0
        if starttrack == 4:
            startynode = 7

        if starttrack == 1 or starttrack == 3:
            startynode = startnode_pos 
        if starttrack == 2 or starttrack == 4:
            startxnode = startnode_pos

        return startxnode, startynode



class Generate_Board:
    #generate an 8x8 board and then put the start and end nodes on the board
    def generate_board():
        board = []
        for i in range(8):
            board.append([])
            for j in range(8):
                board[i].append(0)
                
        start = StartNode.start_node()
        end = StartNode.start_node()
        while end == start:
            end = StartNode.start_node()
        board[start[0]][start[1]] = "S"
        board[end[0]][end[1]] = "E"
        return board

    #print the board in a more readable format

    def print_board(board):
        for row in board:
            print(' '.join(map(str, row)))







class Generate_Numbers():

    def generate_nums():
        count = 0
        sum = 0
        sum2 = 0

        while sum > 40 or sum == 0:
            rowgeneration = []
            count = 0
            sum = 0
            for i in range(8):
                if count == 0:
                    num = random.randint(1, 5)
                    rowgeneration.append(num)
                elif count >= 1 and count <= 6:
                    num = random.randint(1, 8)
                    rowgeneration.append(num)
                elif count == 7:
                    num = random.randint(1, 5)
                    rowgeneration.append(num)
                count += 1
                sum = sum + num

        #generate 8 more numbers that add up to the sum of the previous 8 numbers
        #append to colgeneration
        colgeneration = []
        #while sum2 != sum and all numbers in colgeneration are less than 9
        while sum2 != sum:
            colgeneration = []
            for i in range(8):
                if i == 0:
                    num = random.randint(1, 5)
                    colgeneration.append(num)
                elif i >= 1 and i <= 6:
                    num = random.randint(1, 8)
                    colgeneration.append(num)
                elif i == 7:
                    num = sum - sum2
                    colgeneration.append(num)
                sum2 += num
            if colgeneration[7] < 1 or colgeneration[7] > 8:
                sum2 = 0

        print(sum)
        print(sum2)
        return rowgeneration, colgeneration

        #return generation in a readable format
    



class DisplayBoard():
    def display_board():
        #print the board in format: top row is space, then the numbers in rowgeneration then the other rows all begin with the first number in colgeneration followed by the rest of the numbers in the row
        board = Generate_Board.generate_board()
        rowgeneration, colgeneration = Generate_Numbers.generate_nums()
        print("  ", end = "")
        for i in rowgeneration:
            print(i, end = " ")
        print()
        for i in range(8):
            print(colgeneration[i], end = " ")
            for j in range(8):
                print(board[i][j], end = " ")
            print()
        return board, rowgeneration, colgeneration

DisplayBoard.display_board()