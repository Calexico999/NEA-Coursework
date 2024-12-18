import random
import datetime
import pickle
import os

class GenerateRandomPath:
    def __init__(self, board_size):
        #Initializes the path generator with the given board size
        self.board_size = board_size

    def generate_start_node(self):
        coord1 = random.randint(0, self.board_size - 1)
        coord2 = random.randint(0,3)
        if coord2 == 0:
            startxnode = 0
            startynode = coord1
        elif coord2 == 1:
            startxnode = self.board_size - 1
            startynode = coord1
        elif coord2 == 2:
            startxnode = coord1
            startynode = 0
        else:
            startxnode = coord1
            startynode = self.board_size - 1
        return startxnode, startynode

    def dfs(self, start):
        # Performs a depth-first search to generate a random path on the board
        min_length = (self.board_size ** 2) * 0.4
        max_length = (self.board_size ** 2) * 0.6
        stack = [(start, [start])]
        self.visited = set()
        
        while stack:
            v, path = stack.pop()
            if len(path) >= max_length:
                return None
            if len(path) >= min_length:
                # If on edge, return the path
                if v[0] == 0 or v[0] == self.board_size - 1 or v[1] == 0 or v[1] == self.board_size - 1:
                    # Check if all rows and columns have been visited at least once
                    rows = [0] * self.board_size
                    cols = [0] * self.board_size
                    for (x, y) in path:
                        rows[x] = 1
                        cols[y] = 1
                    if 0 in rows or 0 in cols:
                        return None
                    return path

            self.visited.add(v)
            x, y = v
            all_next = []

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                x1, y1 = x + dx, y + dy
                if x1 < 0 or x1 >= self.board_size or y1 < 0 or y1 >= self.board_size:
                    continue
                if (x1, y1) in self.visited:
                    continue
                all_next.append((x1, y1))

            if all_next:
                next_node = random.choice(all_next)
                stack.append((next_node, path + [next_node]))

        return None  # If no valid path is found


class Generator:
    def build_board(self, board_size):
        while str(board_size).isnumeric() == False or int(board_size) < 4 or int(board_size) > 10:
            board_size = input("Enter the size of the board (edge length in range 4-10): ")
        board_size = int(board_size)
        path = None
        path_generator = GenerateRandomPath(board_size)  # Instance of path generator
        while path is None:
            start = path_generator.generate_start_node()
            path = path_generator.dfs(start)
        build_board = [['X' for _ in range(board_size)] for _ in range(board_size)]
        previousx = path[0][0]
        previousy = path[0][1]        
        currentx = path[1][0]
        currenty = path[1][1]

        if previousx == currentx:
            if previousy < currenty:
                directionpath = "right"
            else:
                directionpath = "left"
        else:
            if previousx < currentx:
                directionpath = "down"
            else:
                directionpath = "up"

        if directionpath == "right":
            if previousx == 0:
                build_board[previousx][previousy] = "└"
            elif previousx == board_size - 1:
                build_board[previousx][previousy] = "┌"
            elif previousy == 0:
                build_board[previousx][previousy] = "─"
        elif directionpath == "left":
            if previousx == 0:
                build_board[previousx][previousy] = "┘"
            elif previousx == board_size - 1:
                build_board[previousx][previousy] = "┐"
            elif previousy == board_size - 1:
                build_board[previousx][previousy] = "─"
        elif directionpath == "up":
            if previousx == board_size - 1:
                build_board[previousx][previousy] = "│"
            elif previousy == 0:
                build_board[previousx][previousy] = "┘"
            elif previousy == board_size - 1:
                build_board[previousx][previousy] = "└"
        elif directionpath == "down":
            if previousx == 0:
                build_board[previousx][previousy] = "│"
            elif previousy == 0:
                build_board[previousx][previousy] = "┐"
            elif previousy == board_size - 1:
                build_board[previousx][previousy] = "┌"
        
        Generator.make_board(path, build_board)

        currentx = path[-2][0]
        currenty = path[-2][1]
        endx = path[-1][0]
        endy = path[-1][1]
        if currentx == endx:
            if currenty < endy:
                directionpath = "right"
            else:
                directionpath = "left"
        else:
            if currentx < endx:
                directionpath = "down"
            else:
                directionpath = "up"

        if endx == 0:
            if directionpath == "right":
                build_board[endx][endy] = "┘"
            elif directionpath == "up":
                build_board[endx][endy] = "│"
            elif directionpath == "left":
                build_board[endx][endy] = "└"
        elif endx == board_size - 1:
            if directionpath == "right":
                build_board[endx][endy] = "┐"
            elif directionpath == "down":
                build_board[endx][endy] = "│"
            elif directionpath == "left":
                build_board[endx][endy] = "┌"
        elif endy == 0:
            if directionpath == "left":
                build_board[endx][endy] = "─"
            elif directionpath == "down":
                build_board[endx][endy] = "┘"
            elif directionpath == "up":
                build_board[endx][endy] = "┐"
        elif endy == board_size - 1:
            if directionpath == "right":
                build_board[endx][endy] = "─"
            elif directionpath == "down":
                build_board[endx][endy] = "└"
            elif directionpath == "up":
                build_board[endx][endy] = "┌"


        xshape = build_board[start[0]][start[1]]
        yshape = build_board[path[-1][0]][path[-1][1]]
        listofchars = ["┌", "┐", "└", "┘", "─", "│"]
        column_totals = []
        row_totals = []
        for i in range(board_size):
            column_total = 0
            for j in range(board_size):
                if build_board[j][i] in listofchars:
                    column_total += 1
            column_totals.append(column_total)
        for i in range(board_size):
            row_total = 0
            for j in range(board_size):
                if build_board[i][j] in listofchars:
                    row_total += 1
            row_totals.append(row_total)

        # save state of board, which will not be overwritten
        SAVEDBOARD = []
        for i in range(len(build_board)):
            SAVEDBOARD.append(build_board[i].copy())

        startingshapes = []
        startingshapes.append((start[0], start[1], xshape))
        startingshapes.append((endx, endy, yshape))

        board = [['N' for _ in range(board_size)] for _ in range(board_size)]
        board[start[0]][start[1]] = xshape
        board[endx][endy] = yshape


        return board, column_totals, row_totals, SAVEDBOARD, startingshapes, board_size

    def manual_board(self):
        startingshapes = []
        board_size = input("Enter the size of the board (edge length in range 4-10): ")
        while board_size.isnumeric() == False or int(board_size) < 4 or int(board_size) > 10:
            board_size = input("Enter the size of the board (edge length in range 4-10): ")
        
        board_size = int(board_size)

        board = [["N"] * board_size for _ in range(board_size)]
        start, xshape = self.get_starting_position(board_size)
        end, yshape = self.get_ending_position(board_size, start)


        startingshapes.append((start[0], start[1], xshape))
        startingshapes.append((end[0], end[1], yshape))

        other_nodes = True
        while other_nodes:
            morenodes = input("Are there any more nodes to add? (Y/N): ")
            if morenodes.lower() == 'y':
                self.add_more_nodes(board, startingshapes)
            elif morenodes.lower() == 'n':
                other_nodes = False
            else:
                print("Invalid input. Please enter Y or N.")

        SAVEDBOARD = []
        column_totals = []
        row_totals = []

        return board, column_totals, row_totals, SAVEDBOARD, startingshapes, board_size

    def get_starting_position(self, size):
        while True:
            try:
                start = input("Enter the starting position in the format x,y: ").split(',')
                start = (int(start[0]), int(start[1]))
                if 0 <= start[0] < size and 0 <= start[1] < size and (start[0] == 0 or start[0] == size - 1 or start[1] == 0 or start[1] == size - 1):
                    xshape = self.get_shape(start)
                    return start, xshape
                else:
                    print("Starting position out of bounds. Please try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter coordinates in the format x,y.")

    def get_shape(self, position):
        while True:
            shape = input(f"Enter the shape at position {position[0]},{position[1]} (V, H, LD, LU, RD, RU): ")
            if shape in ["V", "H", "LD", "LU", "RD", "RU"]:
                return shape
            else:
                print("Invalid shape. Please enter one of the following: V, H, LD, LU, RD, RU")

    def get_ending_position(self, size, start):
        while True:
            try:
                end = input("Enter the ending position in the format x,y: ").split(',')
                end = (int(end[0]), int(end[1]))
                if 0 <= end[0] < size and 0 <= end[1] < size and end != start and (end[0] == 0 or end[0] == size - 1 or end[1] == 0 or end[1] == size - 1):
                    yshape = self.get_shape(end)
                    return end, yshape
                else:
                    print("Ending position out of bounds or same as starting position. Please try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter coordinates in the format x,y.")

    def add_more_nodes(self, board, startingshapes):
        while True:
            try:
                node = input("Enter the node position in the format x,y: ").split(',')
                node = (int(node[0]), int(node[1]))
                if node not in [(x[0], x[1]) for x in startingshapes]:
                    if 0 <= node[0] < len(board) and 0 <= node[1] < len(board):
                        extrashape = self.get_shape(node)
                        startingshapes.append((node[0], node[1], extrashape))
                        break
                    else:
                        print("Node position out of bounds. Please try again.")
                else:
                    print("Node already written with a shape. Type o to overwrite, or any other key to re-enter.")
                    overwrite = input()
                    if overwrite.lower() == 'o':
                        extrashape = self.get_shape(node)
                        startingshapes.append((node[0], node[1], extrashape))
                        break
            except (ValueError, IndexError):
                print("Invalid input. Please enter coordinates in the format x,y.")

    @staticmethod
    def make_board(path, build_board):
        if len(path) <= 2:
            return

        previousx, previousy = path[0][0], path[0][1]
        currentx, currenty = path[1][0], path[1][1]
        nextx, nexty = path[2][0], path[2][1]

        if nextx + 2 == previousx or nextx - 2 == previousx:
            build_board[currentx][currenty] = "│"
        elif nexty + 2 == previousy or nexty - 2 == previousy:
            build_board[currentx][currenty] = "─"
        elif nextx + 1 == previousx and nexty + 1 == previousy:
            if currentx == previousx:
                build_board[currentx][currenty] = "└"
            else:
                build_board[currentx][currenty] = "┐"
        elif nextx - 1 == previousx and nexty - 1 == previousy:
            if currentx == previousx:
                build_board[currentx][currenty] = "┐"
            else:
                build_board[currentx][currenty] = "└"
        elif nextx + 1 == previousx and nexty - 1 == previousy:
            if currentx == previousx:
                build_board[currentx][currenty] = "┘"
            else:
                build_board[currentx][currenty] = "┌"
        else:
            if currentx == previousx:
                build_board[currentx][currenty] = "┌"
            else:
                build_board[currentx][currenty] = "┘"

        Generator.make_board(path[1:], build_board)


