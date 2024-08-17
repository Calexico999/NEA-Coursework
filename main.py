import random

# Box drawing characters: ┌ ┐ └ ┘ ─ │ ┬ ┴ ├ ┤ ┼
# book 3 p175 has 2 possible other rules ####

class StartNode:
    def start_node(board_size):
        edge = False
        while not edge:
            startxnode = random.randint(0, board_size - 1)
            startynode = random.randint(0, board_size - 1)
            if startxnode == 0 or startxnode == board_size - 1 or startynode == 0 or startynode == board_size - 1:
                edge = True
        return startxnode, startynode


class Generate_Board:
    def generate_board():
        size = int(input("Enter the size of the board: "))
        board = []
        for i in range(size):
            board.append([0] * size)
                
        start = StartNode.start_node(size)
        board[start[0]][start[1]] = "S"
        return board, start


    def print_board(board):
        for row in board:
            print(' '.join(map(str, row)))


class GenerateRandomPath:

    def start_node(board_size):
        edge = False
        while not edge:
            startxnode = random.randint(0, board_size - 1)
            startynode = random.randint(0, board_size - 1)
            if startxnode == 0 or startxnode == board_size - 1 or startynode == 0 or startynode == board_size - 1:
                edge = True
        return startxnode, startynode

    def dfs(start, board_size, min_length=30, max_length=40):
        visited = set()
        stack = [(start, [start])]
        

        while stack:
            v, path = stack.pop()

            if len(path) >= max_length:
                return None

            if len(path) >= min_length:
                #if on edge, return path
                if v[0] == 0 or v[0] == board_size - 1 or v[1] == 0 or v[1] == board_size - 1:
                    #if not all rows and columns have been visited at least once return None
                    #do this by checking if any row or column has only 0s
                    rows = [0] * board_size
                    cols = [0] * board_size
                    for (x, y) in path:
                        rows[x] = 1
                        cols[y] = 1
                    if 0 in rows or 0 in cols:
                        return None
                    return path

            if v in visited:
                continue

            visited.add(v)
            (x, y) = v 
            all_next = []

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                x1, y1 = x + dx, y + dy
                if x1 < 0 or x1 >= board_size or y1 < 0 or y1 >= board_size:
                    continue
                if (x1, y1) in visited:
                    continue
                all_next.append((x1, y1))

            if all_next:
                next_node = random.choice(all_next)
                stack.append((next_node, path + [next_node]))

        return None  # If no valid path is found

    def print_path(path, board_size):
        board = [['0' for _ in range(board_size)] for _ in range(board_size)]
        if path:
            start = path[0]
            end = path[-1]
            board[start[0]][start[1]] = 'S'
            board[end[0]][end[1]] = 'E'
            for (x, y) in path[1:-1]:
                board[x][y] = '1'
        for row in board:
            print(' '.join(row))


if __name__ == "__main__":
    board_size = int(input("Enter the size of the board: "))
    path = None
    while path is None:
        start = GenerateRandomPath.start_node(board_size)
        path = GenerateRandomPath.dfs(start, board_size)
    GenerateRandomPath.print_path(path, board_size)