class Solver:
    def print_board(board):
        for row in board:
            print(' '.join(map(str, row)))
    
    def Solve(board, column_totals, row_totals, SAVEDBOARD, startingshapes, generation, board_size):
        start = (startingshapes[0][0], startingshapes[0][1])
        end = (startingshapes[1][0], startingshapes[1][1])
        bruteforceneeded = False
        edgerulesneeded = False
        any_changes = True

        # Box drawing characters: ┌ ┐ └ ┘ ─ │
        RD = "┌"
        LD = "┐"
        RU = "└"
        LU = "┘"
        H = "─"
        V = "│"
        DOT = "."
        NULL = "N"
        X = "X"
        unsures = []
        flagimpossible = False
        trynew = False
        dots = []
        unsureshapes = []
        changecheck = True
        trysecond = False
        dots_two = []


        def get_totals():
            column_totals = []
            row_totals = []
            print()
            print("First column is column 0, first row is row 0.")
            print("If you make a mistake, enter any invalid input (e.g. nothing) and you will be prompted to re-enter all column or row totals.")

            while len(column_totals) < board_size:
                i = 0
                while i < board_size:
                    try:
                        column_totals.append(int(input(f"Enter the total for column {i}: ")))
                        i += 1
                    except ValueError:
                        print("Invalid input. Please enter a number. Re-enter all column totals.")
                        column_totals = []
                        i = 11

                for i in range(len(column_totals)):
                    if column_totals[i] > board_size:
                        print("No column total cannot be greater than the board size. Re-enter all column totals.")
                        column_totals = []



            while len(row_totals) < board_size:
                i = 0
                while i < board_size:
                    try:
                        row_totals.append(int(input(f"Enter the total for row {i}: ")))
                        i += 1
                    except ValueError:
                        print("Invalid input. Please enter a number. Re-enter all row totals.")
                        row_totals = []
                        i = 11

                for i in range(len(row_totals)):
                    if row_totals[i] > board_size:
                        print("No row total cannot be greater than the board size. Re-enter all row totals.")
                        row_totals = []


            for i in range(len(startingshapes)):
                if startingshapes[i][2] == 'RD':
                    startingshapes[i] = (startingshapes[i][0], startingshapes[i][1], RD)
                    board[startingshapes[i][0]][startingshapes[i][1]] = RD
                elif startingshapes[i][2] == 'LD':
                    startingshapes[i] = (startingshapes[i][0], startingshapes[i][1], LD)
                    board[startingshapes[i][0]][startingshapes[i][1]] = LD
                elif startingshapes[i][2] == 'RU':
                    startingshapes[i] = (startingshapes[i][0], startingshapes[i][1], RU)
                    board[startingshapes[i][0]][startingshapes[i][1]] = RU
                elif startingshapes[i][2] == 'LU':
                    startingshapes[i] = (startingshapes[i][0], startingshapes[i][1], LU)
                    board[startingshapes[i][0]][startingshapes[i][1]] = LU
                elif startingshapes[i][2] == 'H':
                    startingshapes[i] = (startingshapes[i][0], startingshapes[i][1], H)
                    board[startingshapes[i][0]][startingshapes[i][1]] = H
                elif startingshapes[i][2] == 'V':
                    startingshapes[i] = (startingshapes[i][0], startingshapes[i][1], V)
                    board[startingshapes[i][0]][startingshapes[i][1]] = V

            return column_totals, row_totals

        if column_totals == []:
            column_totals, row_totals = get_totals()
            while sum(column_totals) != sum(row_totals):
                print("The sum of the column totals must equal the sum of the row totals.")
                column_totals, row_totals = get_totals()

        nodenumber = 0
        for i in range(len(column_totals)):
            nodenumber += column_totals[i]

        characters = {
            'RD': RD,
            'LD': LD,
            'RU': RU,
            'LU': LU,
            'H': H,
            'V': V
        }
        
        definites = {
            'RD': RD,
            'LD': LD,
            'RU': RU,
            'LU': LU,
            'H': H,
            'V': V,
            '.': DOT
        }

        knowns = {
            'RD': RD,
            'LD': LD,
            'RU': RU,
            'LU': LU,
            'H': H,
            'V': V,
            'X': 'X'
        }

        shapes = {
            'RD': RD,
            'LD': LD,
            'RU': RU,
            'LU': LU,
            'H': H,
            'V': V
        }

        def findshape(a,b):
            if a == 'left':
                if b == 'up':
                    return LU
                elif b == 'down':
                    return LD
                elif b == 'right':
                    return H
            if a == 'up':
                if b == 'down':
                    return V
                elif b == 'right':
                    return RU
                elif b == 'left':
                    return LU
            if a == 'down':
                if b == 'right':
                    return RD
                elif b == 'left':
                    return LD
                elif b == 'up':
                    return V
            if a == 'right':
                if b == 'left':
                    return H
                elif b == 'up':
                    return RU
                elif b == 'down':
                    return RD

        def add_to_unsures(a,b):
            if bruteforceneeded == True and generation == "n":
                unsures.append((a, b, board[a][b]))


        while any_changes or bruteforceneeded:

            any_changes = False
            edgerulesneeded = False
            flagimpossible = False

            # First stage: change all Ns which connect to a start or end node to '.'
            print("Initial board:")
            Solver.print_board(board)
            print("\nFirst stage:")
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] in characters.values():
                        if board[i][j] == RD:
                            if i + 1 < len(board) and board[i + 1][j] == "N":
                                add_to_unsures(i + 1, j)
                                board[i + 1][j] = '.'
                                any_changes = True
                            if j + 1 < len(board) and board[i][j + 1] == "N":
                                add_to_unsures(i, j + 1)
                                board[i][j + 1] = '.'
                                any_changes = True
                        elif board[i][j] == LD:
                            if i + 1 < len(board) and board[i + 1][j] == "N":
                                add_to_unsures(i + 1, j)
                                board[i + 1][j] = '.'
                                any_changes = True
                            if j - 1 >= 0 and board[i][j - 1] == "N":
                                add_to_unsures(i, j - 1)
                                board[i][j - 1] = '.'
                                any_changes = True
                        elif board[i][j] == RU:
                            if i - 1 >= 0 and board[i - 1][j] == "N":
                                add_to_unsures(i - 1, j)
                                board[i - 1][j] = '.'
                                any_changes = True
                            if j + 1 < len(board) and board[i][j + 1] == "N":
                                add_to_unsures(i, j + 1)
                                board[i][j + 1] = '.'
                                any_changes = True
                        elif board[i][j] == LU:
                            if i - 1 >= 0 and board[i - 1][j] == "N":
                                add_to_unsures(i - 1, j)
                                board[i - 1][j] = '.'
                                any_changes = True
                            if j - 1 >= 0 and board[i][j - 1] == "N":
                                add_to_unsures(i, j - 1)
                                board[i][j - 1] = '.'
                                any_changes = True
                        elif board[i][j] == H:
                            if j + 1 < len(board) and board[i][j + 1] == "N":
                                add_to_unsures(i, j + 1)
                                board[i][j + 1] = '.'
                                any_changes = True
                            if j - 1 >= 0 and board[i][j - 1] == "N":
                                add_to_unsures(i, j - 1)
                                board[i][j - 1] = '.'
                                any_changes = True
                        else:
                            if i + 1 < len(board) and board[i + 1][j] == "N":
                                add_to_unsures(i + 1, j)
                                board[i + 1][j] = '.'
                                any_changes = True
                            if i - 1 >= 0 and board[i - 1][j] == "N":
                                add_to_unsures(i - 1, j)
                                board[i - 1][j] = '.'
                                any_changes = True

            Solver.print_board(board)

            # Second stage: check each column to see if all possible nodes are used
            temp = True
            while temp == True:
                temp = False
                for j in range(len(board)):
                    count = 0
                    for i in range(len(board)):
                        if board[i][j] in definites.values():
                            count += 1
                    if count == column_totals[j]:
                        for i in range(len(board)):
                            if board[i][j] == "N":
                                add_to_unsures(i, j)
                                board[i][j] = 'X'
                                temp = True
                                any_changes = True
                    if count > column_totals[j]:
                        flagimpossible = True

                for i in range(len(board)):
                    count = 0
                    for j in range(len(board)):
                        if board[i][j] in definites.values():
                            count += 1
                    if count == row_totals[i]:
                        for j in range(len(board)):
                            if board[i][j] == "N":
                                add_to_unsures(i, j)
                                board[i][j] = 'X'
                                temp = True
                                any_changes = True
                    if count > row_totals[i]:
                        flagimpossible = True

                # if number of non-Xs in each column is equal to the column total, change all Ns to dots
                for j in range(len(board)):
                    count = 0
                    for i in range(len(board)):
                        if board[i][j] != 'X':
                            count += 1
                    if count == column_totals[j]:
                        for i in range(len(board)):
                            if board[i][j] == "N":
                                add_to_unsures(i, j)
                                board[i][j] = '.'
                                temp = True
                                any_changes = True
                # do the same for rows
                for i in range(len(board)):
                    count = 0
                    for j in range(len(board)):
                        if board[i][j] != 'X':
                            count += 1
                    if count == row_totals[i]:
                        for j in range(len(board)):
                            if board[i][j] == "N":
                                add_to_unsures(i, j)
                                board[i][j] = '.'
                                temp = True
                                any_changes = True

            print()
            print("Second stage:")
            Solver.print_board(board)



            indefinites = {
                'RD': RD,
                'LD': LD,
                'RU': RU,
                'LU': LU,
                'H': H,
                'V': V,
                '.': DOT,
                'N': NULL
            }
            
            ###### THIRD STAGE
            # for each empty square in the grid
            # if it is adjacent to 0 or 1 squares from 'indefinites', change it to 'X'

            temp = True
            while temp:
                temp = False
                for i in range(len(board)):
                    for j in range(len(board)):
                        if board[i][j] == "N":
                            count = 0
                            if i - 1 >= 0 and ((board[i-1][j] == "N") or (board[i-1][j] == V) or (board[i-1][j] == RD) or (board[i-1][j] == LD) or (board[i-1][j] == ".")):
                                count += 1
                            if i + 1 < len(board) and ((board[i+1][j] == "N") or (board[i+1][j] == V) or (board[i+1][j] == RU) or (board[i+1][j] == LU) or (board[i+1][j] == ".")):
                                count += 1
                            if j - 1 >= 0 and ((board[i][j-1] == "N") or (board[i][j-1] == H) or (board[i][j-1] == RD) or (board[i][j-1] == RU) or (board[i][j-1] == ".")):
                                count += 1
                            if j + 1 < len(board) and ((board[i][j+1] == "N") or (board[i][j+1] == H) or (board[i][j+1] == LD) or (board[i][j+1] == LU) or (board[i][j+1] == ".")):
                                count += 1
                            if count <= 1:
                                add_to_unsures(i, j)
                                board[i][j] = 'X'
                                temp = True
                                any_changes = True
            print("Third stage:")
            Solver.print_board(board)
            print()

            ###### STAGE 4

            # for each dot in the grid
            # if it is adjacent to 2 from 'characters', change it the character which fits the pattern
            temp = False
            while temp == False:
                temp = True
                for i in range(len(board)):
                    for j in range(len(board)):
                        if board[i][j] == '.':
                            directions = []
                            count = 0
                            if j - 1 >= 0 and ((board[i][j-1] == H) or (board[i][j-1] == RD) or (board[i][j-1] == RU)):
                                directions.append('left')
                                count += 1
                            if i - 1 >= 0 and ((board[i-1][j] == V) or (board[i-1][j] == RD) or (board[i-1][j] == LD)):
                                directions.append('up')
                                count += 1
                            if i + 1 < len(board) and ((board[i+1][j] == V) or (board[i+1][j] == RU) or (board[i+1][j] == LU)):
                                directions.append('down')
                                count += 1
                            if j + 1 < len(board) and ((board[i][j+1] == H) or (board[i][j+1] == LD) or (board[i][j+1] == LU)):
                                directions.append('right')
                                count += 1
                            
                            if count == 2:
                                add_to_unsures(i, j)
                                calc = findshape(directions[0], directions[1])
                                if calc == LU:
                                    board[i][j] = LU
                                elif calc == LD:
                                    board[i][j] = LD
                                elif calc == RU:
                                    board[i][j] = RU
                                elif calc == RD:
                                    board[i][j] = RD
                                elif calc == H:
                                    board[i][j] = H
                                elif calc == V:
                                    board[i][j] = V
                                any_changes = True
                                temp = False


            print()
            print("Fourth stage:")
            Solver.print_board(board)


            ##### STAGE 5
            # for each dot in the grid
            # if it is adjacent to exactly 2 from 'characters', change it the character which fits the pattern
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] == '.':
                        count = 0
                        directions = []
                        if j - 1 >= 0 and ((board[i][j-1] == H) or (board[i][j-1] == RD) or (board[i][j-1] == RU) or (board[i][j-1] == '.') or (board[i][j-1] == "N")):
                            count += 1
                            directions.append('left')
                        if j + 1 < len(board) and ((board[i][j+1] == H) or (board[i][j+1] == LD) or (board[i][j+1] == LU) or (board[i][j+1] == DOT) or (board[i][j+1] == "N")):
                            count += 1
                            directions.append('right')
                        if i - 1 >= 0 and ((board[i-1][j] == V) or (board[i-1][j] == RD) or (board[i-1][j] == LD) or (board[i-1][j] == '.') or (board[i-1][j] == "N")):
                            count += 1
                            directions.append('up')
                        if i + 1 < len(board) and ((board[i+1][j] == V) or (board[i+1][j] == RU) or (board[i+1][j] == LU) or (board[i+1][j] == '.') or (board[i+1][j] == "N")):
                            count += 1
                            directions.append('down')
                        #if there are exactly 2 characters adjacent to the dot
                        # draw the appropriate character
                        if count == 2:
                            add_to_unsures(i, j)
                            board[i][j] = findshape(directions[0], directions[1])
                            any_changes = True


                        def findloopinboard(a,b):
                            if board[a][b] == RD:
                                shapedir.append('right')
                                shapedir.append('down')
                            elif board[a][b] == RU:
                                shapedir.append('right')
                                shapedir.append('up')
                            elif board[a][b] == LD:
                                shapedir.append('left')
                                shapedir.append('down')
                            elif board[a][b] == LU:
                                shapedir.append('left')
                                shapedir.append('up')
                            elif board[a][b] == H:
                                shapedir.append('left')
                                shapedir.append('right')
                            elif board[a][b] == V:
                                shapedir.append('up')
                                shapedir.append('down')
                            return a,b

                        def editi1j1(a,b):
                            if shapedir[0] == 'left':
                                return a,b-1
                            if shapedir[0] == 'right':
                                return a,b+1
                            if shapedir[0] == 'up':
                                return a-1,b
                            if shapedir[0] == 'down':
                                return a+1,b

                        def removedirectionvisited(i2,j2):
                            if 'left' in shapedir:
                                i2 = i2
                                j2 = j2-1
                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                    shapedir.remove('left')
                                j2 = j2 + 1
                            if 'right' in shapedir:
                                i2 = i2
                                j2 = j2+1
                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                    shapedir.remove('right')
                                j2 = j2 - 1
                            if 'up' in shapedir:
                                i2 = i2-1
                                j2 = j2
                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                    shapedir.remove('up')
                                i2 = i2 + 1
                            if 'down' in shapedir:
                                i2 = i2+1
                                j2 = j2
                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                    shapedir.remove('down')
                                i2 = i2 - 1
                            
                        def removedirthree(i1,j1):
                            if outofrange == False and i == i1 and j+1 == j1 and change == True:
                                if 'right' in directions:
                                    directions.remove('right')
                            if outofrange == False and i+1 == i1 and j == j1 and change == True:
                                if 'down' in directions:
                                    directions.remove('down')
                            if outofrange == False and i-1 == i1 and j == j1 and change == True:
                                if 'up' in directions:
                                    directions.remove('up')
                            if outofrange == False and i == i1 and j-1 == j1 and change == True:
                                if 'left' in directions:
                                    directions.remove('left')
                            return i1,j1

                        if count == 3:
                            outofrange = False
                            change = False
                            if i - 1 >= 0:
                                if (board[i-1][j] == V) or (board[i-1][j] == RD) or (board[i-1][j] == LD):
                                    prevsquare = i,j
                                    i1 = i-1
                                    j1 = j
                                    outofrange = False                                    
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    while outofrange == False and board[i1][j1] in shapes.values():
                                        i2 = i1
                                        j2 = j1
                                        shapedir = []
                                        i1, j1 == findloopinboard(i1,j1)
                                        while len(shapedir) > 1:
                                            removedirectionvisited(i2,j2)
                                        if len(shapedir) == 1:
                                            change = True
                                            prevsquare = i1,j1
                                            i1,j1 = editi1j1(i1,j1)
                                        if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                            break

                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    if (outofrange == False) and (board[i1][j1] == '.'):
                                        if i1 == i and j1 == j:
                                            flagimpossible = True
                                    removedirthree(i1,j1)

                            if i + 1 < len(board):
                                if (board[i+1][j] == LU) or (board[i+1][j] == RU) or (board[i+1][j] == V):
                                    prevsquare = i,j
                                    i1 = i+1
                                    j1 = j
                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    while outofrange == False and board[i1][j1] in shapes.values():
                                        i2 = i1
                                        j2 = j1
                                        shapedir = []
                                        i1, j1 == findloopinboard(i1,j1)
                                        while len(shapedir) > 1:
                                            removedirectionvisited(i2,j2)
                                        if len(shapedir) == 1:
                                            change = True
                                            prevsquare = i1,j1
                                            i1,j1 = editi1j1(i1,j1)
                                        if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                            break
                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    if outofrange == False and board[i1][j1] == '.':
                                        if i1 == i and j1 == j:
                                            flagimpossible = True
                                    removedirthree(i1,j1)
                                
                            if j - 1 >= 0:
                                if (board[i][j-1] == RU) or (board[i][j-1] == RD) or (board[i][j-1] == H):
                                    prevsquare = i,j
                                    i1 = i
                                    j1 = j-1
                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    while outofrange == False and board[i1][j1] in shapes.values():
                                        i2 = i1
                                        j2 = j1
                                        shapedir = []
                                        i1, j1 == findloopinboard(i1,j1)
                                        while len(shapedir) > 1:
                                            removedirectionvisited(i2,j2)
                                        if len(shapedir) == 1:
                                            change = True
                                            prevsquare = i1,j1
                                            i1,j1 = editi1j1(i1,j1)
                                        if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                            break
                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    if outofrange == False and board[i1][j1] == '.':
                                        if i1 == i and j1 == j:
                                            flagimpossible = True
                                    removedirthree(i1,j1)
                            
                            if j + 1 < len(board):
                                if (board[i][j+1] == LU) or (board[i][j+1] == LD) or (board[i][j+1] == H):
                                    prevsquare = i,j
                                    i1 = i
                                    j1 = j+1
                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    while outofrange == False and board[i1][j1] in shapes.values():
                                        i2 = i1
                                        j2 = j1
                                        shapedir = []
                                        i1, j1 == findloopinboard(i1,j1)
                                        while len(shapedir) > 1:
                                            removedirectionvisited(i2,j2)
                                        if len(shapedir) == 1:
                                            change = True
                                            prevsquare = i1,j1
                                            i1,j1 = editi1j1(i1,j1)
                                        if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                            break
                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    if outofrange == False and board[i1][j1] == '.':
                                        if i1 == i and j1 == j:
                                            flagimpossible = True
                                    removedirthree(i1,j1)


                            if len(directions) == 2:
                                add_to_unsures(i, j)
                                board[i][j] = findshape(directions[0], directions[1])
                                any_changes = True
                                
            print()
            print("Fifth stage:")
            Solver.print_board(board)


            if bruteforceneeded == True:
                # if a dot is surrounded by 3 or 4 nodes that it cant go into, set impossible
                for i in range(len(board)):
                    for j in range(len(board)):
                        if board[i][j] == '.':
                            directions = []
                            if i - 1 >= 0:
                                if (board[i-1][j] == RU) or (board[i-1][j] == LU) or (board[i-1][j] == H) or (board[i-1][j] == 'X'):
                                    directions.append('up')
                            if i + 1 < len(board):
                                if (board[i+1][j] == RD) or (board[i+1][j] == LD) or (board[i+1][j] == H) or (board[i+1][j] == 'X'):
                                    directions.append('down')
                            if j - 1 >= 0:
                                if (board[i][j-1] == LU) or (board[i][j-1] == LD) or (board[i][j-1] == V) or (board[i][j-1] == 'X'):
                                    directions.append('left')
                            if j + 1 < len(board):
                                if (board[i][j+1] == RU) or (board[i][j+1] == RD) or (board[i][j+1] == V) or (board[i][j+1] == 'X'):
                                    directions.append('right')
                            if len(directions) >= 3:
                                flagimpossible = True


                # for each shape in grid
                # determine what directions the shape goes in
                # check if the shape in each direction is a compatible shape

                for i in range(len(board)):
                    for j in range(len(board)):
                        if board[i][j] in shapes.values():
                            shapedir = []
                            findloopinboard(i, j)
                            for direction in shapedir:
                                if direction == 'left' and j - 1 >= 0:
                                    if board[i][j-1] == V or board[i][j-1] == LU or board[i][j-1] == LD:
                                        flagimpossible = True
                                if direction == 'right' and j + 1 < len(board):
                                    if board[i][j+1] == V or board[i][j+1] == RU or board[i][j+1] == RD:
                                        flagimpossible = True
                                if direction == 'up' and i - 1 >= 0:
                                    if board[i-1][j] == H or board[i-1][j] == RU or board[i-1][j] == LU:
                                        flagimpossible = True
                                if direction == 'down' and i + 1 < len(board):
                                    if board[i+1][j] == H or board[i+1][j] == RD or board[i+1][j] == LD:
                                        flagimpossible = True

                #### for each dot in the grid
                # if the dot is surrounded by 3 'X's, flag as impossible

                for i in range(len(board)):
                    for j in range(len(board)):
                        if board[i][j] == ".":
                            count = 0
                            if i - 1 >= 0 and board[i-1][j] == "X":
                                count += 1
                            if i + 1 < len(board) and board[i+1][j] == "X":
                                count += 1
                            if j - 1 >= 0 and board[i][j-1] == "X":
                                count += 1
                            if j + 1 < len(board) and board[i][j+1] == "X":
                                count += 1
                            if count >= 3:
                                flagimpossible = True


                # for dot in grid
                # if the dot is surrounded by 3 shapes which go into it, flag as impossible
                for i in range(len(board)):
                    for j in range(len(board)):
                        if board[i][j] == ".":
                            count = 0
                            # if the shape to the left is a shape that goes right
                            if j - 1 >= 0 and board[i][j-1] in shapes.values():
                                if board[i][j-1] == H or board[i][j-1] == RD or board[i][j-1] == RU:
                                    count += 1
                            # if the shape to the right is a shape that goes left
                            if j + 1 < len(board) and board[i][j+1] in shapes.values():
                                if board[i][j+1] == H or board[i][j+1] == LD or board[i][j+1] == LU:
                                    count += 1
                            # if the shape above is a shape that goes down
                            if i - 1 >= 0 and board[i-1][j] in shapes.values():
                                if board[i-1][j] == V or board[i-1][j] == RD or board[i-1][j] == LD:
                                    count += 1
                            # if the shape below is a shape that goes up
                            if i + 1 < len(board) and board[i+1][j] in shapes.values():
                                if board[i+1][j] == V or board[i+1][j] == RU or board[i+1][j] == LU:
                                    count += 1
                            if count >= 3:
                                flagimpossible = True

            
            i,j = start
            previ,prevj = start
            iend,jend = end
            isashape = True
            fromstartcount = 1

            if j == 0 and board[i][j] != V:
                if board[i][j] == H:
                    j = j + 1
                    fromstartcount += 1
                elif board[i][j] == LU:
                    i = i - 1
                    fromstartcount += 1
                elif board[i][j] == LD:
                    i = i + 1
                    fromstartcount += 1

            elif j == len(board) - 1 and board[i][j] != V:
                if board[i][j] == H:
                    j = j - 1
                    fromstartcount += 1
                elif board[i][j] == RU:
                    i = i - 1
                    fromstartcount += 1
                elif board[i][j] == RD:
                    i = i + 1
                    fromstartcount += 1
            
            elif i == 0 and board[i][j] != H:
                if board[i][j] == V:
                    i = i + 1
                    fromstartcount += 1
                elif board[i][j] == RU:
                    j = j + 1
                    fromstartcount += 1
                elif board[i][j] == LU:
                    j = j - 1
                    fromstartcount += 1
            
            elif i == len(board) - 1 and board[i][j] != H:
                if board[i][j] == V:
                    i = i - 1
                    fromstartcount += 1
                elif board[i][j] == RD:
                    j = j + 1
                    fromstartcount += 1
                elif board[i][j] == LD:
                    j = j - 1
                    fromstartcount += 1

            if board[i][j] in shapes.values():
                isashape = True
            else:
                isashape = False

            while isashape == True and (iend != i or jend != j):
                isashape = False
                # if node is an H and prevnode was to the left
                # move right
                if board[i][j] == H and prevj < j:
                    previ = i
                    prevj = j
                    j = j + 1
                    fromstartcount += 1
                    isashape = True
                elif board[i][j] == H and prevj > j:
                    previ = i
                    prevj = j
                    j = j - 1
                    fromstartcount += 1
                    isashape = True
                #if node is a V and prevnode was above
                # move down
                elif board[i][j] == V and previ < i:
                    previ = i
                    prevj = j
                    i = i + 1
                    fromstartcount += 1
                    isashape = True
                elif board[i][j] == V and previ > i:
                    previ = i
                    prevj = j
                    i = i - 1
                    fromstartcount += 1
                    isashape = True

                #if node is a LU and prevnode was to the left
                # move up
                elif board[i][j] == LU and prevj < j:
                    previ = i
                    prevj = j
                    i = i - 1
                    fromstartcount += 1
                    isashape = True
                elif board[i][j] == LU and prevj == j:
                    previ = i
                    prevj = j
                    j = j - 1
                    fromstartcount += 1
                    isashape = True

                #if node is a LD and prevnode was to the left
                # move down
                elif board[i][j] == LD and prevj < j:
                    previ = i
                    prevj = j
                    i = i + 1
                    fromstartcount += 1
                    isashape = True
                elif board[i][j] == LD and prevj == j:
                    previ = i
                    prevj = j
                    j = j - 1
                    fromstartcount += 1
                    isashape = True

                #if node is a RU and prevnode was to the right
                # move up
                elif board[i][j] == RU and prevj > j:
                    previ = i
                    prevj = j
                    i = i - 1
                    fromstartcount += 1
                    isashape = True
                elif board[i][j] == RU and prevj == j:
                    previ = i
                    prevj = j
                    j = j + 1
                    fromstartcount += 1
                    isashape = True

                #if node is a RD and prevnode was to the right
                # move down
                elif board[i][j] == RD and prevj > j:
                    previ = i
                    prevj = j
                    i = i + 1
                    fromstartcount += 1
                    isashape = True
                elif board[i][j] == RD and prevj == j:
                    previ = i
                    prevj = j
                    j = j + 1
                    fromstartcount += 1
                    isashape = True

            if iend == i and jend == j:

                if fromstartcount != nodenumber:
                    flagimpossible = True
                else:
                    print("Solved succesfully")
                    Solver.print_board(board)
                    print()
                    # reset board to all "N"
                    # add board to editboard without changing board
                    editboard = [['N' for i in range(len(board))] for j in range(len(board))]
                    for i in range(len(startingshapes)):
                        editboard[startingshapes[i][0]][startingshapes[i][1]] = startingshapes[i][2]
                    Solver.print_board(board)

                    return board, editboard, column_totals, row_totals



            edgerulesneeded = False
            if any_changes == False:
                edgerulesneeded = True



            if edgerulesneeded == True:
                if column_totals[0] == len(board) - 1:
                    if (board[2][0] == H or board[2][0] == LD or board[2][0] == RD) and (board[0][0] == 'N'):
                        add_to_unsures(0, 0)
                        add_to_unsures(1,0)
                        board[0][0] = "."
                        board[1][0] = "."
                        any_changes = True
                    if ((board[len(board) - 3][0] == H) or (board[len(board) - 3][0] == LU) or (board[len(board) - 3][0] == RU)) and (board[len(board) - 1][0] == 'N'):
                        add_to_unsures(len(board) - 1, 0)
                        add_to_unsures(len(board) - 2, 0)
                        board[len(board) - 1][0] = "."
                        board[len(board) - 2][0] = "."
                        any_changes = True

                if column_totals[len(board) - 1] == len(board) - 1:
                    if (board[2][len(board) - 1] == H or board[2][len(board) - 1] == LD or board[2][len(board) - 1] == RD) and (board[0][len(board) - 1] == 'N'):
                        add_to_unsures(0, len(board) - 1)
                        add_to_unsures(1, len(board) - 1)
                        board[0][len(board) - 1] = "."
                        board[1][len(board) - 1] = "."
                        any_changes = True
                    if (board[len(board) - 3][len(board) - 1] == H or board[len(board) - 3][len(board) - 1] == LU or board[len(board) - 3][len(board) - 1] == RU) and (board[len(board) - 1][len(board) - 1] == 'N'):
                        add_to_unsures(len(board) - 1, len(board) - 1)
                        add_to_unsures(len(board) - 2, len(board) - 1)
                        board[len(board) - 1][len(board) - 1] = "."
                        board[len(board) - 2][len(board) - 1] = "."
                        any_changes = True

                if row_totals[0] == len(board) - 1:
                    if (board[0][2] == V or board[0][2] == RU or board[0][2] == RD) and (board[0][0] == 'N'):
                        add_to_unsures(0, 0)
                        add_to_unsures(0,1)
                        board[0][0] = "."
                        board[0][1] = "."
                        any_changes = True
                    if (board[0][len(board) - 3] == V or board[0][len(board) - 3] == LU or board[0][len(board) - 3] == LD) and (board[0][len(board) - 1] == 'N'):
                        add_to_unsures(0, len(board) - 1)
                        add_to_unsures(0, len(board) - 2)
                        board[0][len(board) - 1] = "."
                        board[0][len(board) - 2] = "."
                        any_changes = True

                if row_totals[len(board) - 1] == len(board) - 1:
                    if (board[len(board) - 1][2] == V or board[len(board) - 1][2] == RU or board[len(board) - 1][2] == RD) and (board[len(board) - 1][0] == 'N'):
                        add_to_unsures(len(board) - 1, 0)
                        add_to_unsures(len(board) - 1, 1)
                        board[len(board) - 1][0] = "."
                        board[len(board) - 1][1] = "."
                        any_changes = True
                    if (board[len(board) - 1][len(board) - 3] == V or board[len(board) - 1][len(board) - 3] == LU or board[len(board) - 1][len(board) - 3] == LD) and (board[len(board) - 1][len(board) - 1] == 'N'):
                        add_to_unsures(len(board) - 1, len(board) - 1)
                        add_to_unsures(len(board) - 1, len(board) - 2)
                        board[len(board) - 1][len(board) - 1] = "."
                        board[len(board) - 1][len(board) - 2] = "."
                        any_changes = True

                
                edgecolumns = []
                edgerows = []
                edgecolumns.append(-1)
                edgecolumns.append(len(board))
                edgerows.append(-1)
                edgerows.append(len(board))

                for j in range(len(board)):
                    count = 0
                    for i in range(len(board)):
                        if board[i][j] in knowns.values():
                            count += 1
                    if count == len(board):
                        edgecolumns.append(j)
                for i in range(len(board)):
                    count = 0
                    for j in range(len(board)):
                        if board[i][j] in knowns.values():
                            count += 1
                    if count == len(board):
                        edgerows.append(i)


                # for each column
                # if column to the left or right is in edgecolumns, check if the number of 'definites' in the column is equal to the column total - 1
                # if yes, for each square in the column which is 'N' and above or below a dot, add this coordinate to a list
                # if the length of list is 1, change the square to a dot, and change all other 'N's in the column to 'X'

                for j in range(len(board)):
                    if (j - 1 in edgecolumns) or (j + 1 in edgecolumns) and j not in edgecolumns:
                        count = 0
                        for i in range(len(board)):
                            if board[i][j] in definites.values():
                                count += 1
                        if count == column_totals[j] - 1:
                            dots = []
                            for i in range(len(board)):
                                if board[i][j] == "N":
                                    possible = False
                                    if i - 1 >= 0 and board[i-1][j] == ".":
                                        dots.append((i, j))
                                        possible = True
                                    if i + 1 < len(board) and board[i+1][j] == ".":
                                        dots.append((i, j))
                                        possible = True
                                    if possible == False:
                                        add_to_unsures(i, j)
                                        board[i][j] = "X"
                                        any_changes = True
                                    
                            if len(dots) == 1:
                                add_to_unsures(dots[0][0], dots[0][1])
                                board[dots[0][0]][dots[0][1]] = "."
                                any_changes = True
                                for i in range(len(board)):
                                    if board[i][j] == "N":
                                        add_to_unsures(i, j)
                                        board[i][j] = "X"
                                        any_changes = True
                # do the same for rows
                for i in range(len(board)):
                    if (i - 1 in edgerows) or (i + 1 in edgerows) and i not in edgerows:
                        count = 0
                        for j in range(len(board)):
                            if board[i][j] in definites.values():
                                count += 1
                        if count == row_totals[i] - 1:
                            dots = []
                            for j in range(len(board)):
                                if board[i][j] == "N":
                                    possible = False
                                    if j - 1 >= 0 and board[i][j-1] == ".": ###### add some shapes to the dot?
                                        dots.append((i, j))
                                        possible = True
                                    if j + 1 < len(board) and board[i][j+1] == ".":
                                        dots.append((i, j))
                                        possible = True
                                    if possible == False:
                                        add_to_unsures(i, j)
                                        board[i][j] = "X"
                                        any_changes = True
                                    
                            if len(dots) == 1:
                                add_to_unsures(dots[0][0], dots[0][1])
                                board[dots[0][0]][dots[0][1]] = "."
                                any_changes = True
                                for j in range(len(board)):
                                    if board[i][j] == "N":
                                        add_to_unsures(i, j)
                                        board[i][j] = "X"
                                        any_changes = True


                ###### edge rules part 2 ######
                # for each column
                # if column to the left is an edge
                # if column to the left has column total = 1
                # if column to the right has column total = 1
                # go to the node to the right of the node in left column
                # including this node, go down until nodes in column = column total
                # if any of these nodes are 'X', this direction is considered invalid
                # including this node, go up until nodes in column = column total
                # if any of these nodes are 'X', this direction is considered invalid
                # if one of the directions is valid, change all of these nodes to '.'

                #TRACE

                possible_down = False
                possible_up = False
                possibles = 0
                for j in range(len(board)):
                    if j - 1 in edgecolumns and j+1 < len(board) and j not in edgecolumns and j-1 >= 0:
                        if (column_totals[j-1] == 1 or column_totals[j-1] == 0) and column_totals[j+1] == 1:
                            for i in range(len(board)):
                                if (board[i][j-1] in shapes.values()):
                                    place = i
                                    counter = 1
                                    k = i
                                    while counter < column_totals[j]:
                                        if k > len(board):
                                            break
                                        if board[k][j] == "X":
                                            counter = -100
                                            break
                                        k += 1
                                        counter += 1
                                    if counter == column_totals[j] and k < len(board): ###changed
                                        possible_down = True
                                        possibles += 1
                                    counter = 1
                                    k = i
                                    while counter < column_totals[j]:
                                        if k < 0:
                                            break
                                        if board[k][j] == "X":
                                            break
                                        k -= 1
                                        counter += 1
                                    if counter == column_totals[j] and k >= 0: ###changed
                                        possible_up = True
                                        possibles += 1

                            if possibles == 1:
                                if possible_down == True:
                                    counter = 0
                                    k = place
                                    while counter < column_totals[j]:
                                        if board[k][j] in definites.values():
                                            counter += 1
                                        if board[k][j] == "N":
                                            add_to_unsures(k, j)
                                            board[k][j] = "."
                                            counter += 1
                                        k += 1
                                    any_changes = True
                                if possible_up == True:
                                    counter = 0
                                    k = place
                                    while counter < column_totals[j]:
                                        if board[k][j] in definites.values():
                                            counter += 1
                                        if board[k][j] == "N":
                                            add_to_unsures(k, j)
                                            board[k][j] = "."
                                            counter += 1
                                        k -= 1
                                    any_changes = True
                                                           
                # do the same for rows
                possiblementright = False
                possiblementleft = False
                possibles = 0
                for i in range(len(board)):
                    if i - 1 in edgerows and i+1 < len(board) and i-1 >= 0 and i not in edgerows:
                        if (row_totals[i-1] == 1 or row_totals[i-1] == 0) and row_totals[i+1] == 1:
                            for j in range(len(board)):
                                if (board[i-1][j] == H) or (board[i-1][j] == RD) or (board[i-1][j] == RU) or (board[i-1][j] == LD) or (board[i-1][j] == LU) or (board[i-1][j] == V):
                                    place = j
                                    counter = 1
                                    k = j
                                    while counter < row_totals[i]:
                                        if k > len(board):
                                            break
                                        if board[i][k] == "X":
                                            counter = -100
                                            break
                                        k += 1
                                        counter += 1
                                    if counter == row_totals[i] and k < len(board): ###changed
                                        possiblementright = True
                                        possibles += 1
                                    counter = 1
                                    k = j
                                    while counter < row_totals[i]:
                                        if k < 0:
                                            break
                                        if board[i][k] == "X":
                                            break
                                        k -= 1
                                        counter += 1
                                    if counter == row_totals[i] and k >= 0: ###changed
                                        possiblementleft = True
                                        possibles += 1

                            if possibles == 1:
                                if possiblementright == True:
                                    counter = 0
                                    k = place
                                    while counter < row_totals[i]:
                                        if board[i][k] in definites.values():
                                            counter += 1
                                        if board[i][k] == "N":
                                            add_to_unsures(i, k)
                                            board[i][k] = "."
                                            counter += 1
                                        k += 1
                                    any_changes = True
                                if possiblementleft == True:
                                    counter = 0
                                    k = place
                                    while counter < row_totals[i]:
                                        if board[i][k] in definites.values():
                                            counter += 1
                                        if board[i][k] == "N": ###outofrange
                                            add_to_unsures(i, k)
                                            board[i][k] = "."
                                            counter += 1
                                        k -= 1
                                    any_changes = True
                
                # do the same but swap left and right
                # for each column
                # if column to the right is an edge
                # if column to the right has column total = 1
                # if column to the left has column total = 1
                # go to the node to the left of the node in right column
                # including this node, go down until nodes in column = column total
                # if any of these nodes are 'X', this direction is considered invalid
                # including this node, go up until nodes in column = column total
                # if any of these nodes are 'X', this direction is considered invalid
                # if one of the directions is valid, change all of these nodes to '.'
                possible_down = False
                possible_up = False
                possibles = 0
                for j in range(len(board)):
                    if j + 1 in edgecolumns and j-1 >= 0 and j+1 < len(board) and j not in edgecolumns:
                        if (column_totals[j+1] == 1 or column_totals[j+1] == 0) and column_totals[j-1] == 1:
                            for i in range(len(board)):
                                if (board[i][j+1] in shapes.values()):
                                    place = i
                                    counter = 1
                                    k = i
                                    while counter < column_totals[j]:
                                        if k > len(board):
                                            break
                                        if board[k][j] == "X":
                                            counter = -100
                                            break
                                        k += 1
                                        counter += 1
                                    if counter == column_totals[j] and k < len(board):
                                        possible_down = True
                                        possibles += 1
                                    counter = 1
                                    k = i
                                    while counter < column_totals[j]:
                                        if k < 0:
                                            break
                                        if board[k][j] == "X":
                                            break
                                        k -= 1
                                        counter += 1
                                    if counter == column_totals[j] and k >= 0:
                                        possible_up = True
                                        possibles += 1

                            if possibles == 1:
                                if possible_down == True:
                                    counter = 0
                                    k = place
                                    while counter < column_totals[j]:
                                        if board[k][j] in definites.values():
                                            counter += 1
                                        if board[k][j] == "N":
                                            add_to_unsures(k, j)
                                            board[k][j] = "."
                                            counter += 1
                                        k += 1
                                    any_changes = True
                                if possible_up == True:
                                    counter = 0
                                    k = place
                                    while counter < column_totals[j]:
                                        if board[k][j] in definites.values():
                                            counter += 1
                                        if board[k][j] == "N":
                                            add_to_unsures(k, j)
                                            board[k][j] = "."
                                            counter += 1
                                        k -= 1
                                    any_changes = True
                
                # do the same for rows
                possiblementright = False
                possiblementleft = False
                possibles = 0
                for i in range(len(board)):
                    if i + 1 in edgerows and i-1 >= 0 and i + 1 < len(board) and i not in edgerows:
                        if (row_totals[i+1] == 1 or row_totals[i+1] == 0) and row_totals[i-1] == 1:
                            for j in range(len(board)):
                                if (board[i+1][j] == H) or (board[i+1][j] == RD) or (board[i+1][j] == RU) or (board[i+1][j] == LD) or (board[i+1][j] == LU) or (board[i+1][j] == V):
                                    place = j
                                    counter = 1
                                    k = j
                                    while counter < row_totals[i]:
                                        if k > len(board):
                                            break
                                        if board[i][k] == "X":
                                            counter = -100
                                            break
                                        k += 1
                                        counter += 1
                                    if counter == row_totals[i] and k < len(board):
                                        possiblementright = True
                                        possibles += 1
                                    counter = 1
                                    k = j
                                    while counter < row_totals[i]:
                                        if k < 0:
                                            break
                                        if board[i][k] == "X":
                                            break
                                        k -= 1
                                        counter += 1
                                    if counter == row_totals[i] and k >= 0:
                                        possiblementleft = True
                                        possibles += 1

                            if possibles == 1:
                                if possiblementright == True:
                                    counter = 0
                                    k = place
                                    while counter < row_totals[i]:
                                        if board[i][k] in definites.values():
                                            counter += 1
                                        if board[i][k] == "N":
                                            add_to_unsures(i, k)
                                            board[i][k] = "."
                                            counter += 1
                                        k += 1
                                    any_changes = True
                                if possiblementleft == True:
                                    counter = 0
                                    k = place
                                    while counter < row_totals[i]:
                                        if board[i][k] in definites.values():
                                            counter += 1
                                        if board[i][k] == "N":
                                            add_to_unsures(i, k)
                                            board[i][k] = "."
                                            counter += 1
                                        k -= 1
                                    any_changes = True
                
                print("Unique rule used")
                print()
                Solver.print_board(board)


                if column_totals[1] == 2:
                    if start[1] >= 2 and end[1] >= 2:
                        # count the number of dots in the column
                        count = 0
                        for i in range(len(board)):
                            if board[i][1] == ".":
                                count += 1
                        # if the number of dots is 2, make them both Hs
                        if count == 2:
                            for i in range(len(board)):
                                if board[i][1] == ".":
                                    add_to_unsures(i, 1)
                                    board[i][1] = H
                                    any_changes = True
                        # if the number of dots is 1, make the the dot an H
                        if count == 1:
                            for i in range(len(board)):
                                if board[i][1] == ".":
                                    add_to_unsures(i, 1)
                                    board[i][1] = H
                                    any_changes = True
                                    temp = column_totals[0] - 1
                                    for k in range(len(board)):
                                        if board[k][1] == "N":
                                            if (k != i - temp) and (k != i + temp):
                                                add_to_unsures(k, 1)
                                                board[k][1] = "X"

                        if count == 0:
                            # count the number of Hs in the column
                            for i in range(len(board)):
                                if board[i][1] == H:
                                    count += 1
                                    ivalue = i
                            # if the number of Hs is 1
                            if count == 1:
                                temp = column_totals[0] - 1
                                for k in range(len(board)):
                                    if board[k][1] == "N":
                                        if (k != ivalue - temp) and (k != ivalue + temp):
                                            add_to_unsures(k, 1)
                                            board[k][1] = "X"
                                            any_changes = True

                if column_totals[len(board) - 2] == 2:
                    if start[1] <= len(board) - 3 and end[1] <= len(board) - 3:
                        count = 0
                        for i in range(len(board)):
                            if board[i][len(board) - 2] == ".":
                                count += 1
                        if count == 2:
                            for i in range(len(board)):
                                if board[i][len(board) - 2] == ".":
                                    add_to_unsures(i, len(board) - 2)
                                    board[i][len(board) - 2] = H
                                    any_changes = True
                        if count == 1:
                            for i in range(len(board)):
                                if board[i][len(board) - 2] == ".":
                                    add_to_unsures(i, len(board) - 2)
                                    board[i][len(board) - 2] = H
                                    any_changes = True
                                    temp = column_totals[len(board) - 1] - 1
                                    for k in range(len(board)):
                                        if board[k][len(board) - 2] == "N":
                                            if (k != i - temp) and (k != i + temp):
                                                add_to_unsures(k, len(board) - 2)
                                                board[k][len(board) - 2] = "X"

                        if count == 0:
                            for i in range(len(board)):
                                if board[i][len(board) - 2] == H:
                                    count += 1
                                    ivalue = i
                            if count == 1:
                                temp = column_totals[len(board) - 1] - 1
                                for k in range(len(board)):
                                    if board[k][len(board) - 2] == "N":
                                        if (k != ivalue - temp) and (k != ivalue + temp):
                                            add_to_unsures(k, len(board) - 2)
                                            board[k][len(board) - 2] = "X"
                                            any_changes = True

                if row_totals[1] == 2:
                    if start[0] >= 2 and end[0] >= 2:
                        count = 0
                        for j in range(len(board)):
                            if board[1][j] == ".":
                                count += 1
                        if count == 2:
                            for j in range(len(board)):
                                if board[1][j] == ".":
                                    add_to_unsures(1, j)
                                    board[1][j] = V
                                    any_changes = True
                        if count == 1:
                            for j in range(len(board)):
                                if board[1][j] == ".":
                                    add_to_unsures(1, j)
                                    board[1][j] = V
                                    any_changes = True
                                    temp = row_totals[0] - 1
                                    for k in range(len(board)):
                                        if board[1][k] == "N":
                                            if (k != j - temp) and (k != j + temp):
                                                add_to_unsures(1, k)
                                                board[1][k] = "X"

                        if count == 0:
                            for j in range(len(board)):
                                if board[1][j] == V:
                                    count += 1
                                    jvalue = j
                            if count == 1:
                                temp = row_totals[0] - 1
                                for k in range(len(board)):
                                    if board[1][k] == "N":
                                        if (k != jvalue - temp) and (k != jvalue + temp):
                                            add_to_unsures(1, k)
                                            board[1][k] = "X"
                                            any_changes = True
                
                if row_totals[len(board) - 2] == 2:
                    if start[0] <= len(board) - 3 and end[0] <= len(board) - 3:
                        count = 0
                        for j in range(len(board)):
                            if board[len(board) - 2][j] == ".":
                                count += 1
                        if count == 2:
                            for j in range(len(board)):
                                if board[len(board) - 2][j] == ".":
                                    add_to_unsures(len(board) - 2, j)
                                    board[len(board) - 2][j] = V
                                    any_changes = True
                        if count == 1:
                            for j in range(len(board)):
                                if board[len(board) - 2][j] == ".":
                                    add_to_unsures(len(board) - 2, j)
                                    board[len(board) - 2][j] = V
                                    any_changes = True
                                    temp = row_totals[len(board) - 1] - 1
                                    for k in range(len(board)):
                                        if board[len(board) - 2][k] == "N":
                                            if (k != j - temp) and (k != j + temp):
                                                add_to_unsures(len(board) - 2, k)
                                                board[len(board) - 2][k] = "X"
                    
                        if count == 0:
                            for j in range(len(board)):
                                if board[len(board) - 2][j] == V:
                                    count += 1
                                    jvalue = j
                            if count == 1:
                                temp = row_totals[len(board) - 1] - 1
                                for k in range(len(board)):
                                    if board[len(board) - 2][k] == "N":
                                        if (k != jvalue - temp) and (k != jvalue + temp):
                                            add_to_unsures(len(board) - 2, k)
                                            board[len(board) - 2][k] = "X"
                                            any_changes = True


                #for each column which has column total = 1
                # for each node in the column
                # if the node to the left is an X, LU,LD,V or the node to the right is an X, RU, RD, V
                # make the node an X
                for j in range(len(board)):
                    if column_totals[j] == 1 and j not in edgecolumns:
                        for i in range(len(board)):
                            if j - 1 >= 0 and (board[i][j-1] == "X" or board[i][j-1] == LU or board[i][j-1] == LD or board[i][j-1] == V):
                                add_to_unsures(i, j)
                                if board[i][j] != "X":
                                    any_changes = True
                                board[i][j] = "X"
                            if j + 1 < len(board) and (board[i][j+1] == "X" or board[i][j+1] == RU or board[i][j+1] == RD or board[i][j+1] == V):
                                add_to_unsures(i, j)
                                if board[i][j] != "X":
                                    any_changes = True
                                board[i][j] = "X"

                # do the same for rows
                for i in range(len(board)):
                    if row_totals[i] == 1 and i not in edgerows:
                        for j in range(len(board)):
                            if i - 1 >= 0 and (board[i-1][j] == "X" or board[i-1][j] == LU or board[i-1][j] == RU or board[i-1][j] == H):
                                add_to_unsures(i, j)
                                if board[i][j] != "X":
                                    any_changes = True
                                board[i][j] = "X"
                            if i + 1 < len(board) and (board[i+1][j] == "X" or board[i+1][j] == LD or board[i+1][j] == RD or board[i+1][j] == H):
                                add_to_unsures(i, j)
                                if board[i][j] != "X":
                                    any_changes = True
                                board[i][j] = "X"


                if len(board) >= 5:
                    count = 0
                    for j in range(len(board)):
                        if board[0][j] in definites.values():
                            count += 1
                    if row_totals[0] == count + 1:
                        if board[0][len(board) - 4] in [V, LD, LU] and board[0][len(board) - 2] == "." and board[0][len(board) - 3] == 'N' and board[0][len(board) - 1] == 'N':
                            for i in range(0,len(board)-4):
                                if board[0][i] == 'N':
                                    add_to_unsures(0, i)
                                    if board[0][i] != "X":
                                        any_changes = True
                                    board[0][i] = "X"
                        if board[0][3] in [V, RD, RU] and board[0][1] == "." and board[0][2] == 'N' and board[0][0] == 'N':
                            for i in range(5, len(board)):
                                if board[0][i] == 'N':
                                    add_to_unsures(0, i)
                                    if board[0][i] != "X":
                                        any_changes = True
                                    board[0][i] = "X"

                    count = 0
                    for i in range(len(board)):
                        if board[i][0] in definites.values():
                            count += 1
                    if column_totals[0] == count + 1:
                        if board[len(board) - 4][0] in [H, RU, LU] and board[len(board) - 2][0] == "." and board[len(board) - 3][0] == 'N' and board[len(board) - 1][0] == 'N':
                            for i in range(0,len(board)-4):
                                if board[i][0] == 'N':
                                    add_to_unsures(i, 0)
                                    if board[i][0] != "X":
                                        any_changes = True
                                    board[i][0] = "X"
                        if board[3][0] in [H, RD, LD] and board[1][0] == "." and board[2][0] == 'N' and board[0][0] == 'N':
                            for i in range(5, len(board)):
                                if board[i][0] == 'N':
                                    add_to_unsures(i, 0)
                                    if board[i][0] != "X":
                                        any_changes = True
                                    board[i][0] = "X"

                    count = 0
                    for j in range(len(board)):
                        if board[len(board) - 1][j] in definites.values():
                            count += 1
                    if row_totals[len(board) - 1] == count + 1:
                        if board[len(board) - 1][len(board) - 4] in [V, LD, LU] and board[len(board) - 1][len(board) - 2] == "." and board[len(board) - 1][len(board) - 3] == 'N' and board[len(board) - 1][len(board) - 1] == 'N':
                            for i in range(0,len(board)-4):
                                if board[len(board) - 1][i] == 'N':
                                    add_to_unsures(len(board) - 1, i)
                                    if board[len(board) - 1][i] != "X":
                                        any_changes = True
                                    board[len(board) - 1][i] = "X"
                        if board[len(board) - 1][3] in [V, RD, RU] and board[len(board) - 1][1] == "." and board[len(board) - 1][2] == 'N' and board[len(board) - 1][0] == 'N':
                            for i in range(5, len(board)):
                                if board[len(board) - 1][i] == 'N':
                                    add_to_unsures(len(board) - 1, i)
                                    if board[len(board) - 1][i] != "X":
                                        any_changes = True
                                    board[len(board) - 1][i] = "X"

                    count = 0
                    for i in range(len(board)):
                        if board[i][len(board) - 1] in definites.values():
                            count += 1
                    if column_totals[len(board) - 1] == count + 1:
                        if board[len(board) - 4][len(board) - 1] in [H, RU, LU] and board[len(board) - 2][len(board) - 1] == "." and board[len(board) - 3][len(board) - 1] == 'N' and board[len(board) - 1][len(board) - 1] == 'N':
                            for i in range(0,len(board)-4):
                                if board[i][len(board) - 1] == 'N':
                                    add_to_unsures(i, len(board) - 1)
                                    if board[i][len(board) - 1] != "X":
                                        any_changes = True
                                    board[i][len(board) - 1] = "X"
                        if board[3][len(board) - 1] in [H, RD, LD] and board[1][len(board) - 1] == "." and board[2][len(board) - 1] == 'N' and board[0][len(board) - 1] == 'N':
                            for i in range(5, len(board)):
                                if board[i][len(board) - 1] == 'N':
                                    add_to_unsures(i, len(board) - 1)
                                    if board[i][len(board) - 1] != "X":
                                        any_changes = True
                                    board[i][len(board) - 1] = "X"



            if flagimpossible == True:
                trynew = True

            edgerulesneeded = False
            if any_changes == False:
                print("No changes made, entering guessing stage")
                bruteforceneeded = True

            if (bruteforceneeded == True and any_changes == False and generation != "y") or trynew == True:
                stuck = False
                print("Brute force needed")
                # Add all unsures back to board (in reverse order to ensure board is changed to original state)
                unsures = unsures[::-1]
                for unsure in unsures:
                    board[unsure[0]][unsure[1]] = unsure[2]
                unsures = []
                if trynew == True:
                    if trysecond == False:
                        if len(unsureshapes) == 1:
                            unsureshapes.pop(0)
                        else:
                            stuck = True
                    else:
                        if len(unsureshapes) == 1:
                            unsureshapes.pop(1)
                        else:
                            stuck = True
                    trysecond = False
                if len(unsureshapes) == 1:
                    # make the board square of save_state the shape in unsureshapes
                    board[save_state[0]][save_state[1]] = unsureshapes
                    unsureshapes.pop(0)
                    trynew = False
                    any_changes = True
                    bruteforceneeded = False
                    changecheck = True
                if len(unsureshapes) == 2:
                    if trysecond == False:
                        trysecond = True
                        any_changes = True
                    else:
                        board[save_state[0]][save_state[1]] = save_state[2]
                        trysecond = False
                if trysecond == True:
                    board[nodeguess[0]][nodeguess[1]] = nodeguess[3]

                # for dot in board
                # find the number of possible shapes that can go in the dot
                # if only one possible shape, change the dot to that shape
                # if two possible shapes, add a tuple to 'dots_two' in the form (i, j, shape1, shape2)
                
                if changecheck == True and trysecond == False and any_changes == False:
                    changecheck = False
                    for i in range(len(board)):
                        for j in range(len(board)):
                            if board[i][j] == ".":
                                possible = []
                                ### for each dot that connects to a shape
                                # for example if the shape at [i][j-1] is H, RD, RU, check the other three directions to see if any are dots or 'N's
                                # if they are add the corresponding shapes to 'possible'
                                if j - 1 >= 0 and (board[i][j-1] == H or board[i][j-1] == RD or board[i][j-1] == RU):
                                    if j + 1 < len(board) and (board[i][j+1] == "." or board[i][j+1] == "N"):
                                        possible.append(H)
                                    if i - 1 >= 0 and (board[i-1][j] == "." or board[i-1][j] == "N"):
                                        possible.append(LU)
                                    if i + 1 < len(board) and (board[i+1][j] == "." or board[i+1][j] == "N"):
                                        possible.append(LD)

                                if j + 1 < len(board) and (board[i][j+1] == H or board[i][j+1] == LD or board[i][j+1] == LU):
                                    if j - 1 >= 0 and (board[i][j-1] == "." or board[i][j-1] == "N"):
                                        possible.append(H)
                                    if i - 1 >= 0 and (board[i-1][j] == "." or board[i-1][j] == "N"):
                                        possible.append(RU)
                                    if i + 1 < len(board) and (board[i+1][j] == "." or board[i+1][j] == "N"):
                                        possible.append(RD)
                                
                                if i - 1 >= 0 and (board[i-1][j] == V or board[i-1][j] == RD or board[i-1][j] == LD):
                                    if i + 1 < len(board) and (board[i+1][j] == "." or board[i+1][j] == "N"):
                                        possible.append(V)
                                    if j - 1 >= 0 and (board[i][j-1] == "." or board[i][j-1] == "N"):
                                        possible.append(LU)
                                    if j + 1 < len(board) and (board[i][j+1] == "." or board[i][j+1] == "N"):
                                        possible.append(RU)

                                if i + 1 < len(board) and (board[i+1][j] == V or board[i+1][j] == RU or board[i+1][j] == LU):
                                    if i - 1 >= 0 and (board[i-1][j] == "." or board[i-1][j] == "N"):
                                        possible.append(V)
                                    if j - 1 >= 0 and (board[i][j-1] == "." or board[i][j-1] == "N"):
                                        possible.append(LD)
                                    if j + 1 < len(board) and (board[i][j+1] == "." or board[i][j+1] == "N"):
                                        possible.append(RD)

                                if len(possible) == 1:
                                    board[i][j] = possible[0]
                                    any_changes = True

                                if len(possible) == 3:
                                    # if column total = 2 and dots in column = 1 and number of dots + Ns in column = 3
                                    # if the start node is to the left of the column and end node is to the right of the column
                                    # if H is in possible
                                    # remove H from possible

                                    if column_totals[j] == 2 and sum([1 for i in range(len(board)) if board[i][j] == "."]) == 1 and sum([1 for i in range(len(board)) if board[i][j] == "." or board[i][j] == "N"]) == 3 and sum([1 for i in range(len(board)) if board[i][j] in shapes.values()]) == 0:
                                        if start[1] < j and end[1] > j:
                                            if H in possible:
                                                possible.remove(H)
                                        if start[1] > j and end[1] < j:
                                            if H in possible:
                                                possible.remove(H)

                                    if len(possible) == 3:
                                        # if column total - number of shapes in column = 2 and number of dots in column = 1
                                        # if the dot is not next to a shape going into it
                                        # try H
                                        # if H causes all Ns in the row to be Xs, remove H from possible

                                        if column_totals[j] - sum([1 for i in range(len(board)) if board[i][j] in shapes.values()]) == 2 and sum([1 for i in range(len(board)) if board[i][j] == "."]) == 1:
                                            if i - 1 >= 0 and board[i-1][j] not in shapes.values():
                                                if i + 1 < len(board) and board[i+1][j] not in shapes.values():
                                                    # use the fourth stage from earlier to see if both i+1 and i-1 are Xs
                                                    board[i][j] = H
                                                    isimpossible = False
                                                    for k in range(len(board)):
                                                        if board[k][j] == "N":
                                                            count = 0
                                                            # if the node to the left is a shape that goes right
                                                            if j - 1 >= 0:
                                                                if board[k][j-1] == H or board[k][j-1] == RD or board[k][j-1] == RU or board[k][j-1] == '.' or board[k][j-1] == 'N':
                                                                    count += 1
                                                            # if the node to the right is a shape that goes left
                                                            if j + 1 < len(board):
                                                                if board[k][j+1] == H or board[k][j+1] == LD or board[k][j+1] == LU or board[k][j+1] == '.' or board[k][j+1] == 'N':
                                                                    count += 1
                                                            # if the node above is a shape that goes down
                                                            if k - 1 >= 0:
                                                                if board[k-1][j] == V or board[k-1][j] == RD or board[k-1][j] == LD or board[k-1][j] == '.' or board[k-1][j] == 'N':
                                                                    count += 1
                                                            # if the node below is a shape that goes up
                                                            if k + 1 < len(board):
                                                                if board[k+1][j] == V or board[k+1][j] == RU or board[k+1][j] == LU or board[k+1][j] == '.' or board[k+1][j] == 'N':
                                                                    count += 1
                                                            if count <= 1:
                                                                isimpossible = True
                                                    if isimpossible == True:
                                                        if H in possible:
                                                            possible.remove(H)
                                                        isimpossible = False
                                                    board[i][j] = "."

                                        # if row total - number of shapes in row = 2 and number of dots in row = 1
                                        # if the dot is not next to a shape going into it
                                        # try V
                                        # if V causes all Ns in the column to be Xs, remove V from possible

                                        if row_totals[i] - sum([1 for j in range(len(board)) if board[i][j] in shapes.values()]) == 2 and sum([1 for j in range(len(board)) if board[i][j] == "."]) == 1:
                                            if j - 1 >= 0 and board[i][j-1] not in shapes.values():
                                                if j + 1 < len(board) and board[i][j+1] not in shapes.values():
                                                    board[i][j] = V
                                                    isimpossible = False
                                                    for k in range(len(board)):
                                                        if board[i][k] == "N":
                                                            count = 0
                                                            # if the node to the left is a shape that goes right
                                                            if k - 1 >= 0:
                                                                if board[i][k-1] == H or board[i][k-1] == RD or board[i][k-1] == RU or board[i][k-1] == '.' or board[i][k-1] == 'N':
                                                                    count += 1
                                                            # if the node to the right is a shape that goes left
                                                            if k + 1 < len(board):
                                                                if board[i][k+1] == H or board[i][k+1] == LD or board[i][k+1] == LU or board[i][k+1] == '.' or board[i][k+1] == 'N':
                                                                    count += 1
                                                            # if the node above is a shape that goes down
                                                            if i - 1 >= 0:
                                                                if board[i-1][k] == V or board[i-1][k] == RD or board[i-1][k] == LD or board[i-1][k] == '.' or board[i-1][k] == 'N':
                                                                    count += 1
                                                            # if the node below is a shape that goes up
                                                            if i + 1 < len(board):
                                                                if board[i+1][k] == V or board[i+1][k] == RU or board[i+1][k] == LU or board[i+1][k] == '.' or board[i+1][k] == 'N':
                                                                    count += 1
                                                            if count <= 1:
                                                                isimpossible = True
                                                    if isimpossible == True:
                                                        if V in possible:
                                                            possible.remove(V)
                                                        isimpossible = False
                                                    board[i][j] = "."

                                if len(possible) == 2:
                                    #if not already in dots_two, add to dots_two
                                    if (i, j, possible[0], possible[1]) not in dots_two:
                                        dots_two.append((i, j, possible[0], possible[1]))


                if any_changes == False and len(dots_two) > 0:
                    unsureshapes = []
                    # nodeguess = first node in dots_two
                    # change the board position designated by the first and second parts of nodeguess to the first shape in the third part of nodeguess
                    # add both shapes to 'unsureshapes'
                    # save old state of board square to save_state
                    # save state includes the coordinates of the node, and the shape of the node
                    save_state = [dots_two[0][0], dots_two[0][1], board[dots_two[0][0]][dots_two[0][1]]]
                    nodeguess = dots_two[0]
                    board[nodeguess[0]][nodeguess[1]] = nodeguess[2]
                    unsureshapes.append(nodeguess[2])
                    unsureshapes.append(nodeguess[3])
                    dots_two.pop(0)
                    any_changes = True


                if (any_changes == False and len(dots_two) == 0) or stuck == True:
                    stuck = False
                    print("This is how far this program was able to get")
                    print("It is possible that you made a mistake in your input")
                    print()
                    Solver.print_board(board)
                    print("type y if you would like to aid the program in solving the puzzle, n if you would like to quit")
                    generation = input()
                    while generation not in ["y", "n", "Y", "N"]:
                        print("Invalid input")
                        print("Enter a valid input, considering the options above")
                        generation = input()
                    if generation.upper() == "N":
                        quit()
                    if generation.upper() == "Y":
                        print()
                        Solver.print_board(board)
                        rowcol = input("Enter row and column in the form row, column: ")
                        while not (len(rowcol) == 3) and not (rowcol[1] == ",") and not (rowcol[0].isdigit()) and not (rowcol[2].isdigit()):
                            print("Invalid input")
                            print("Enter a valid input, considering the options above")
                            rowcol = input()
                        row = int(rowcol[0])
                        col = int(rowcol[2])
                        print(f"Enter the shape you would like to add to the board at node {row},{col}")
                        print("Enter shape: H, V, RD, LD, RU, LU, N, X,.")
                        shape = input()
                        while shape not in {"H", "V", "RD", "LD", "RU", "LU", "N", "X", "."}:
                            print("Invalid input")
                            print("Enter a valid input, considering the options above")
                            shape = input()
                        board[row][col] = shape
                        any_changes = True


            if any_changes == False and generation == "y":
                Solver.print_board(board)
                print("adding hint")
                # add all nodes with a shape in SAVEDBOARD but not in board to possibleadditions
                possibleadditions = []
                for i in range(len(board)):
                    for j in range(len(board)):
                        if SAVEDBOARD[i][j] in shapes.values():
                            if board[i][j] not in shapes.values():
                                possibleadditions.append((i, j, SAVEDBOARD[i][j]))
                # chose a random shape from possibleadditions, add shape to board and to startingshapes
                if len(possibleadditions) > 0:
                    chosen = random.choice(possibleadditions)
                    board[chosen[0]][chosen[1]] = chosen[2]
                    startingshapes.append(chosen)
                    Solver.print_board(board)
                    print("added a shape")
                any_changes = True


class EditBoard:
    def print_board(board):
        for row in board:
            print(' '.join(map(str, row)))

    def manual_edit(board,editboard, column_totals, row_totals):
        timeshow = False
        percshow = False
        hintson = False
        solutionon = False
        with open("account.csv", "r") as f:
            accdata = f.readline()
            accdata = accdata.split(",")
        f.close()
        if accdata[1] == "1":
            timeshow = True
        if accdata[2] == "1":
            percshow = True
        if accdata[3] == "1":
            hintson = True
        if accdata[4] == "1":
            solutionon = True
        RD = "┌"
        LD = "┐"
        RU = "└"
        LU = "┘"
        H = "─"
        V = "│"
        DOT = "."
        X = "X"
        N = "N"
        changenode = {
        RD: "RD",
        LD: "LD",
        RU: "RU",
        LU: "LU",
        H: "H",
        V: "V",
        DOT: ".",
        X: "X",
        N: "N"
        }
        shapes = {
        "RD": RD,
        "LD": LD,
        "RU": RU,
        "LU": LU,
        "H": H,
        "V": V
        }
        displayboard = []
        displayboard = [['N' for i in range(len(board)+ 1)] for j in range(len(board)+1)]
        displayboard[0][0] = "#"
        for i in range(1,len(board)+1):
            displayboard[0][i] = column_totals[i-1]
        for i in range(1,len(board)+1):
            displayboard[i][0] = row_totals[i-1]
        for i in range(1,len(board)+1):
            if displayboard[0][i] == 10:
                displayboard[0][i] = "M"
        for i in range(1,len(board)+1):
            if displayboard[i][0] == 10:
                displayboard[i][0] = "M"
        # add editboard to the bottom right of displayboard
        for i in range(0,len(board)):
            for j in range(0,len(board)):
                displayboard[i+1][j+1] = editboard[i][j]
        print()
        Solver.print_board(displayboard)
        undostack = []
        time = datetime.datetime.now()
        time4 = None
        while True:
            print()
            print("Edit the board: ")
            print()
            Solver.print_board(displayboard)
            print()
            print("Enter row and column in the form row, column")
            print("Or enter u to undo last move, p to pause, q to quit, SAVE to save the board")
            if hintson == True and solutionon == True:
                print("Enter h for a hint, Enter s to see the solution. Only use if you are truly stuck")
            elif hintson == True and solutionon == False:
                print("Enter h for a hint. Only use if you are truly stuck")
            elif hintson == False and solutionon == True:
                print("Enter s to see the solution. Only use if you are truly stuck")
            rowcol = input()
            while rowcol not in ["u", "h", "s", "p", "q", "save", "U", "H", "S", "P", "Q", "SAVE"] and not (len(rowcol) == 3):
                print("Invalid input")
                print("Enter a valid input, considering the options above")
                rowcol = input()
            if rowcol.upper() == "P":
                # start a second timer, which will be subtracted from the first timer upon completion
                time4 = datetime.datetime.now()
                print("Game paused")
                for i in range(50):
                    print()
                restart = ""
                while restart not in ["r", "q", "R", "Q", "m", "M"]:
                    restart = input("Enter r to resume, m to return to main menu or q to quit: ")
                if restart.upper() == "R":
                    # subtract the time taken from the first timer
                    time3 = datetime.datetime.now()
                    time4 = time3 - time4
                    print("Game resumed")
                if restart.upper() == "Q":
                    print("Game quit")
                    quit()
                if restart.upper() == "M":
                    print("Returning to main menu")
                    MainMenu()
            elif rowcol.upper() == "Q":
                print("Game quit")
                quit()
            elif rowcol.upper() == "U":
                if len(undostack) > 0:
                    last = undostack.pop()
                    displayboard[last[0] + 1][last[1] + 1] = last[2]
                else:
                    print("No moves to undo")
            elif rowcol.upper() == "S":
                if solutionon == True:
                    print("Solution: ")
                    Solver.print_board(board)
                else:
                    print("Solutions are disabled")
            elif rowcol.upper() == "H":
                if hintson == True:
                    print("Hints are enabled")
                    print("Providing hint")
                    possibleadditions = []
                    for i in range(len(board)):
                        for j in range(len(board)):
                            if board[i][j] in shapes.values():
                                if displayboard[i+1][j+1] not in shapes.values():
                                    possibleadditions.append((i, j, board[i][j]))
                    chosen = random.choice(possibleadditions)
                    undostack.append((chosen[0], chosen[1], chosen[2]))
                    displayboard[chosen[0] + 1][chosen[1] + 1] = chosen[2]
                else:
                    print("Hints are disabled")
            elif rowcol.upper() == "SAVE":
                data = board, editboard, column_totals, row_totals
                filename = input("Enter the new name of the file you want to save the board to (dont include file type) ")
                filename = filename + ".pkl"
                files = find_pkl_files()
                if filename in files:
                    print("File already exists")
                else:
                    with open(filename, "wb") as f:
                        pickle.dump(data, f)
                    f.close()
                    print("Board saved")
                    quitoption = input("Enter q to quit, or any other key to continue: ")
                    if quitoption == "q":
                        quit()
            else:
                if any([char not in "0123456789," for char in rowcol]):
                    print("Invalid input")
                if rowcol.count(",") != 1 or rowcol[0] == "," or rowcol[-1] == ",":
                    print("Invalid input")
                else:
                    rowcol = rowcol.split(",")
                    row = int(rowcol[0]) + 1
                    col = int(rowcol[1]) + 1
                    if row < 1 or row > len(board) or col < 1 or col > len(board):
                        print("Invalid input")
                        continue
                    shape = input("Enter shape, dot, N or X: ")
                    if shape in changenode.values():
                        if shape == "V":
                            undostack.append((row - 1, col - 1, displayboard[row][col]))
                            displayboard[row][col] = V
                        elif shape == "H":
                            undostack.append((row - 1, col - 1, displayboard[row][col]))
                            displayboard[row][col] = H
                        elif shape == "RD":
                            undostack.append((row - 1, col - 1, displayboard[row][col]))
                            displayboard[row][col] = RD
                        elif shape == "RU":
                            undostack.append((row - 1, col - 1, displayboard[row][col]))
                            displayboard[row][col] = RU
                        elif shape == "LD":
                            undostack.append((row - 1, col - 1, displayboard[row][col]))
                            displayboard[row][col] = LD
                        elif shape == "LU":
                            undostack.append((row - 1, col - 1, displayboard[row][col]))
                            displayboard[row][col] = LU
                        elif shape == ".":
                            undostack.append((row - 1, col - 1, displayboard[row][col]))
                            displayboard[row][col] = DOT
                        elif shape == "X":
                            undostack.append((row - 1, col - 1, displayboard[row][col]))
                            displayboard[row][col] = X
                        elif shape == "N":
                            undostack.append((row - 1, col - 1, displayboard[row][col]))
                            displayboard[row][col] = N
                        Solver.print_board(displayboard)
                        print()
            if timeshow == True:
                temp = datetime.datetime.now()
                temp = temp - time
                print("Time taken so far in seconds: ", temp.seconds)
            if percshow == True:
                print("Percentage complete: ", round(sum([1 for i in range(len(board)) for j in range(len(board)) if displayboard[i+1][j+1] in shapes.values()]) / sum([1 for i in range(len(board)) for j in range(len(board)) if board[i][j] in shapes.values()]) * 100, 3), "%")
            success = True
            for i in range(len(board)):
                if success == False:
                    break
                for j in range(len(board)):
                    if board[i][j] != displayboard[i+1][j+1] and board[i][j] != "N" and board[i][j] != "X":
                        success = False
                        break
            if success == True:
                for i in range(len(board)):
                    if success == False:
                        break
                    else:
                        for j in range(len(board)):
                            if displayboard[i+1][j+1] == ".":
                                success = False
                                break
            if success == True:
                # if the number of shapes in the board != sum of column totals, success = False
                for i in range(len(board)):
                    if success == False:
                        break
                    count = 0
                    for j in range(len(board)):
                        if displayboard[j+1][i+1] in shapes.values():
                            count += 1
                    if count != column_totals[i]:
                        success = False
            if success == True:
                time2 = datetime.datetime.now()
                time = time2 - time
                if time4 != None:
                    time = time - time4
                score = len(board)**2/ time.seconds
                accdata[0] = str(float(accdata[0]) + score)
                accdata[6] = str(int(accdata[6]) + 1)
                with open("account.csv", "w") as f:
                    f.write(accdata[0] + "," + accdata[1] + "," + accdata[2] + "," + accdata[3] + "," + accdata[4] + "," + accdata[5] + "," + accdata[6])
                f.close()
                print("Time taken: ", time.seconds, " seconds")
                print()
                print("Solved")
                for i in range(len(displayboard)):
                    for j in range(len(displayboard)):
                        if displayboard[i][j] == "N":
                            displayboard[i][j] = "X"
                Solver.print_board(displayboard)
                MainMenu()