class Solver:
    # Box drawing characters
    RD = "┌"
    LD = "┐"
    RU = "└"
    LU = "┘"
    H = "─"
    V = "│"
    DOT = "."
    NULL = "0"
    characters = {
        'RD': RD,
        'LD': LD,
        'RU': RU,
        'LU': LU,
        'H': H,
        'V': V
    }
    

    def generate_board():
        size = int(input("Enter the edge length of the board, in range 4 <= length <= 10: "))
        if size < 4 or size > 10:
            print("Invalid size")
            size = int(input("Enter the edge length of the board, in range 4 <= length <= 10: "))
        
        board = []
        for i in range(size):
            board.append(["N"] * size)

        # User selects character for the starting position
        while True:
            try:
                start = input("Enter the starting position in the format x,y: ").split(',')
                start = (int(start[0]), int(start[1]))
                if 0 <= start[0] < size and 0 <= start[1] < size:
                    char_choice = input(f"Choose a character for the starting position {start} (RD, LD, RU, LU, H, V): ")
                    if char_choice in Solver.characters:
                        board[start[0]][start[1]] = Solver.characters[char_choice]
                        break
                    else:
                        print("Invalid character choice. Please choose from RD, LD, RU, LU, H, V.")
                else:
                    print(f"Invalid position. Please enter values between 0 and {size-1}.")
            except ValueError:
                print("Invalid format. Please enter the position in the format x,y with integers.")

        # User selects character for the ending position
        while True:
            try:
                end = input("Enter the ending position in the format x,y: ").split(',')
                end = (int(end[0]), int(end[1]))
                if 0 <= end[0] < size and 0 <= end[1] < size:
                    if end != start:
                        char_choice = input(f"Choose a character for the ending position {end} (RD, LD, RU, LU, H, V): ")
                        if char_choice in Solver.characters:
                            board[end[0]][end[1]] = Solver.characters[char_choice]
                            break
                        else:
                            print("Invalid character choice. Please choose from RD, LD, RU, LU, H, V.")
                    else:
                        print("End position cannot be the same as start position.")
                else:
                    print(f"Invalid position. Please enter values between 0 and {size-1}.")
            except ValueError:
                print("Invalid format. Please enter the position in the format x,y with integers.")

        othernodes = True
        while othernodes:
            # User defines position and shape of any other given nodes
            morenodes = input("Are there any more nodes to add? (Y/N): ")
            if morenodes.lower() == 'y':
                while True:
                    try:
                        node = input("Enter the position in the format x,y: ").split(',')
                        node = (int(node[0]), int(node[1]))
                        if 0 <= node[0] < size and 0 <= node[1] < size:
                            if node != start and node != end:
                                char_choice = input(f"Choose a character for the position {node} (RD, LD, RU, LU, H, V): ")
                                if char_choice in Solver.characters:
                                    board[node[0]][node[1]] = Solver.characters[char_choice]
                                    break
                                else:
                                    print("Invalid character choice. Please choose from RD, LD, RU, LU, H, V.")
                            else:
                                print("Node position cannot be the same as start or end position.")
                        else:
                            print(f"Invalid position. Please enter values between 0 and {size-1}.")
                    except ValueError:
                        print("Invalid format. Please enter the position in the format x,y with integers.")
            elif morenodes.lower() == 'n':
                othernodes = False
            else:
                print("Invalid input. Please enter Y or N.")

        

        return board, start, end


    def print_board(board):
        for row in board:
            print(' '.join(map(str, row)))


    def Solve(board, start, end):
        bruteforceneeded = False
        edgerulesneeded = False
        any_changes = True
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
        minicount = 0
        trysecond = False
        dots_two = []
        dots_two_possibles = []
        satisfactory = False

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

        while any_changes or bruteforceneeded:
                
            any_changes = False
            edgerulesneeded = False
            flagimpossible = False
            alreadyreplaced = False

            if bruteforceneeded == False:
                # for i in dots_two
                # if first and second parts of dots two are a character on the board, remove from dotstwo
                # e.g. if a node of dotstwo is (1, 2, 3, 4) and board[1][2] is a character, remove from dotstwo
                for d in dots_two:
                    if board[d[0]][d[1]] in shapes.values():
                        dots_two.remove(d)

            # First stage: change all 0s which connect to a start or end node to '.'
            print("Initial board:")
            Solver.print_board(board)
            print("\nFirst stage:")
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] in Solver.characters.values():
                        if board[i][j] == Solver.RD:
                            if i + 1 < len(board) and board[i + 1][j] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i + 1) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i+1, j, board[i+1][j], 1))

                                board[i + 1][j] = '.'
                                any_changes = True
                            if j + 1 < len(board) and board[i][j + 1] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j + 1):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j+1, board[i][j+1], 1))
                                board[i][j + 1] = '.'
                                any_changes = True
                        elif board[i][j] == Solver.LD:
                            if i + 1 < len(board) and board[i + 1][j] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i + 1) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i+1, j, board[i+1][j], 1))
                                board[i + 1][j] = '.'
                                any_changes = True
                            if j - 1 >= 0 and board[i][j - 1] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j - 1):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j-1, board[i][j-1], 1))
                                board[i][j - 1] = '.'
                                any_changes = True
                        elif board[i][j] == Solver.RU:
                            if i - 1 >= 0 and board[i - 1][j] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i - 1) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i-1, j, board[i-1][j], 1))
                                board[i - 1][j] = '.'
                                any_changes = True
                            if j + 1 < len(board) and board[i][j + 1] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j + 1):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j+1, board[i][j+1], 1))
                                board[i][j + 1] = '.'
                                any_changes = True
                        elif board[i][j] == Solver.LU:
                            if i - 1 >= 0 and board[i - 1][j] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i - 1) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i-1, j, board[i-1][j], 1))
                                board[i - 1][j] = '.'
                                any_changes = True
                            if j - 1 >= 0 and board[i][j - 1] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j - 1):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j-1, board[i][j-1], 1))
                                board[i][j - 1] = '.'
                                any_changes = True
                        elif board[i][j] == Solver.H:
                            if j + 1 < len(board) and board[i][j + 1] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j + 1):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j+1, board[i][j+1], 1))
                                board[i][j + 1] = '.'
                                any_changes = True
                            if j - 1 >= 0 and board[i][j - 1] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j - 1):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j-1, board[i][j-1], 1))
                                board[i][j - 1] = '.'
                                any_changes = True
                        elif board[i][j] == Solver.V:
                            if i + 1 < len(board) and board[i + 1][j] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i + 1) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i+1, j, board[i+1][j], 1))
                                board[i + 1][j] = '.'
                                any_changes = True
                            if i - 1 >= 0 and board[i - 1][j] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i - 1) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i-1, j, board[i-1][j], 1))
                                board[i - 1][j] = '.'
                                any_changes = True

            Solver.print_board(board)

            # Second stage: check each column to see if all possible nodes are used
            column_totals = [2,3,2,7,8,8,3,5,2,2]
            row_totals = [5,4,2,5,7,3,4,4,4,4]
            changed = True
            while changed == True:
                changed = False
                for j in range(len(board)):
                    count = 0
                    for i in range(len(board)):
                        if board[i][j] in definites.values():
                            count += 1
                    if count == column_totals[j]:
                        for i in range(len(board)):
                            if board[i][j] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = 'X'
                                changed = True
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
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = 'X'
                                changed = True
                                any_changes = True
                    if count > row_totals[i]:
                        flagimpossible = True

                # if number of non-Xs in each column is equal to the column total, change all 0s to dots
                for j in range(len(board)):
                    count = 0
                    for i in range(len(board)):
                        if board[i][j] != 'X':
                            count += 1
                    if count == column_totals[j]:
                        for i in range(len(board)):
                            if board[i][j] == "N":
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = '.'
                                changed = True
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
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = '.'
                                changed = True
                                any_changes = True

            print()
            print("Second stage:")
            Solver.print_board(board)

            ###### THIRD STAGE
            # for each dot in the grid
            # if it is adjacent to 2 from 'characters', change it the character which fits the pattern
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
                            if directions[0] == 'left' and directions[1] == 'right':
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = H
                                any_changes = True
                            elif directions[0] == 'left' and directions[1] == 'up':
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = LU
                                any_changes = True
                            elif directions[0] == 'left' and directions[1] == 'down':
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = LD
                                any_changes = True
                            elif directions[0] == 'up' and directions[1] == 'down':
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = V
                                any_changes = True
                            elif directions[0] == 'up' and directions[1] == 'right':
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = RU
                                any_changes = True
                            elif directions[0] == 'down' and directions[1] == 'right':
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = RD
                                any_changes = True

                            
            print()
            print("Third stage:")
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
            
            ###### FOURTH STAGE
            # for each empty square in the grid
            # if it is adjacent to 0 or 1 squares from 'indefinites', change it to 'X'

            changed = True
            while changed:
                changed = False
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
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = 'X'
                                changed = True
                                any_changes = True
            print("Fourth stage:")
            Solver.print_board(board)
            print()

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
                            if directions[0] == 'left' and directions[1] == 'right':
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = H
                                any_changes = True
                            elif directions[0] == 'left' and directions[1] == 'up':
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = LU
                                any_changes = True
                            elif directions[0] == 'left' and directions[1] == 'down':
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = LD
                                any_changes = True
                            elif directions[0] == 'up' and directions[1] == 'down':
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = V
                                any_changes = True
                            elif directions[0] == 'right' and directions[1] == 'up':
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = RU
                                any_changes = True
                            elif directions[0] == 'right' and directions[1] == 'down':
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                board[i][j] = RD
                                any_changes = True
                        if count == 3:
                            outofrange = False
                            change = False
                            if i - 1 >= 0:
                                if (board[i-1][j] == V) or (board[i-1][j] == RD) or (board[i-1][j] == LD):
                                    shapedir = []
                                    if board[i-1][j] == RD:
                                        shapedir.append('right')
                                        shapedir.append('down')
                                    if board[i-1][j] == RU:
                                        shapedir.append('up')
                                        shapedir.append('right')
                                    if board[i-1][j] == LD:
                                        shapedir.append('left')
                                        shapedir.append('down')
                                    if board[i-1][j] == LU:
                                        shapedir.append('left')
                                        shapedir.append('up')
                                    if board[i-1][j] == H:
                                        shapedir.append('left')
                                        shapedir.append('right')
                                    if board[i-1][j] == V:
                                        shapedir.append('up')
                                        shapedir.append('down')
                                    prevsquare = i-1,j
                                    if shapedir[0] == 'left':
                                        i1 = i-1
                                        j1 = j-1
                                    if shapedir[0] == 'right':
                                        i1 = i-1
                                        j1 = j+1
                                    if shapedir[0] == 'up':
                                        i1 = i-2
                                        j1 = j
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    while outofrange == False and board[i1][j1] in shapes.values():
                                        i2 = i1
                                        j2 = j1
                                        shapedir = []
                                        if board[i1][j1] == RD:
                                            shapedir.append('right')
                                            shapedir.append('down')
                                        if board[i1][j1] == RU:
                                            shapedir.append('up')
                                            shapedir.append('right')
                                        if board[i1][j1] == LD:
                                            shapedir.append('left')
                                            shapedir.append('down')
                                        if board[i1][j1] == LU:
                                            shapedir.append('left')
                                            shapedir.append('up')
                                        if board[i1][j1] == H:
                                            shapedir.append('left')
                                            shapedir.append('right')
                                        if board[i1][j1] == V:
                                            shapedir.append('up')
                                            shapedir.append('down')
                                        while len(shapedir) > 1:
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
                                        if len(shapedir) == 1:
                                            change = True
                                            prevsquare = i1,j1
                                            if shapedir[0] == 'left':
                                                i1 = i1
                                                j1 = j1-1
                                            if shapedir[0] == 'right':
                                                i1 = i1
                                                j1 = j1+1
                                            if shapedir[0] == 'up':
                                                i1 = i1-1
                                                j1 = j1
                                            if shapedir[0] == 'down':
                                                i1 = i1+1
                                                j1 = j1
                                        if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                            break
                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    if (outofrange == False) and (board[i1][j1] == '.'):
                                        if i1 == i and j1 == j:
                                            if board[i-1][j] in shapes.values():
                                                shapedir = []
                                                if board[i-1][j] == RD:
                                                    shapedir.append('down')
                                                    shapedir.append('right')
                                                if board[i-1][j] == RU:
                                                    shapedir.append('right')
                                                    shapedir.append('up')
                                                if board[i-1][j] == LD:
                                                    shapedir.append('down')
                                                    shapedir.append('left')
                                                if board[i-1][j] == LU:
                                                    shapedir.append('up')
                                                    shapedir.append('left')
                                                if board[i-1][j] == H:
                                                    shapedir.append('right')
                                                    shapedir.append('left')
                                                if board[i-1][j] == V:
                                                    shapedir.append('down')
                                                    shapedir.append('up')
                                                prevsquare = i-1,j
                                                if shapedir[0] == 'down':
                                                    i1 = i
                                                    j1 = j
                                                if shapedir[0] == 'right':
                                                    i1 = i-1
                                                    j1 = j+1
                                                if shapedir[0] == 'up':
                                                    i1 = i-2
                                                    j1 = j
                                                outofrange = False
                                                if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                                    outofrange = True  
                                                while outofrange == False and board[i1][j1] in shapes.values():
                                                    i2 = i1
                                                    j2 = j1
                                                    shapedir = []
                                                    if board[i1][j1] == RD:
                                                        shapedir.append('right')
                                                        shapedir.append('down')
                                                    if board[i1][j1] == RU:
                                                        shapedir.append('up')
                                                        shapedir.append('right')
                                                    if board[i1][j1] == LD:
                                                        shapedir.append('left')
                                                        shapedir.append('down')
                                                    if board[i1][j1] == LU:
                                                        shapedir.append('left')
                                                        shapedir.append('up')
                                                    if board[i1][j1] == H:
                                                        shapedir.append('left')
                                                        shapedir.append('right')
                                                    if board[i1][j1] == V:
                                                        shapedir.append('up')
                                                        shapedir.append('down')
                                                    while len(shapedir) > 1:
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
                                                        
                                                    if len(shapedir) == 1:
                                                        change = True
                                                        prevsquare = i1,j1
                                                        if shapedir[0] == 'left':
                                                            i1 = i1
                                                            j1 = j1-1
                                                        if shapedir[0] == 'right':
                                                            i1 = i1
                                                            j1 = j1+1
                                                        if shapedir[0] == 'up':
                                                            i1 = i1-1
                                                            j1 = j1
                                                        if shapedir[0] == 'down':
                                                            i1 = i1+1
                                                            j1 = j1
                                                    outofrange = False
                                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                                        outofrange = True
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

                            if i + 1 < len(board):
                                if (board[i+1][j] == LU) or (board[i+1][j] == RU) or (board[i+1][j] == V):
                                    shapedir = []
                                    if board[i+1][j] == RD:
                                        shapedir.append('right')
                                        shapedir.append('down')
                                    if board[i+1][j] == RU:
                                        shapedir.append('up')
                                        shapedir.append('right')
                                    if board[i+1][j] == LD:
                                        shapedir.append('left')
                                        shapedir.append('down')
                                    if board[i+1][j] == LU:
                                        shapedir.append('left')
                                        shapedir.append('up')
                                    if board[i+1][j] == H:
                                        shapedir.append('left')
                                        shapedir.append('right')
                                    if board[i+1][j] == V:
                                        shapedir.append('up')
                                        shapedir.append('down')
                                    prevsquare = i+1,j
                                    if shapedir[0] == 'left':
                                        i1 = i+1
                                        j1 = j-1
                                    if shapedir[0] == 'right':
                                        i1 = i+1
                                        j1 = j+1
                                    if shapedir[0] == 'up':
                                        i1 = i
                                        j1 = j
                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    while outofrange == False and board[i1][j1] in shapes.values():
                                        i2 = i1
                                        j2 = j1
                                        shapedir = []
                                        if board[i1][j1] == RD:
                                            shapedir.append('right')
                                            shapedir.append('down')
                                        if board[i1][j1] == RU:
                                            shapedir.append('up')
                                            shapedir.append('right')
                                        if board[i1][j1] == LD:
                                            shapedir.append('left')
                                            shapedir.append('down')
                                        if board[i1][j1] == LU:
                                            shapedir.append('left')
                                            shapedir.append('up')
                                        if board[i1][j1] == H:
                                            shapedir.append('left')
                                            shapedir.append('right')
                                        if board[i1][j1] == V:
                                            shapedir.append('up')
                                            shapedir.append('down')
                                        while len(shapedir) > 1:
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
                                        if len(shapedir) == 1:
                                            change = True
                                            prevsquare = i1,j1
                                            if 'left' in shapedir:
                                                i1 = i1
                                                j1 = j1-1
                                            if 'right' in shapedir:
                                                i1 = i1
                                                j1 = j1+1
                                            if 'up' in shapedir:
                                                i1 = i1-1
                                                j1 = j1
                                            if 'down' in shapedir:
                                                i1 = i1+1
                                                j1 = j1
                                        if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                            break
                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    if outofrange == False and board[i1][j1] == '.':
                                        if i1 == i and j1 == j:
                                            if board[i+1][j] in shapes.values():
                                                shapedir = []
                                                if board[i+1][j] == RD:
                                                    shapedir.append('down')
                                                    shapedir.append('right')
                                                if board[i+1][j] == RU:
                                                    shapedir.append('right')
                                                    shapedir.append('up')
                                                if board[i+1][j] == LD:
                                                    shapedir.append('down')
                                                    shapedir.append('left')
                                                if board[i+1][j] == LU:
                                                    shapedir.append('up')
                                                    shapedir.append('left')
                                                if board[i+1][j] == H:
                                                    shapedir.append('right')
                                                    shapedir.append('left')
                                                if board[i+1][j] == V:
                                                    shapedir.append('down')
                                                    shapedir.append('up')
                                                prevsquare = i+1,j
                                                if shapedir[0] == 'down':
                                                    i1 = i+2
                                                    j1 = j
                                                if shapedir[0] == 'right':
                                                    i1 = i+1
                                                    j1 = j+1
                                                if shapedir[0] == 'up':
                                                    i1 = i
                                                    j1 = j
                                                outofrange = False
                                                if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                                    outofrange = True  
                                                while outofrange == False and board[i1][j1] in shapes.values():
                                                    i2 = i1
                                                    j2 = j1
                                                    shapedir = []
                                                    if board[i1][j1] == RD:
                                                        shapedir.append('right')
                                                        shapedir.append('down')
                                                    if board[i1][j1] == RU:
                                                        shapedir.append('up')
                                                        shapedir.append('right')
                                                    if board[i1][j1] == LD:
                                                        shapedir.append('left')
                                                        shapedir.append('down')
                                                    if board[i1][j1] == LU:
                                                        shapedir.append('left')
                                                        shapedir.append('up')
                                                    if board[i1][j1] == H:
                                                        shapedir.append('left')
                                                        shapedir.append('right')
                                                    if board[i1][j1] == V:
                                                        shapedir.append('up')
                                                        shapedir.append('down')
                                                    while len(shapedir) > 1:
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
                                                    if len(shapedir) == 1:
                                                        change = True
                                                        prevsquare = i1,j1
                                                        if 'left' in shapedir:
                                                            i1 = i1
                                                            j1 = j1-1
                                                        if 'right' in shapedir:
                                                            i1 = i1
                                                            j1 = j1+1
                                                        if 'up' in shapedir:
                                                            i1 = i1-1
                                                            j1 = j1
                                                        if 'down' in shapedir:
                                                            i1 = i1+1
                                                            j1 = j1
                                                    outofrange = False
                                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                                        outofrange = True

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
                                
                            if j - 1 >= 0:
                                if (board[i][j-1] == RU) or (board[i][j-1] == RD) or (board[i][j-1] == H):
                                    shapedir = []
                                    if board[i][j-1] == H:
                                        shapedir.append('left')
                                        shapedir.append('right')
                                    if board[i][j-1] == RD:
                                        shapedir.append('right')
                                        shapedir.append('down')
                                    if board[i][j-1] == RU:
                                        shapedir.append('up')
                                        shapedir.append('right')
                                    if board[i][j-1] == LD:
                                        shapedir.append('left')
                                        shapedir.append('down')
                                    if board[i][j-1] == LU:
                                        shapedir.append('left')
                                        shapedir.append('up')
                                    if board[i][j-1] == V:
                                        shapedir.append('up')
                                        shapedir.append('down')
                                    prevsquare = i,j-1
                                    if shapedir[0] == 'left':
                                        i1 = i
                                        j1 = j-2
                                    if shapedir[0] == 'right':
                                        i1 = i
                                        j1 = j
                                    if shapedir[0] == 'up':
                                        i1 = i-1
                                        j1 = j-1
                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    while outofrange == False and board[i1][j1] in shapes.values():
                                        i2 = i1
                                        j2 = j1
                                        shapedir = []
                                        if board[i1][j1] == RD:
                                            shapedir.append('right')
                                            shapedir.append('down')
                                        if board[i1][j1] == RU:
                                            shapedir.append('up')
                                            shapedir.append('right')
                                        if board[i1][j1] == LD:
                                            shapedir.append('left')
                                            shapedir.append('down')
                                        if board[i1][j1] == LU:
                                            shapedir.append('left')
                                            shapedir.append('up')
                                        if board[i1][j1] == H:
                                            shapedir.append('left')
                                            shapedir.append('right')
                                        if board[i1][j1] == V:
                                            shapedir.append('up')
                                            shapedir.append('down')
                                        while len(shapedir) > 1:
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
                                        if len(shapedir) == 1:
                                            change = True
                                            prevsquare = i1,j1
                                            if 'left' in shapedir:
                                                i1 = i1
                                                j1 = j1-1
                                            if 'right' in shapedir:
                                                i1 = i1
                                                j1 = j1+1
                                            if 'up' in shapedir:
                                                i1 = i1-1
                                                j1 = j1
                                            if 'down' in shapedir:
                                                i1 = i1+1
                                                j1 = j1
                                        if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                            break
                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    if outofrange == False and board[i1][j1] == '.':
                                        if i1 == i and j1 == j:
                                            if board[i][j-1] in shapes.values():
                                                shapedir = []
                                                if board[i][j-1] == H:
                                                    shapedir.append('right')
                                                    shapedir.append('left')
                                                if board[i][j-1] == RD:
                                                    shapedir.append('down')
                                                    shapedir.append('right')
                                                if board[i][j-1] == RU:
                                                    shapedir.append('right')
                                                    shapedir.append('up')
                                                if board[i][j-1] == LD:
                                                    shapedir.append('down')
                                                    shapedir.append('left')
                                                if board[i][j-1] == LU:
                                                    shapedir.append('up')
                                                    shapedir.append('left')
                                                if board[i][j-1] == V:
                                                    shapedir.append('down')
                                                    shapedir.append('up')
                                                prevsquare = i,j-1
                                                if shapedir[0] == 'down':
                                                    i1 = i+1
                                                    j1 = j-1
                                                if shapedir[0] == 'right':
                                                    i1 = i
                                                    j1 = j
                                                if shapedir[0] == 'up':
                                                    i1 = i-1
                                                    j1 = j-1
                                                outofrange = False
                                                if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                                    outofrange = True  
                                                while outofrange == False and board[i1][j1] in shapes.values():
                                                    i2 = i1
                                                    j2 = j1
                                                    shapedir = []
                                                    if board[i1][j1] == RD:
                                                        shapedir.append('right')
                                                        shapedir.append('down')
                                                    if board[i1][j1] == RU:
                                                        shapedir.append('up')
                                                        shapedir.append('right')
                                                    if board[i1][j1] == LD:
                                                        shapedir.append('left')
                                                        shapedir.append('down')
                                                    if board[i1][j1] == LU:
                                                        shapedir.append('left')
                                                        shapedir.append('up')
                                                    if board[i1][j1] == H:
                                                        shapedir.append('left')
                                                        shapedir.append('right')
                                                    if board[i1][j1] == V:
                                                        shapedir.append('up')
                                                        shapedir.append('down')
                                                    while len(shapedir) > 1:
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
                                                    if len(shapedir) == 1:
                                                        change = True
                                                        prevsquare = i1,j1
                                                        if 'left' in shapedir:
                                                            i1 = i1
                                                            j1 = j1-1
                                                        if 'right' in shapedir:
                                                            i1 = i1
                                                            j1 = j1+1
                                                        if 'up' in shapedir:
                                                            i1 = i1-1
                                                            j1 = j1
                                                        if 'down' in shapedir:
                                                            i1 = i1+1
                                                            j1 = j1
                                                    outofrange = False
                                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                                        outofrange = True
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
                            
                            if j + 1 < len(board):
                                if (board[i][j+1] == LU) or (board[i][j+1] == LD) or (board[i][j+1] == H):
                                    shapedir = []
                                    if board[i][j+1] == H:
                                        shapedir.append('left')
                                        shapedir.append('right')
                                    if board[i][j+1] == RD:
                                        shapedir.append('right')
                                        shapedir.append('down')
                                    if board[i][j+1] == RU:
                                        shapedir.append('up')
                                        shapedir.append('right')
                                    if board[i][j+1] == LD:
                                        shapedir.append('left')
                                        shapedir.append('down')
                                    if board[i][j+1] == LU:
                                        shapedir.append('left')
                                        shapedir.append('up')
                                    if board[i][j+1] == V:
                                        shapedir.append('up')
                                        shapedir.append('down')
                                    prevsquare = i,j+1
                                    if shapedir[0] == 'left':
                                        i1 = i
                                        j1 = j
                                    if shapedir[0] == 'right':
                                        i1 = i
                                        j1 = j+2
                                    if shapedir[0] == 'up':
                                        i1 = i-1
                                        j1 = j+1
                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    while outofrange == False and board[i1][j1] in shapes.values():
                                        i2 = i1
                                        j2 = j1
                                        shapedir = []
                                        if board[i1][j1] == RD:
                                            shapedir.append('right')
                                            shapedir.append('down')
                                        if board[i1][j1] == RU:
                                            shapedir.append('up')
                                            shapedir.append('right')
                                        if board[i1][j1] == LD:
                                            shapedir.append('left')
                                            shapedir.append('down')
                                        if board[i1][j1] == LU:
                                            shapedir.append('left')
                                            shapedir.append('up')
                                        if board[i1][j1] == H:
                                            shapedir.append('left')
                                            shapedir.append('right')
                                        if board[i1][j1] == V:
                                            shapedir.append('up')
                                            shapedir.append('down')
                                        while len(shapedir) > 1:
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
                                        if len(shapedir) == 1:
                                            change = True
                                            prevsquare = i1,j1
                                            if 'left' in shapedir:
                                                i1 = i1
                                                j1 = j1-1
                                            if 'right' in shapedir:
                                                i1 = i1
                                                j1 = j1+1
                                            if 'up' in shapedir:
                                                i1 = i1-1
                                                j1 = j1
                                            if 'down' in shapedir:
                                                i1 = i1+1
                                                j1 = j1
                                        if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                            break
                                    outofrange = False
                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                        outofrange = True
                                    if outofrange == False and board[i1][j1] == '.':
                                        if i1 == i and j1 == j:
                                            if board[i][j+1] in shapes.values():
                                                shapedir = []
                                                if board[i][j+1] == H:
                                                    shapedir.append('right')
                                                    shapedir.append('left')
                                                if board[i][j+1] == RD:
                                                    shapedir.append('down')
                                                    shapedir.append('right')
                                                if board[i][j+1] == RU:
                                                    shapedir.append('right')
                                                    shapedir.append('up')
                                                if board[i][j+1] == LD:
                                                    shapedir.append('down')
                                                    shapedir.append('left')
                                                if board[i][j+1] == LU:
                                                    shapedir.append('up')
                                                    shapedir.append('left')
                                                if board[i][j+1] == V:
                                                    shapedir.append('down')
                                                    shapedir.append('up')
                                                prevsquare = i,j+1
                                                if shapedir[0] == 'down':
                                                    i1 = i+1
                                                    j1 = j+1
                                                if shapedir[0] == 'right':
                                                    i1 = i
                                                    j1 = j+2
                                                if shapedir[0] == 'up':
                                                    i1 = i-1
                                                    j1 = j+1
                                                outofrange = False
                                                if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                                    outofrange = True  
                                                while outofrange == False and board[i1][j1] in shapes.values():
                                                    i2 = i1
                                                    j2 = j1
                                                    shapedir = []
                                                    if board[i1][j1] == RD:
                                                        shapedir.append('right')
                                                        shapedir.append('down')
                                                    if board[i1][j1] == RU:
                                                        shapedir.append('up')
                                                        shapedir.append('right')
                                                    if board[i1][j1] == LD:
                                                        shapedir.append('left')
                                                        shapedir.append('down')
                                                    if board[i1][j1] == LU:
                                                        shapedir.append('left')
                                                        shapedir.append('up')
                                                    if board[i1][j1] == H:
                                                        shapedir.append('left')
                                                        shapedir.append('right')
                                                    if board[i1][j1] == V:
                                                        shapedir.append('up')
                                                        shapedir.append('down')
                                                    while len(shapedir) > 1:
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
                                                    if len(shapedir) == 1:
                                                        change = True
                                                        prevsquare = i1,j1
                                                        if 'left' in shapedir:
                                                            i1 = i1
                                                            j1 = j1-1
                                                        if 'right' in shapedir:
                                                            i1 = i1
                                                            j1 = j1+1
                                                        if 'up' in shapedir:
                                                            i1 = i1-1
                                                            j1 = j1
                                                        if 'down' in shapedir:
                                                            i1 = i1+1
                                                            j1 = j1
                                                    outofrange = False
                                                    if i1 < 0 or j1 < 0 or i1 >= len(board) or j1 >= len(board):
                                                        outofrange = True
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

                            if len(directions) == 2:
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == i) and (u[1] == j):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((i, j, board[i][j], 1))
                                if directions[0] == 'left' and directions[1] == 'right':
                                    board[i][j] = H
                                    any_changes = True
                                elif directions[0] == 'left' and directions[1] == 'up':
                                    board[i][j] = LU
                                    any_changes = True
                                elif directions[0] == 'left' and directions[1] == 'down':
                                    board[i][j] = LD
                                    any_changes = True
                                elif directions[0] == 'up' and directions[1] == 'down':
                                    board[i][j] = V
                                    any_changes = True
                                elif directions[0] == 'right' and directions[1] == 'up':
                                    board[i][j] = RU
                                    any_changes = True
                                elif directions[0] == 'right' and directions[1] == 'down':
                                    board[i][j] = RD
                                    any_changes = True
                                
            print()
            print("Fifth stage:")
            Solver.print_board(board)

            # if a dot is surrounded by 4 nodes that it cant go into, set impossible
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
                        if len(directions) == 4:
                            #impossible
                            flagimpossible = True

            i,j = start
            previ,prevj = start
            iend,jend = end
            isashape = True
            fromstartcount = 1
            donestart = False

            if j == 0:
                if board[i][j] == H:
                    j = j + 1
                    fromstartcount += 1
                    donestart = True
                if board[i][j] == LU and donestart == False:
                    i = i - 1
                    fromstartcount += 1
                    donestart = True
                if board[i][j] == LD and donestart == False:
                    i = i + 1
                    fromstartcount += 1
                    donestart = True

            if j == len(board) - 1:
                if board[i][j] == H and donestart == False:
                    j = j - 1
                    fromstartcount += 1
                    donestart = True
                if board[i][j] == RU and donestart == False:
                    i = i - 1
                    fromstartcount += 1
                    donestart = True
                if board[i][j] == RD and donestart == False:
                    i = i + 1
                    fromstartcount += 1
                    donestart = True
            
            if i == 0:
                if board[i][j] == V and donestart == False:
                    i = i + 1
                    fromstartcount += 1
                    donestart = True
                if board[i][j] == RU and donestart == False:
                    j = j + 1
                    fromstartcount += 1
                    donestart = True
                if board[i][j] == LU and donestart == False:
                    j = j - 1
                    fromstartcount += 1
                    donestart = True
            
            if i == len(board) - 1:
                if board[i][j] == V and donestart == False:
                    i = i - 1
                    fromstartcount += 1
                    donestart = True
                if board[i][j] == RD and donestart == False:
                    j = j + 1
                    fromstartcount += 1
                    donestart = True
                if board[i][j] == LD and donestart == False:
                    j = j - 1
                    fromstartcount += 1
                    donestart = True

            if board[i][j] in shapes.values():
                isashape = True
            else:
                isashape = False

            while isashape == True and (iend != i or jend != j):
                isashape = False
                done = False
                # if node is an H and prevnode was to the left
                # move right
                if board[i][j] == H and prevj < j:
                    previ = i
                    prevj = j
                    j = j + 1
                    fromstartcount += 1
                    isashape = True
                    done = True
                if board[i][j] == H and prevj > j and done == False:
                    previ = i
                    prevj = j
                    j = j - 1
                    fromstartcount += 1
                    isashape = True
                    done = True
                #if node is a V and prevnode was above
                # move down
                if board[i][j] == V and previ < i and done == False:
                    previ = i
                    prevj = j
                    i = i + 1
                    fromstartcount += 1
                    isashape = True
                    done = True
                if board[i][j] == V and previ > i and done == False:
                    previ = i
                    prevj = j
                    i = i - 1
                    fromstartcount += 1
                    isashape = True
                    done = True

                #if node is a LU and prevnode was to the left
                # move up
                if board[i][j] == LU and prevj < j and done == False:
                    previ = i
                    prevj = j
                    i = i - 1
                    fromstartcount += 1
                    isashape = True
                    done = True
                if board[i][j] == LU and prevj == j and done == False:
                    previ = i
                    prevj = j
                    j = j - 1
                    fromstartcount += 1
                    isashape = True
                    done = True

                #if node is a LD and prevnode was to the left
                # move down
                if board[i][j] == LD and prevj < j and done == False:
                    previ = i
                    prevj = j
                    i = i + 1
                    fromstartcount += 1
                    isashape = True
                    done = True
                if board[i][j] == LD and prevj == j and done == False:
                    previ = i
                    prevj = j
                    j = j - 1
                    fromstartcount += 1
                    isashape = True
                    done = True

                #if node is a RU and prevnode was to the right
                # move up
                if board[i][j] == RU and prevj > j and done == False:
                    previ = i
                    prevj = j
                    i = i - 1
                    fromstartcount += 1
                    isashape = True
                    done = True
                if board[i][j] == RU and prevj == j and done == False:
                    previ = i
                    prevj = j
                    j = j + 1
                    fromstartcount += 1
                    isashape = True
                    done = True

                #if node is a RD and prevnode was to the right
                # move down
                if board[i][j] == RD and prevj > j and done == False:
                    previ = i
                    prevj = j
                    i = i + 1
                    fromstartcount += 1
                    isashape = True
                    done = True
                if board[i][j] == RD and prevj == j and done == False:
                    previ = i
                    prevj = j
                    j = j + 1
                    fromstartcount += 1
                    isashape = True
                    done = True

            if iend == i and jend == j:
                nodenumber = 0
                # for i in column_totals
                # add to nodenumber

                for i in range(len(column_totals)):
                    nodenumber += column_totals[i]

                if fromstartcount != nodenumber:
                    flagimpossible = True
                else:
                    flagimpossible = False
                    any_changes = False
                    print("Solved succesfully")
                    break

            edgerulesneeded = False
            if any_changes == False:
                edgerulesneeded = True
            if edgerulesneeded == True:
                # for top row
                # if rowtotal = 3 and there is one 'V' and one '.' in the row
                # if the node to the left of the dot is X, V, LU, LD
                # change node to the right of the dot to a dot
                # if the node to the right of the dot is X, V, RU, RD
                # change node to the left of the dot to a dot

                # for bottom row
                # if rowtotal = 3 and there is one 'V' and one '.' in the row
                # if the node to the left of the dot is X, V, LU, LD
                # change node to the right of the dot to a dot
                # if the node to the right of the dot is X, V, RU, RD
                # change node to the left of the dot to a dot

                # for left column
                # if columntotal = 3 and there is one 'H' and one '.' in the column
                # if the node above the dot is X, H, RU, LU
                # change node below the dot to a dot
                # if the node below the dot is X, H, RD, LD
                # change node above the dot to a dot

                # for right column
                # if columntotal = 3 and there is one 'H' and one '.' in the column
                # if the node above the dot is X, H, RU, LU
                # change node below the dot to a dot
                # if the node below the dot is X, H, RD, LD
                # change node above the dot to a dot

                if row_totals[0] == 3:
                    # if there is one 'V' and one '.' in the row
                    satisfactory = False
                    count = 0
                    for j in range(len(board)):
                        if board[0][j] == "V":
                            count += 1
                    if count == 1:
                        satisfactory = True

                    if satisfactory == True:
                        satisfactory = False
                        count = 0
                        dotposition = []
                        for j in range(len(board)):
                            if board[0][j] == ".":
                                count += 1
                                dotposition.append(j)
                        if count == 1:
                            satisfactory = True
                    if satisfactory == True:
                        if dotposition[0] - 1 >= 0:
                            if board[0][dotposition[0] - 1] in ["X", "V", "LU", "LD"]:
                                if board[0][dotposition[0] + 1] == "N":
                                    if bruteforceneeded == True:
                                        alreadyreplaced = False
                                        for u in unsures:
                                            if (u[0] == 0) and (u[1] == dotposition[0] + 1):
                                                alreadyreplaced = True
                                        if alreadyreplaced == False:
                                            unsures.append((0, dotposition[0] + 1, board[0][dotposition[0] + 1], 1))
                                    board[0][dotposition[0] + 1] = "."
                                    any_changes = True

                        if dotposition[0] + 1 < len(board):
                            if board[0][dotposition[0] + 1] in ["X", "V", "RU", "RD"]:
                                if board[0][dotposition[0] - 1] == "N":
                                    if bruteforceneeded == True:
                                        alreadyreplaced = False
                                        for u in unsures:
                                            if (u[0] == 0) and (u[1] == dotposition[0] - 1):
                                                alreadyreplaced = True
                                        if alreadyreplaced == False:
                                            unsures.append((0, dotposition[0] - 1, board[0][dotposition[0] - 1], 1))
                                    board[0][dotposition[0] - 1] = "."
                                    any_changes = True

                if row_totals[len(board) - 1] == 3:
                    # if there is one 'V' and one '.' in the row
                    satisfactory = False
                    count = 0
                    for j in range(len(board)):
                        if board[len(board) - 1][j] == "V":
                            count += 1
                    if count == 1:
                        satisfactory = True

                    if satisfactory == True:
                        satisfactory = False
                        count = 0
                        dotposition = []
                        for j in range(len(board)):
                            if board[len(board) - 1][j] == ".":
                                count += 1
                                dotposition.append(j)
                        if count == 1:
                            satisfactory = True
                    if satisfactory == True:
                        if dotposition[0] - 1 >= 0:
                            if board[len(board) - 1][dotposition[0] - 1] in ["X", "V", "LU", "LD"]:
                                if board[len(board) - 1][dotposition[0] + 1] == "N":
                                    if bruteforceneeded == True:
                                        alreadyreplaced = False
                                        for u in unsures:
                                            if (u[0] == len(board) - 1) and (u[1] == dotposition[0] + 1):
                                                alreadyreplaced = True
                                        if alreadyreplaced == False:
                                            unsures.append((len(board) - 1, dotposition[0] + 1, board[len(board) - 1][dotposition[0] + 1], 1))
                                    board[len(board) - 1][dotposition[0] + 1] = "."
                                    any_changes = True

                        if dotposition[0] + 1 < len(board):
                            if board[len(board) - 1][dotposition[0] + 1] in ["X", "V", "RU", "RD"]:
                                if board[len(board) - 1][dotposition[0] - 1] == "N":
                                    if bruteforceneeded == True:
                                        alreadyreplaced = False
                                        for u in unsures:
                                            if (u[0] == len(board) - 1) and (u[1] == dotposition[0] - 1):
                                                alreadyreplaced = True
                                        if alreadyreplaced == False:
                                            unsures.append((len(board) - 1, dotposition[0] - 1, board[len(board) - 1][dotposition[0] - 1], 1))
                                    board[len(board) - 1][dotposition[0] - 1] = "."
                                    any_changes = True

                if column_totals[0] == 3:
                    # if there is one 'H' and one '.' in the column
                    satisfactory = False
                    count = 0
                    for i in range(len(board)):
                        if board[i][0] == "H":
                            count += 1
                    if count == 1:
                        satisfactory = True

                    if satisfactory == True:
                        satisfactory = False
                        count = 0
                        dotposition = []
                        for i in range(len(board)):
                            if board[i][0] == ".":
                                count += 1
                                dotposition.append(i)
                        if count == 1:
                            satisfactory = True
                    if satisfactory == True:
                        if dotposition[0] - 1 >= 0:
                            if board[dotposition[0] - 1][0] in ["X", "H", "RU", "LU"]:
                                if board[dotposition[0] + 1][0] == "N":
                                    if bruteforceneeded == True:
                                        alreadyreplaced = False
                                        for u in unsures:
                                            if (u[0] == dotposition[0] + 1) and (u[1] == 0):
                                                alreadyreplaced = True
                                        if alreadyreplaced == False:
                                            unsures.append((dotposition[0] + 1, 0, board[dotposition[0] + 1][0], 1))
                                    board[dotposition[0] + 1][0] = "."
                                    any_changes = True

                        if dotposition[0] + 1 < len(board):
                            if board[dotposition[0] + 1][0] in ["X", "H", "RD", "LD"]:
                                if board[dotposition[0] - 1][0] == "N":
                                    if bruteforceneeded == True:
                                        alreadyreplaced = False
                                        for u in unsures:
                                            if (u[0] == dotposition[0] - 1) and (u[1] == 0):
                                                alreadyreplaced = True
                                        if alreadyreplaced == False:
                                            unsures.append((dotposition[0] - 1, 0, board[dotposition[0] - 1][0], 1))
                                    board[dotposition[0] - 1][0] = "."
                                    any_changes = True

                if column_totals[len(board) - 1] == 3:
                    # if there is one 'H' and one '.' in the column
                    satisfactory = False
                    count = 0
                    for i in range(len(board)):
                        if board[i][len(board) - 1] == "H":
                            count += 1
                    if count == 1:
                        satisfactory = True

                    if satisfactory == True:
                        satisfactory = False
                        count = 0
                        dotposition = []
                        for i in range(len(board)):
                            if board[i][len(board) - 1] == ".":
                                count += 1
                                dotposition.append(i)
                        if count == 1:
                            satisfactory = True
                    if satisfactory == True:
                        if dotposition[0] - 1 >= 0:
                            if board[dotposition[0] - 1][len(board) - 1] in ["X", "H", "RU", "LU"]:
                                if board[dotposition[0] + 1][len(board) - 1] == "N":
                                    if bruteforceneeded == True:
                                        alreadyreplaced = False
                                        for u in unsures:
                                            if (u[0] == dotposition[0] + 1) and (u[1] == len(board) - 1):
                                                alreadyreplaced = True
                                        if alreadyreplaced == False:
                                            unsures.append((dotposition[0] + 1, len(board) - 1, board[dotposition[0] + 1][len(board) - 1], 1))
                                    board[dotposition[0] + 1][len(board) - 1] = "."
                                    any_changes = True

                        if dotposition[0] + 1 < len(board):
                            if board[dotposition[0] + 1][len(board) - 1] in ["X", "H", "RD", "LD"]:
                                if board[dotposition[0] - 1][len(board) - 1] == "N":
                                    if bruteforceneeded == True:
                                        alreadyreplaced = False
                                        for u in unsures:
                                            if (u[0] == dotposition[0] - 1) and (u[1] == len(board) - 1):
                                                alreadyreplaced = True
                                        if alreadyreplaced == False:
                                            unsures.append((dotposition[0] - 1, len(board) - 1, board[dotposition[0] - 1][len(board) - 1], 1))
                                    board[dotposition[0] - 1][len(board) - 1] = "."
                                    any_changes = True

                ##### STAGE 6 #####
                # for each column
                # if every square in the column is in knowns, add the column to edgecolumns
                # for each row
                # if every square in the row is in knowns, add the row to edgerows
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
                print("Edge columns:", edgecolumns)
                print("Edge rows:", edgerows)

                # for each column
                # if column to the left or right is in edgecolumns, check if the number of 'definites' in the column is equal to the column total - 1
                # if yes, for each square in the column which is 'N' and above or below a dot, add this coordinate to a list
                # if the length of list is 1, change the square to a dot, and change all other 'N's in the column to 'X'
                for j in range(len(board)):
                    if (j - 1 in edgecolumns) or (j + 1 in edgecolumns):
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
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i, j, board[i][j], 1))
                                        board[i][j] = "X"
                                        any_changes = True
                                    
                            if len(dots) == 1:
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == dots[0][0]) and (u[1] == dots[0][1]):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((dots[0][0], dots[0][1], board[dots[0][0]][dots[0][1]], 1))
                                board[dots[0][0]][dots[0][1]] = "."
                                any_changes = True
                                for i in range(len(board)):
                                    if board[i][j] == "N":
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i, j, board[i][j], 1))
                                        board[i][j] = "X"
                                        any_changes = True
                # do the same for rows
                for i in range(len(board)):
                    if (i - 1 in edgerows) or (i + 1 in edgerows):
                        count = 0
                        for j in range(len(board)):
                            if board[i][j] in definites.values():
                                count += 1
                        if count == row_totals[i] - 1:
                            dots = []
                            for j in range(len(board)):
                                if board[i][j] == "N":
                                    possible = False
                                    if j - 1 >= 0 and board[i][j-1] == ".":
                                        dots.append((i, j))
                                        possible = True
                                    if j + 1 < len(board) and board[i][j+1] == ".":
                                        dots.append((i, j))
                                        possible = True
                                    if possible == False:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i, j, board[i][j], 1))
                                        board[i][j] = "X"
                                        any_changes = True
                                    
                            if len(dots) == 1:
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == dots[0][0]) and (u[1] == dots[0][1]):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((dots[0][0], dots[0][1], board[dots[0][0]][dots[0][1]], 1))
                                board[dots[0][0]][dots[0][1]] = "."
                                any_changes = True
                                for j in range(len(board)):
                                    if board[i][j] == "N":
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i, j, board[i][j], 1))
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

                possiblementdown = False
                possiblementup = False
                possibles = 0
                for j in range(len(board)):
                    if j - 1 in edgecolumns and j+1 < len(board) and j-1 >= 0:
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
                                            counter = -10000
                                            break
                                        k += 1
                                        counter += 1
                                    if counter == column_totals[j]:
                                        possiblementdown = True
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
                                    if counter == column_totals[j]:
                                        possiblementup = True
                                        possibles += 1

                            if possibles == 1:
                                if possiblementdown == True:
                                    counter = 1
                                    k = place
                                    while counter < column_totals[j]:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == k) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((k, j, board[k][j], 1))
                                        board[k][j] = "."
                                        k += 1
                                        counter += 1
                                    any_changes = True
                                if possiblementup == True:
                                    counter = 1
                                    k = place
                                    while counter < column_totals[j]:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == k) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((k, j, board[k][j], 1))
                                        board[k][j] = "."
                                        k -= 1
                                        counter += 1
                                    any_changes = True
                                                           
                # do the same for rows
                possiblementright = False
                possiblementleft = False
                possibles = 0
                for i in range(len(board)):
                    if i - 1 in edgerows and i+1 < len(board) and i-1 >= 0:
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
                                            counter = -10000
                                            break
                                        k += 1
                                        counter += 1
                                    if counter == row_totals[i]:
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
                                    if counter == row_totals[i]:
                                        possiblementleft = True
                                        possibles += 1

                            if possibles == 1:
                                if possiblementright == True:
                                    counter = 1
                                    k = place
                                    while counter < row_totals[i]:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == k):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i, k, board[i][k], 1))
                                        board[i][k] = "."
                                        k += 1
                                        counter += 1
                                    any_changes = True
                                if possiblementleft == True:
                                    counter = 1
                                    k = place
                                    while counter < row_totals[i]:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == k):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i, k, board[i][k], 1))
                                        board[i][k] = "."
                                        k -= 1
                                        counter += 1
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
                possiblementdown = False
                possiblementup = False
                possibles = 0
                for j in range(len(board)):
                    if j + 1 in edgecolumns and j-1 >= 0 and j+1 < len(board):
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
                                            counter = -10000
                                            break
                                        k += 1
                                        counter += 1
                                    if counter == column_totals[j]:
                                        possiblementdown = True
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
                                    if counter == column_totals[j]:
                                        possiblementup = True
                                        possibles += 1

                            if possibles == 1:
                                if possiblementdown == True:
                                    counter = 1
                                    k = place
                                    while counter < column_totals[j]:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == k) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((k, j, board[k][j], 1))
                                        board[k][j] = "."
                                        k += 1
                                        counter += 1
                                    any_changes = True
                                if possiblementup == True:
                                    counter = 1
                                    k = place
                                    while counter < column_totals[j]:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == k) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((k, j, board[k][j], 1))
                                        board[k][j] = "."
                                        k -= 1
                                        counter += 1
                                    any_changes = True
                
                # do the same for rows
                possiblementright = False
                possiblementleft = False
                possibles = 0
                for i in range(len(board)):
                    if i + 1 in edgerows and i-1 >= 0 and i + 1 < len(board):
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
                                            counter = -10000
                                            break
                                        k += 1
                                        counter += 1
                                    if counter == row_totals[i]:
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
                                    if counter == row_totals[i]:
                                        possiblementleft = True
                                        possibles += 1

                            if possibles == 1:
                                if possiblementright == True:
                                    counter = 1
                                    k = place
                                    while counter < row_totals[i]:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == k):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i, k, board[i][k], 1))
                                        board[i][k] = "."
                                        k += 1
                                        counter += 1
                                    any_changes = True
                                if possiblementleft == True:
                                    counter = 1
                                    k = place
                                    while counter < row_totals[i]:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == k):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i, k, board[i][k], 1))
                                        board[i][k] = "."
                                        k -= 1
                                        counter += 1
                                    any_changes = True
                
                print("Unique rule used")###
                print()
                Solver.print_board(board)

                ##### other unique rule #####
                # if column to the right has column total = 1
                # if one of the nodes in column is a H, RD, RU
                # make the corresponding node in the column to the right an H

                for j in range(len(board)):
                    if j + 1 < len(board):
                        if column_totals[j+1] == 1:
                            for i in range(len(board)):
                                if board[i][j] == H:
                                    if board[i][j+1] != H:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == j+1):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i,j+1,board[i][j+1],1))
                                        board[i][j+1] = H
                                        any_changes = True
                                if board[i][j] == RD:
                                    if board[i][j+1] != H:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == j+1):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i,j+1,board[i][j+1],1))
                                        board[i][j+1] = H
                                        any_changes = True
                                if board[i][j] == RU:
                                    if board[i][j+1] != H:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == j+1):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i,j+1,board[i][j+1],1))
                                        board[i][j+1] = H
                                        any_changes = True
                
                # do the same for rows
                for i in range(len(board)):
                    if i + 1 < len(board):
                        if row_totals[i+1] == 1:
                            for j in range(len(board)):
                                if board[i][j] == V:
                                    if board[i+1][j] != V:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i+1) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i+1,j,board[i+1][j],1))
                                        board[i+1][j] = V
                                        any_changes = True
                                if board[i][j] == RD:
                                    if board[i+1][j] != V:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i+1) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i+1,j,board[i+1][j],1))
                                        board[i+1][j] = V
                                        any_changes = True
                                if board[i][j] == LD:
                                    if board[i+1][j] != V:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i+1) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i+1,j,board[i+1][j],1))
                                        board[i+1][j] = V
                                        any_changes = True
                # do the same but swap left and right
                # if column to the left has column total = 1
                # if one of the nodes in column is a H, LD, LU
                # make the corresponding node in the column to the left an H
                for j in range(len(board)):
                    if j - 1 >= 0:
                        if column_totals[j-1] == 1:
                            for i in range(len(board)):
                                if board[i][j] == H:
                                    if board[i][j-1] != H:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == j-1):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i,j-1,board[i][j-1],1))
                                        board[i][j-1] = H
                                        any_changes = True
                                if board[i][j] == LD:
                                    if board[i][j-1] != H:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == j-1):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i,j-1,board[i][j-1],1))
                                        board[i][j-1] = H
                                        any_changes = True
                                if board[i][j] == LU:
                                    if board[i][j-1] != H:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == j-1):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i,j-1,board[i][j-1],1))
                                        board[i][j-1] = H
                                        any_changes = True
                
                # do the same for rows
                for i in range(len(board)):
                    if i - 1 >= 0:
                        if row_totals[i-1] == 1:
                            for j in range(len(board)):
                                if board[i][j] == V:
                                    if board[i-1][j] != V:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i-1) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i-1,j,board[i-1][j],1))
                                        board[i-1][j] = V
                                        any_changes = True
                                if board[i][j] == RU:
                                    if board[i-1][j] != V:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i-1) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i-1,j,board[i-1][j],1))
                                        board[i-1][j] = V
                                        any_changes = True
                                if board[i][j] == LU:
                                    if board[i-1][j] != V:
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i-1) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i-1,j,board[i-1][j],1))
                                        board[i-1][j] = V
                                        any_changes = True

                print("Unique rule used")
                print()
                Solver.print_board(board)

                # unique rule
                # if 2nd column has column total = 2
                # if start and end are not in column 2
                # if there is exactly one dot in column 2
                # make the dot an H
                if column_totals[1] == 2:
                    if any_changes == False:
                        # if column 1 has no shapes
                        count = 0
                        
                        for i in range(len(board)):
                            if board[i][0] in shapes.values():
                                count += 1
                        if count == 0:
                            satisfactory = False
                            count = 0
                            dotpos = []
                            for i in range(len(board)):
                                if board[i][1] == ".":
                                    count += 1
                                    dotpos.append(i)

                            if count == 1:
                                satisfactory = True
                            if satisfactory == True:
                                # change the dot in column 2 to an H
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == dotpos[0]) and (u[1] == 1):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((dotpos[0], 1, board[dotpos[0]][1], 1))
                                board[dotpos[0]][1] = H
                                any_changes = True

                # if 2nd row has row total = 2
                # if start and end are not in row 2
                # if there is exactly one dot in row 2
                # make the dot a V
                if row_totals[1] == 2:
                    if any_changes == False:
                        count = 0
                        # if row 1 has no shapes
                        for j in range(len(board)):
                            if board[0][j] in shapes.values():
                                count += 1
                        if count == 0:
                            satisfactory = False
                            count = 0
                            dotpos = []
                            for j in range(len(board)):
                                if board[1][j] == ".":
                                    count += 1
                                    dotpos.append(j)

                            if count == 1:
                                satisfactory = True
                            if satisfactory == True:
                                # change the dot in row 2 to a V
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == 1) and (u[1] == dotpos[0]):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((1, dotpos[0], board[1][dotpos[0]], 1))
                                board[1][dotpos[0]] = V
                                any_changes = True

                # if penultimate column has column total = 2
                # if start and end are not in penultimate column
                # if there is exactly one dot in penultimate column
                # make the dot an H
                if column_totals[len(board) - 2] == 2:
                    if any_changes == False:
                        # if last column has no shapes
                        count = 0
                        for i in range(len(board)):
                            if board[i][len(board) - 1] in shapes.values():
                                count += 1
                        if count == 0:
                            satisfactory = False
                            count = 0
                            dotpos = []
                            for i in range(len(board)):
                                if board[i][len(board) - 2] == ".":
                                    count += 1
                                    dotpos.append(i)

                            if count == 1:
                                satisfactory = True
                            if satisfactory == True:
                                # change the dot in penultimate column to an H
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == dotpos[0]) and (u[1] == len(board) - 2):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((dotpos[0], len(board) - 2, board[dotpos[0]][len(board) - 2], 1))
                                board[dotpos[0]][len(board) - 2] = H
                                any_changes = True

                # if penultimate row has row total = 2
                # if start and end are not in penultimate row
                # if there is exactly one dot in penultimate row
                # make the dot a V
                if row_totals[len(board) - 2] == 2:
                    if any_changes == False:
                        # if last row has no shapes
                        count = 0
                        for j in range(len(board)):
                            if board[len(board) - 1][j] in shapes.values():
                                count += 1
                        if count == 0:
                            satisfactory = False
                            count = 0
                            dotpos = []
                            for j in range(len(board)):
                                if board[len(board) - 2][j] == ".":
                                    count += 1
                                    dotpos.append(j)

                            if count == 1:
                                satisfactory = True
                            if satisfactory == True:
                                # change the dot in penultimate row to a V
                                if bruteforceneeded == True:
                                    alreadyreplaced = False
                                    for u in unsures:
                                        if (u[0] == len(board) - 2) and (u[1] == dotpos[0]):
                                            alreadyreplaced = True
                                    if alreadyreplaced == False:
                                        unsures.append((len(board) - 2, dotpos[0], board[len(board) - 2][dotpos[0]], 1))
                                board[len(board) - 2][dotpos[0]] = V
                                any_changes = True

            if column_totals[1] == 2:
                if any_changes == False:
                    satisfactory = False
                    count = 0
                    for i in range(len(board)):
                        if board[i][1] == H:
                            count += 1
                    if count == 1:
                        for i in range(len(board)):
                            if board[i][1] in definites.values() and board[i][1] != H:
                                satisfactory = False
                        if satisfactory == True:
                            for i in range(len(board)):
                                #if node is a LD or RD, make the nodes above the node Xs
                                # if node is a LU or RU, make the nodes below the node Xs

                                if (board[i][0] == LD) or (board[i][0] == RD):
                                    while i < 0:
                                        i -= 1
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == 0):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i, 0, board[i][0], 1))
                                        board[i][0] = "X"
                                        any_changes = True

                                if (board[i][0] == LU) or (board[i][0] == RU):
                                    while i < len(board):
                                        i += 1
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == 0):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i, 0, board[i][0], 1))
                                        board[i][0] = "X"
                                        any_changes = True
                                
                            # if Xs in column[0] = len(board) - column_totals[0]
                            # continue
                            # else
                            # find the first shape in column[0]
                            # if the shape is a LD or RD
                            # countercolumn = 1
                            # while countercolumn < column_totals[0]
                            # go down making each node a dot

                            # if the shape is a LU or RU
                            # countercolumn = 1
                            # while countercolumn < column_totals[0]
                            # go up making each node a dot
                            # if the shape is a V
                            #continue

                            for i in range(len(board)):
                                if board[i][0] == "X":
                                    count += 1
                            if count != len(board) - column_totals[0]:
                                found = False
                                for i in range(len(board)):
                                    if board[i][0] in shapes.values():
                                        found = True
                                        if board[i][0] == LD or board[i][0] == RD:
                                            counter = 2
                                            k = i + 1
                                            while counter <= column_totals[0]:
                                                if k >= len(board):
                                                    break

                                                if bruteforceneeded == True:
                                                    alreadyreplaced = False
                                                    for u in unsures:
                                                        if (u[0] == k) and (u[1] == 0):
                                                            alreadyreplaced = True
                                                    if alreadyreplaced == False:
                                                        unsures.append((k, 0, board[k][0], 1))
                                                board[k][0] = "."
                                                k += 1
                                                counter += 1
                                                any_changes = True
                                        if board[i][0] == LU or board[i][0] == RU:
                                            counter = 2
                                            k = i - 1
                                            while counter <= column_totals[0]:
                                                if k < 0:
                                                    break
                                                if bruteforceneeded == True:
                                                    alreadyreplaced = False
                                                    for u in unsures:
                                                        if (u[0] == k) and (u[1] == 0):
                                                            alreadyreplaced = True
                                                    if alreadyreplaced == False:
                                                        unsures.append((k, 0, board[k][0], 1))
                                                board[k][0] = "."
                                                k -= 1
                                                counter += 1
                                                any_changes = True

            if row_totals[1] == 2:
                if any_changes == False:
                    satisfactory = False
                    count = 0
                    for j in range(len(board)):
                        if board[1][j] == V:
                            count += 1
                    if count == 1:
                        for j in range(len(board)):
                            if board[1][j] in definites.values() and board[1][j] != V:
                                satisfactory = False
                        if satisfactory == True:
                            for j in range(len(board)):
                                if (board[0][j] == H) or (board[0][j] == RD) or (board[0][j] == RU):
                                    while j < 0:
                                        j -= 1
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == 0) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((0, j, board[0][j], 1))
                                        board[0][j] = "X"
                                        any_changes = True
                                if (board[0][j] == LD) or (board[0][j] == RD):
                                    while j < len(board):
                                        j += 1
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == 0) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((0, j, board[0][j], 1))
                                        board[0][j] = "X"
                                        any_changes = True

                            # if Xs in row[0] = len(board) - row_totals[0]
                            # continue
                            # else
                            # find the first shape in row[0]
                            # if the shape is a RD or RU
                            # countercolumn = 1
                            # while countercolumn < row_totals[0]
                            # go right making each node a dot
                            # if the shape is a LD or LU
                            # countercolumn = 1
                            # while countercolumn < row_totals[0]
                            # go left making each node a dot
                            # if the shape is a H
                            #continue

                            for j in range(len(board)):
                                if board[0][j] == "X":
                                    count += 1
                            if count != len(board) - row_totals[0]:
                                found = False
                                for j in range(len(board)):
                                    if board[0][j] in shapes.values():
                                        found = True
                                        if board[0][j] == RD or board[0][j] == RU:
                                            counter = 2
                                            k = j + 1
                                            while counter <= row_totals[0]:
                                                if k >= len(board):
                                                    break
                                                if bruteforceneeded == True:
                                                    alreadyreplaced = False
                                                    for u in unsures:
                                                        if (u[0] == 0) and (u[1] == k):
                                                            alreadyreplaced = True
                                                    if alreadyreplaced == False:
                                                        unsures.append((0, k, board[0][k], 1))
                                                board[0][k] = "."
                                                k += 1
                                                counter += 1
                                                any_changes = True
                                        if board[0][j] == LD or board[0][j] == LU:
                                            counter = 2
                                            k = j - 1
                                            while counter <= row_totals[0]:
                                                if k < 0:
                                                    break
                                                if bruteforceneeded == True:
                                                    alreadyreplaced = False
                                                    for u in unsures:
                                                        if (u[0] == 0) and (u[1] == k):
                                                            alreadyreplaced = True
                                                    if alreadyreplaced == False:
                                                        unsures.append((0, k, board[0][k], 1))
                                                board[0][k] = "."
                                                k -= 1
                                                counter += 1
                                                any_changes = True

            if column_totals[len(board) - 2] == 2:
                if any_changes == False:
                    satisfactory = True
                    count = 0
                    for i in range(len(board)):
                        if board[i][len(board) - 2] == H:
                            count += 1
                    if count == 1:
                        for i in range(len(board)):
                            if board[i][len(board) - 2] in definites.values() and board[i][len(board) - 2] != H:
                                satisfactory = False
                        if satisfactory == True:
                            for i in range(len(board)):
                                if (board[i][len(board) - 1] == LD) or (board[i][len(board) - 1] == RD):
                                    while i < 0:
                                        i -= 1
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == len(board) - 1):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i, len(board) - 1, board[i][len(board) - 1], 1))
                                        board[i][len(board) - 1] = "X"
                                        any_changes = True
                                if (board[i][len(board) - 1] == LU) or (board[i][len(board) - 1] == RU):
                                    while i < len(board):
                                        i += 1
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == i) and (u[1] == len(board) - 1):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((i, len(board) - 1, board[i][len(board) - 1], 1))
                                        board[i][len(board) - 1] = "X"
                                        any_changes = True

                            # if Xs in column[len(board) - 1] = len(board) - column_totals[len(board) - 1]
                            # continue
                            # else
                            # find the first shape in column[len(board) - 1]
                            # if the shape is a LD or RD
                            # countercolumn = 1
                            # while countercolumn < column_totals[len(board) - 1]
                            # go down making each node a dot
                            # if the shape is a LU or RU
                            # countercolumn = 1
                            # while countercolumn < column_totals[len(board) - 1]
                            # go up making each node a dot
                            # if the shape is a V
                            #continue

                            for i in range(len(board)):
                                if board[i][len(board) - 1] == "X":
                                    count += 1
                            if count != len(board) - column_totals[len(board) - 1]:
                                found = False
                                for i in range(len(board)):
                                    if board[i][len(board) - 1] in shapes.values():
                                        found = True
                                        if board[i][len(board) - 1] == LD or board[i][len(board) - 1] == RD:
                                            counter = 2
                                            k = i + 1
                                            while counter <= column_totals[len(board) - 1]:
                                                if k >= len(board):
                                                    break
                                                if bruteforceneeded == True:
                                                    alreadyreplaced = False
                                                    for u in unsures:
                                                        if (u[0] == k) and (u[1] == len(board) - 1):
                                                            alreadyreplaced = True
                                                    if alreadyreplaced == False:
                                                        unsures.append((k, len(board) - 1, board[k][len(board) - 1], 1))
                                                board[k][len(board) - 1] = "."
                                                k += 1
                                                counter += 1
                                                any_changes = True
                                        if board[i][len(board) - 1] == LU or board[i][len(board) - 1] == RU:
                                            counter = 2
                                            k = i - 1
                                            while counter <= column_totals[len(board) - 1]:
                                                if k < 0:
                                                    break
                                                if bruteforceneeded == True:
                                                    alreadyreplaced = False
                                                    for u in unsures:
                                                        if (u[0] == k) and (u[1] == len(board) - 1):
                                                            alreadyreplaced = True
                                                    if alreadyreplaced == False:
                                                        unsures.append((k, len(board) - 1, board[k][len(board) - 1], 1))
                                                board[k][len(board) - 1] = "."
                                                k -= 1
                                                counter += 1
                                                any_changes = True

            if row_totals[len(board) - 2] == 2:
                if any_changes == False:
                    satisfactory = False
                    count = 0
                    for j in range(len(board)):
                        if board[len(board) - 2][j] == V:
                            count += 1
                    if count == 1:
                        for j in range(len(board)):
                            if board[len(board) - 2][j] in definites.values() and board[len(board) - 2][j] != V:
                                satisfactory = False
                        if satisfactory == True:
                            for j in range(len(board)):
                                if (board[len(board) - 1][j] == LD) or (board[len(board) - 1][j] == RD):
                                    while j < 0:
                                        j -= 1
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == len(board) - 1) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((len(board) - 1, j, board[len(board) - 1][j], 1))
                                        board[len(board) - 1][j] = "X"
                                        any_changes = True
                                if (board[len(board) - 1][j] == LU) or (board[len(board) - 1][j] == RU):
                                    while j < len(board):
                                        j += 1
                                        if bruteforceneeded == True:
                                            alreadyreplaced = False
                                            for u in unsures:
                                                if (u[0] == len(board) - 1) and (u[1] == j):
                                                    alreadyreplaced = True
                                            if alreadyreplaced == False:
                                                unsures.append((len(board) - 1, j, board[len(board) - 1][j], 1))
                                        board[len(board) - 1][j] = "X"
                                        any_changes = True

                            # if Xs in row[len(board) - 1] = len(board) - row_totals[len(board) - 1]
                            # continue
                            # else
                            # find the first shape in row[len(board) - 1]
                            # if the shape is a LD or RD
                            # countercolumn = 1
                            # while countercolumn < row_totals[len(board) - 1]
                            # go down making each node a dot
                            # if the shape is a LU or RU
                            # countercolumn = 1
                            # while countercolumn < row_totals[len(board) - 1]
                            # go up making each node a dot
                            # if the shape is a H
                            #continue

                            for j in range(len(board)):
                                if board[len(board) - 1][j] == "X":
                                    count += 1
                            if count != len(board) - row_totals[len(board) - 1]:
                                found = False
                                for j in range(len(board)):
                                    if board[len(board) - 1][j] in shapes.values():
                                        found = True
                                        if board[len(board) - 1][j] == LD or board[len(board) - 1][j] == RD:
                                            counter = 2
                                            k = j + 1
                                            while counter <= row_totals[len(board) - 1]:
                                                if k >= len(board):
                                                    break
                                                if bruteforceneeded == True:
                                                    alreadyreplaced = False
                                                    for u in unsures:
                                                        if (u[0] == len(board) - 1) and (u[1] == k):
                                                            alreadyreplaced = True
                                                    if alreadyreplaced == False:
                                                        unsures.append((len(board) - 1, k, board[len(board) - 1][k], 1))
                                                board[len(board) - 1][k] = "."
                                                k += 1
                                                counter += 1
                                                any_changes = True
                                        if board[len(board) - 1][j] == LU or board[len(board) - 1][j] == RU:
                                            counter = 2
                                            k = j - 1
                                            while counter <= row_totals[len(board) - 1]:
                                                if k < 0:
                                                    break
                                                if bruteforceneeded == True:
                                                    alreadyreplaced = False
                                                    for u in unsures:
                                                        if (u[0] == len(board) - 1) and (u[1] == k):
                                                            alreadyreplaced = True
                                                    if alreadyreplaced == False:
                                                        unsures.append((len(board) - 1, k, board[len(board) - 1][k], 1))
                                                board[len(board) - 1][k] = "."
                                                k -= 1
                                                counter += 1
                                                any_changes = True

            #for each column which has column total = 1
            # for each node in the column
            # if the node to the left is an X, LU,LD,V or the node to the right is an X, RU, RD, V
            # make the node an X

            for j in range(len(board)):
                if column_totals[j] == 1:
                    for i in range(len(board)):
                        if j - 1 >= 0 and (board[i][j-1] == "X" or board[i][j-1] == LU or board[i][j-1] == LD or board[i][j-1] == V):
                            if bruteforceneeded == True:
                                alreadyreplaced = False
                                for u in unsures:
                                    if (u[0] == i) and (u[1] == j):
                                        alreadyreplaced = True
                                if alreadyreplaced == False:
                                    unsures.append((i, j, board[i][j], 1))
                            if board[i][j] != "X":
                                any_changes = True
                            board[i][j] = "X"
                        if j + 1 < len(board) and (board[i][j+1] == "X" or board[i][j+1] == RU or board[i][j+1] == RD or board[i][j+1] == V):
                            if bruteforceneeded == True:
                                alreadyreplaced = False
                                for u in unsures:
                                    if (u[0] == i) and (u[1] == j):
                                        alreadyreplaced = True
                                if alreadyreplaced == False:
                                    unsures.append((i, j, board[i][j], 1))
                            if board[i][j] != "X":
                                any_changes = True
                            board[i][j] = "X"

            # do the same for rows
            for i in range(len(board)):
                if row_totals[i] == 1:
                    for j in range(len(board)):
                        if i - 1 >= 0 and (board[i-1][j] == "X" or board[i-1][j] == LU or board[i-1][j] == RU or board[i-1][j] == H):
                            if bruteforceneeded == True:
                                alreadyreplaced = False
                                for u in unsures:
                                    if (u[0] == i) and (u[1] == j):
                                        alreadyreplaced = True
                                if alreadyreplaced == False:
                                    unsures.append((i, j, board[i][j], 1))
                            if board[i][j] != "X":
                                any_changes = True
                            board[i][j] = "X"
                        if i + 1 < len(board) and (board[i+1][j] == "X" or board[i+1][j] == LD or board[i+1][j] == RD or board[i+1][j] == H):
                            if bruteforceneeded == True:
                                alreadyreplaced = False
                                for u in unsures:
                                    if (u[0] == i) and (u[1] == j):
                                        alreadyreplaced = True
                                if alreadyreplaced == False:
                                    unsures.append((i, j, board[i][j], 1))
                            if board[i][j] != "X":
                                any_changes = True
                            board[i][j] = "X"



            # for each shape in grid
            # determine what directions the shape goes in
            # check if the shape in each direction is a compatible shape

            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] in shapes.values():
                        shapedirections = []
                        if board[i][j] == H:
                            shapedirections.append('left')
                            shapedirections.append('right')
                        if board[i][j] == V:
                            shapedirections.append('up')
                            shapedirections.append('down')
                        if board[i][j] == RD:
                            shapedirections.append('right')
                            shapedirections.append('down')
                        if board[i][j] == RU:
                            shapedirections.append('right')
                            shapedirections.append('up')
                        if board[i][j] == LD:
                            shapedirections.append('left')
                            shapedirections.append('down')
                        if board[i][j] == LU:
                            shapedirections.append('left')
                            shapedirections.append('up')
                        for direction in shapedirections:
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


            if flagimpossible == True:
                trynew = True
                        
            edgerulesneeded = False
            if any_changes == False:
                print("No changes made, entering guessing stage")
                bruteforceneeded = True

            if (bruteforceneeded == True and any_changes == False) or trynew == True:
                print("Brute force needed")

                # reverse unsures

                unsures = unsures[::-1]
                ####add all unsures back to board in reverse order
                for unsure in unsures:
                    board[unsure[0]][unsure[1]] = unsure[2]
                unsures = []


                if trynew == True:
                    if trysecond == False:
                        unsureshapes.pop(0)
                    if trysecond == True:
                        unsureshapes.pop(1)
                    trysecond = False

                if len(unsureshapes) == 1:
                    # make the board square of save_state the shape in unsureshapes
                    board[save_state[0]][save_state[1]] = unsureshapes[0]
                    unsureshapes.pop(0)
                    trynew = False
                    any_changes = True
                    bruteforceneeded = False


                if len(unsureshapes) == 2:
                    if trysecond == False:
                        trysecond = True
                        any_changes = True
                    else:
                        board[save_state[0]][save_state[1]] = save_state[2]
                        trysecond = False


                if trysecond == True:
                    board[nodeguess[0]][nodeguess[1]] = nodeguess[3]


                ###### brute force ######

                #for dot in board
                # find the number of possible shapes that can go in the dot
                # if only one possible shape, change the dot to that shape
                # if two possible shapes, add a tuple to 'dots_two' in the form (i, j, shape1, shape2)
                
                if minicount == 0 and trysecond == False and any_changes == False:
                    minicount += 1
                    any_changes = False
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

                #reverse dotstwo

                dots_two = dots_two[::-1]

                # for d in dots_two
                # if d[0], d[1] not in dots_two_possibles
                # add d[0], d[1] to dots_two_possibles
                # else remove d from dots_two

                dots_two_possibles = []
                for d in dots_two:
                    if (d[0], d[1]) not in dots_two_possibles:
                        dots_two_possibles.append((d[0], d[1]))
                    else:
                        dots_two.remove(d)

                print(dots_two)


                if any_changes == False:
                    unsureshapes = []
                    ##### nodeguess = first node in dots_two
                    # change the board position designated by the first and second parts of nodeguess to the first shape in the third part of nodeguess
                    # add both shapes to 'unsureshapes'
                    # save old state of board square to save_state

                    ## save state includes the coordinates of the node, and the shape of the node
                    save_state = [dots_two[0][0], dots_two[0][1], board[dots_two[0][0]][dots_two[0][1]]]

                    nodeguess = dots_two[0]
                    board[nodeguess[0]][nodeguess[1]] = nodeguess[2]
                    unsureshapes.append(nodeguess[2])
                    unsureshapes.append(nodeguess[3])
                    dots_two.pop(0)


                print("Brute force used")




board, start, end = Solver.generate_board()
Solver.Solve(board, start, end)