def GetStats():
    print(GetLevel())
    with open("account.csv", "r") as f:
        data = f.readline()
        data = data.split(",")
        score = float(data[0])
        gamesplayed = int(data[6])
    f.close()
    if gamesplayed == 0:
        print("No games played")
    else:
        print("Games played: ", gamesplayed)
        print("Average score: ", score/gamesplayed)

def GetLevel():
    with open("account.csv", "r") as f:
        levelscore = f.readline()
        levelscore = levelscore.split(",")
        levelscore = float(levelscore[0])
    f.close()
    if levelscore < 1:
        rank = "Beginner"
    elif levelscore >= 1 and levelscore < 5:
        rank = "Intermediate solver"
    elif levelscore >= 5 and levelscore < 20:
        rank = "Advanced solver"
    elif levelscore >= 20 and levelscore < 100:
        rank = "Elite Challenger"
    elif levelscore >= 100:
        rank = "Train Tracks Solver Elite"
    return rank

def Settings():
    with open("account.csv", "r") as f:
        data = f.readline()
        data = data.split(",")
        score = float(data[0])
        onofftimetaken = int(data[1])
        onoffpercent = int(data[2])
        onoffhints = int(data[3])
        onoffsolution = int(data[4])
        maxstartingshapes = int(data[5])
        gamesplayed = int(data[6])
    f.close()
    print("Current Settings")
    print()
    if onofftimetaken == 0:
        print("Time taken viewing is off")
    else:
        print("Time taken viewing is on")
    if onoffpercent == 0:
        print("Percent complete viewing is off")
    else:
        print("Percent complete viewing is on")
    if onoffhints == 0:
        print("Hints are off- this is the recommended setting")
    else:
        print("Hints are on- this is not the recommended setting")
    if onoffsolution == 0:
        print("Solution viewing is off- this is the recommended setting")
    else:
        print("Solution viewing is on- to discourage cheating, we recommend turning this off")
    print("Maximum starting shapes: ", maxstartingshapes)
    print()
    print("Enter 1 to turn time taken viewing on or off")
    print("Enter 2 to turn percent complete viewing on or off")
    print("Enter 3 to turn hints on or off")
    print("Enter 4 to turn solution viewing on or off")
    print("Enter 5 to change the maximum starting shapes")
    print("Enter 6 to turn on hard mode")
    print("Enter 7 to return settings to default")
    print("Enter 8 to return to the main menu")
    print("Enter 9 to reset account")
    choice = input()
    while choice not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        choice = input("Enter a valid choice: ")
    if choice == "1":
        if onofftimetaken == 0:
            print("Time taken viewing is off, type y to turn on or n to keep off: ")
            choice = input()
            while choice not in ["y", "n"]:
                choice = input("Enter a valid choice: ")
            if choice == "y":
                onofftimetaken = 1
        else:
            print("Time taken viewing is on, type y to turn off or n to keep on: ")
            choice = input()
            while choice not in ["y", "n"]:
                choice = input("Enter a valid choice: ")
            if choice == "y":
                onofftimetaken = 0
    if choice == "2":
        if onoffpercent == 0:
            print("Percent complete viewing is off, type y to turn on or n to keep off: ")
            choice = input()
            while choice not in ["y", "n"]:
                choice = input("Enter a valid choice: ")
            if choice == "y":
                onoffpercent = 1
        else:
            print("Percent complete viewing is on, type y to turn off or n to keep on: ")
            choice = input()
            while choice not in ["y", "n"]:
                choice = input("Enter a valid choice: ")
            if choice == "y":
                onoffpercent = 0
    if choice == "3":
        if onoffhints == 0:
            print("Hints are off, type y to turn on or n to keep off: ")
            choice = input()
            while choice not in ["y", "n"]:
                choice = input("Enter a valid choice: ")
            if choice == "y":
                onoffhints = 1
        else:
            print("Hints are on, type y to turn off or n to keep on: ")
            choice = input()
            while choice not in ["y", "n"]:
                choice = input("Enter a valid choice: ")
            if choice == "y":
                onoffhints = 0
    if choice == "4":
        if onoffsolution == 0:
            print("Solution viewing is off, type y to turn on or n to keep off: ")
            choice = input()
            while choice not in ["y", "n"]:
                choice = input("Enter a valid choice: ")
            if choice == "y":
                onoffsolution = 1
        else:
            print("Solution viewing is on, type y to turn off or n to keep on: ")
            choice = input()
            while choice not in ["y", "n"]:
                choice = input("Enter a valid choice: ")
            if choice == "y":
                onoffsolution = 0
    if choice == "5":
        print("Enter the maximum starting shapes (minimum of 2): ")
        print("Current maximum: ", maxstartingshapes)
        choice = input()
        while not choice.isdigit() or int(choice) < 2:
            choice = input("Enter a valid number: ")
        maxstartingshapes = int(choice)
        print("Maximum starting shapes changed to: ", maxstartingshapes)
    if choice == "6":
        print("Type h to confirm hard mode")
        print("This disables hints, solution viewing and makes maximum starting shapes 4")
        choice = input()
        if choice.upper() == "H":
            onoffhints = 0
            onoffsolution = 0
            maxstartingshapes = 4
            print("Hard mode enabled")
    if choice == "7":
        print("Settings will be returned to default. Confirm by typing y")
        choice = input()
        if choice.upper() == "Y":
            onofftimetaken = 1
            onoffpercent = 0
            onoffhints = 0
            onoffsolution = 0
            maxstartingshapes = 7
            print("Settings returned to default")
    if choice == "8":
        MainMenu()
    if choice == "9":
        print("Are you sure you want to reset your account? Type y to confirm. This cannot be redone.") 
        print("This will reset your score and settings to default.")
        choice = input()
        if choice.upper() == "Y":
            score = 0
            onofftimetaken = 1
            onoffpercent = 0
            onoffhints = 0
            onoffsolution = 0
            maxstartingshapes = 7
            gamesplayed = 0
            print("Account reset")

    with open("account.csv", "w") as f:
        f.write(f"{score},{onofftimetaken},{onoffpercent},{onoffhints},{onoffsolution},{maxstartingshapes},{gamesplayed}")
    f.close()
    Settings()

def find_pkl_files():
    files = []
    for file in os.listdir():
        if file.endswith(".pkl"):
            files.append(file)
    return files

def MainMenu():
    print()
    x = GetLevel()
    print("Welcome", x)

    with open("account.csv", "r") as f:
        data = f.readline()
        data = data.split(",")
        gamesplayed = int(data[6])
    f.close()
    if gamesplayed == 0:
        ExplainRules()
        print("Enter any key to continue")
        input()
    while True:
        print("Main Menu")
        print("Enter 1 to play a game")
        print("Enter 2 to view your stats")
        print("Enter 3 to view settings")
        print("Enter 4 to quit")
        print()
        choice = input()
        if choice == "1":
            PlayGame()
        elif choice == "2":
            GetStats()
        elif choice == "3":
            Settings()
        elif choice == "4":
            quit()
        print()

def PlayGame():
    generation = ""
    gamechoice = ""
    while gamechoice not in ["G", "M", "F", "Q", "g", "m", "f", "q"]:
        gamechoice = input("Enter G to generate a board, M to manually input a board, F to read from a file and Q to return to the main menu: ")
    if gamechoice.upper() == "G":
        with open("account.csv", "r") as f:
            data = f.readline()
            data = data.split(",")
            maxstartingshapes = int(data[5])
        f.close()

        board_size = 0
        generation = "y"
        generator = Generator()
        board, column_totals, row_totals, SAVEDBOARD, startingshapes, board_size = generator.build_board(board_size)
        board, editboard, column_totals, row_totals = Solver.Solve(board, column_totals, row_totals, SAVEDBOARD, startingshapes, generation, board_size)
        while len(startingshapes) > maxstartingshapes:
            board, column_totals, row_totals, SAVEDBOARD, startingshapes, board_size = generator.build_board(board_size)
            board, editboard, column_totals, row_totals = Solver.Solve(board, column_totals, row_totals, SAVEDBOARD, startingshapes, generation, board_size)
        EditBoard.manual_edit(board,editboard,column_totals,row_totals)
    
    elif gamechoice.upper() == "M":
        generation = "n"
        generator = Generator()
        board, column_totals, row_totals, SAVEDBOARD, startingshapes, board_size = generator.manual_board()
        board, editboard, column_totals, row_totals = Solver.Solve(board, column_totals, row_totals, SAVEDBOARD, startingshapes, generation, board_size)
        EditBoard.manual_edit(board,editboard,column_totals,row_totals)
    
    elif gamechoice.upper() == "F":
        files = find_pkl_files()
        print()
        print("Files available: ")
        print()
        for file in files:
            print(file)
        print()
        picklefile = input("Enter the name of the file (Dont include file type) ")
        picklefile = picklefile + ".pkl"
        if picklefile not in files:
            print("File not found")
            PlayGame()
        with open(picklefile, "rb") as f:
            pick = pickle.load(f)
        f.close()
        board, editboard, column_totals, row_totals = pick
        EditBoard.manual_edit(board,editboard,column_totals,row_totals)

    elif gamechoice.upper() == "Q":
        MainMenu()

def ExplainRules():
    print("Welcome to the Train Tracks Puzzle Game")
    print()
    print("This is a game where you must connect village A to village B")
    print("You must do this by drawing tracks between the nodes")
    print("The nodes are represented using a coordinate system")
    print("The top left node is 0,0 and the bottom right node is board size - 1, board size - 1")
    print("i.e. for a 5x5 board, the top left node is 0,0 and the bottom right node is 4,4")
    print("The top row and left column of the board show the column and row totals respectively")
    print("The number of tracks you need to fill in each row and column is dictated by these totals")
    print("The board is mostly filled with Ns, which represent empty nodes")
    print("Input dots to represent nodes which you know must be tracks, but you don't know the shape yet")
    print("If you think you know a shape, input the shape")
    print("The shapes are as follows: ")
    print("H represents a horizontal track")
    print("V represents a vertical track")
    print("RD represents a track that connects to the node above and to the right")
    print("LD represents a track that connects to the node above and to the left")
    print("RU represents a track that connects to the node below and to the right")
    print("LU represents a track that connects to the node below and to the left")
    print("You can also input X to represent a node that cannot be a track")
    print("You can undo your previous move by typing u")
    print("There are also a few other features such as hints and solution viewing")
    print("If you are stuck on a puzzle which you have attempted in real life, you can input the board")
    print("The program will then attempt to solve the puzzle")
    print("You can also save the board to a file")
    print("If you just want to play a random game, enter 1 in the Main Menu, followed by G to generate")
    print("Then follow any further instructions")
    print("Good luck!")
    print()

MainMenu()