import random

# Box drawing characters: ┌ ┐ └ ┘ ─ │ ┬ ┴ ├ ┤ ┼

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
        size = int(input("Enter the size of the board: "))
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
            #asks user if there are any more nodes to add
            #if yes, asks for position and character
            #if no, breaks the loop
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
        edgerulesneeded = False

        any_changes = True
        while any_changes:
            any_changes = False
            edgerulesneeded = False
            RD = "┌"
            LD = "┐"
            RU = "└"
            LU = "┘"
            H = "─"
            V = "│"
            DOT = "."
            NULL = "N"
            X = "X"
            
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


            # First stage: change all 0s which connect to a start or end node to '.'
            # Print the board and solve first stage
            print("Initial board:")
            Solver.print_board(board)
            print("\nFirst stage:")

            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] in Solver.characters.values():
                        if board[i][j] == Solver.RD:
                            if i + 1 < len(board) and board[i + 1][j] == "N":
                                board[i + 1][j] = '.'
                                any_changes = True
                            if j + 1 < len(board) and board[i][j + 1] == "N":
                                board[i][j + 1] = '.'
                                any_changes = True
                        elif board[i][j] == Solver.LD:
                            if i + 1 < len(board) and board[i + 1][j] == "N":
                                board[i + 1][j] = '.'
                                any_changes = True
                            if j - 1 >= 0 and board[i][j - 1] == "N":
                                board[i][j - 1] = '.'
                                any_changes = True
                        elif board[i][j] == Solver.RU:
                            if i - 1 >= 0 and board[i - 1][j] == "N":
                                board[i - 1][j] = '.'
                                any_changes = True
                            if j + 1 < len(board) and board[i][j + 1] == "N":
                                board[i][j + 1] = '.'
                                any_changes = True
                        elif board[i][j] == Solver.LU:
                            if i - 1 >= 0 and board[i - 1][j] == "N":
                                board[i - 1][j] = '.'
                                any_changes = True
                            if j - 1 >= 0 and board[i][j - 1] == "N":
                                board[i][j - 1] = '.'
                                any_changes = True
                        elif board[i][j] == Solver.H:
                            if j + 1 < len(board) and board[i][j + 1] == "N":
                                board[i][j + 1] = '.'
                                any_changes = True
                            if j - 1 >= 0 and board[i][j - 1] == "N":
                                board[i][j - 1] = '.'
                                any_changes = True
                        elif board[i][j] == Solver.V:
                            if i + 1 < len(board) and board[i + 1][j] == "N":
                                board[i + 1][j] = '.'
                                any_changes = True
                            if i - 1 >= 0 and board[i - 1][j] == "N":
                                board[i - 1][j] = '.'
                                any_changes = True

            Solver.print_board(board)
            # Second stage: check each column to see if all possible nodes are used
            column_totals = [5,5,3,5,4,5,5,2]
            row_totals = [2,4,5,5,4,4,3,7]

            

            changed = True
            while changed == True:
                changed = False

                ######## Check each column ########
                for j in range(len(board)):
                    count = 0
                    for i in range(len(board)):
                        if board[i][j] in definites.values():
                            count += 1
                    if count == column_totals[j]:
                        for i in range(len(board)):
                            if board[i][j] == "N":
                                board[i][j] = 'X'
                                changed = True
                                any_changes = True
                
                #do the same for rows
                for i in range(len(board)):
                    count = 0
                    for j in range(len(board)):
                        if board[i][j] in definites.values():
                            count += 1
                    if count == row_totals[i]:
                        for j in range(len(board)):
                            if board[i][j] == "N":
                                board[i][j] = 'X'
                                changed = True
                                any_changes = True

                # if number of non-Xs in each column is equal to the column total, change all 0s to dots
                for j in range(len(board)):
                    count = 0
                    for i in range(len(board)):
                        if board[i][j] != 'X':
                            count += 1
                    if count == column_totals[j]:
                        for i in range(len(board)):
                            if board[i][j] == "N":
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
                                board[i][j] = '.'
                                changed = True
                                any_changes = True



            print()
            print("Second stage:")
            Solver.print_board(board)


            ###### THIRD STAGE

            # for each dot in the grid
            # if it is adjacent to 2 from 'characters', change it the character which fits the pattern
            # if square to the left is H, RD, or RU, and square to the right is H, LD, or LU, then change dot to H
            # if square to the left is H, RD, or RU, and square above is V, RD, or LD, then change dot to LU
            # if square to the left is H, RD or RU, and square below is V, RU, or LU, then change dot to LD
            # if square above is V, RD, or LD, and square below is V, RU, or LU, then change dot to V
            # if square to the right is H, LD, or LU, and square above is V, RD, or LD, then change dot to RU
            # if square to the right is H, LD, or LU, and square below is V, RU, or LU, then change dot to RD
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
                            elif directions[0] == 'up' and directions[1] == 'right':
                                board[i][j] = RU
                                any_changes = True
                            elif directions[0] == 'down' and directions[1] == 'right':
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
            # for each empty/null square in the grid
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
                                board[i][j] = 'X'
                                changed = True
                                any_changes = True
            print()
            print("Fourth stage:")
            Solver.print_board(board)


                
            ##### STAGE 5
            # for each dot in the grid
            # if it is adjacent to exactly 2 from 'characters', change it the character which fits the pattern
            # if square to the left is H, RD, or RU, and square to the right is H, LD, or LU, then change dot to H
            # if square to the left is H, RD, or RU, and square above is V, RD, or LD, then change dot to LU
            # if square to the left is H, RD or RU, and square below is V, RU, or LU, then change dot to LD
            # if square above is V, RD, or LD, and square below is V, RU, or LU, then change dot to V
            # if square to the right is H, LD, or LU, and square above is V, RD, or LD, then change dot to RU
            # if square to the right is H, LD, or LU, and square below is V, RU, or LU, then change dot to RD
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] == '.':
                        ########
                        #check each direction
                        ########
                        #use a count to check how many characters from indefinites are adjacent to the dot
                        count = 0
                        directions = []
                        #check if the square to the left is a character
                        if j - 1 >= 0 and ((board[i][j-1] == H) or (board[i][j-1] == RD) or (board[i][j-1] == RU) or (board[i][j-1] == '.') or (board[i][j-1] == "N")):
                            count += 1
                            directions.append('left')
                        #check if the square to the right is a character
                        if j + 1 < len(board) and ((board[i][j+1] == H) or (board[i][j+1] == LD) or (board[i][j+1] == LU) or (board[i][j+1] == '.') or (board[i][j+1] == "N")):
                            count += 1
                            directions.append('right')
                        #check if the square above is a character
                        if i - 1 >= 0 and ((board[i-1][j] == V) or (board[i-1][j] == RD) or (board[i-1][j] == LD) or (board[i-1][j] == '.') or (board[i-1][j] == "N")):
                            count += 1
                            directions.append('up')
                        #check if the square below is a character
                        if i + 1 < len(board) and ((board[i+1][j] == V) or (board[i+1][j] == RU) or (board[i+1][j] == LU) or (board[i+1][j] == '.') or (board[i+1][j] == "N")):
                            count += 1
                            directions.append('down')
                        #if there are exactly 2 characters adjacent to the dot
                        # draw the appropriate character
                        if count == 2:
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
                                                    #remove left from shapedir
                                                    shapedir.remove('left')
                                                j2 = j2 + 1
                                            if 'right' in shapedir:
                                                i2 = i2
                                                j2 = j2+1
                                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                    #remove right from shapedir
                                                    shapedir.remove('right')
                                                j2 = j2 - 1
                                            if 'up' in shapedir:
                                                i2 = i2-1
                                                j2 = j2
                                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                    #remove up from shapedir
                                                    shapedir.remove('up')
                                                i2 = i2 + 1
                                            if 'down' in shapedir:
                                                i2 = i2+1
                                                j2 = j2
                                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                    #remove down from shapedir
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
                                                                #remove left from shapedir
                                                                shapedir.remove('left')
                                                            j2 = j2 + 1
                                                        if 'right' in shapedir:
                                                            i2 = i2
                                                            j2 = j2+1
                                                            if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                                #remove right from shapedir
                                                                shapedir.remove('right')
                                                            j2 = j2 - 1
                                                        if 'up' in shapedir:
                                                            i2 = i2-1
                                                            j2 = j2
                                                            if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                                #remove up from shapedir
                                                                shapedir.remove('up')
                                                            i2 = i2 + 1
                                                        if 'down' in shapedir:
                                                            i2 = i2+1
                                                            j2 = j2
                                                            if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                                #remove down from shapedir
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
                                        directions.remove('right')
                                    if outofrange == False and i+1 == i1 and j == j1 and change == True:
                                        directions.remove('down')
                                    if outofrange == False and i-1 == i1 and j == j1 and change == True:
                                        directions.remove('up')
                                    if outofrange == False and i == i1 and j-1 == j1 and change == True:
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
                                                    #remove left from shapedir
                                                    shapedir.remove('left')
                                                j2 = j2 + 1
                                            if 'right' in shapedir:
                                                i2 = i2
                                                j2 = j2+1
                                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                    #remove right from shapedir
                                                    shapedir.remove('right')
                                                j2 = j2 - 1
                                            if 'up' in shapedir:
                                                i2 = i2-1
                                                j2 = j2
                                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                    #remove up from shapedir
                                                    shapedir.remove('up')
                                                i2 = i2 + 1
                                            if 'down' in shapedir:
                                                i2 = i2+1
                                                j2 = j2
                                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                    #remove down from shapedir
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
                                                                #remove left from shapedir
                                                                shapedir.remove('left')
                                                            j2 = j2 + 1
                                                        if 'right' in shapedir:
                                                            i2 = i2
                                                            j2 = j2+1
                                                            if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                                #remove right from shapedir
                                                                shapedir.remove('right')
                                                            j2 = j2 - 1
                                                        if 'up' in shapedir:
                                                            i2 = i2-1
                                                            j2 = j2
                                                            if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                                #remove up from shapedir
                                                                shapedir.remove('up')
                                                            i2 = i2 + 1
                                                        if 'down' in shapedir:
                                                            i2 = i2+1
                                                            j2 = j2
                                                            if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                                #remove down from shapedir
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
                                        directions.remove('right')
                                    if outofrange == False and i+1 == i1 and j == j1 and change == True:
                                        directions.remove('down')
                                    if outofrange == False and i-1 == i1 and j == j1 and change == True:
                                        directions.remove('up')
                                    if outofrange == False and i == i1 and j-1 == j1 and change == True:
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
                                                    #remove left from shapedir
                                                    shapedir.remove('left')
                                                j2 = j2 + 1
                                            if 'right' in shapedir:
                                                i2 = i2
                                                j2 = j2+1
                                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                    #remove right from shapedir
                                                    shapedir.remove('right')
                                                j2 = j2 - 1
                                            if 'up' in shapedir:
                                                i2 = i2-1
                                                j2 = j2
                                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                    #remove up from shapedir
                                                    shapedir.remove('up')
                                                i2 = i2 + 1
                                            if 'down' in shapedir:
                                                i2 = i2+1
                                                j2 = j2
                                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                    #remove down from shapedir
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
                                                                #remove left from shapedir
                                                                shapedir.remove('left')
                                                            j2 = j2 + 1
                                                        if 'right' in shapedir:
                                                            i2 = i2
                                                            j2 = j2+1
                                                            if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                                #remove right from shapedir
                                                                shapedir.remove('right')
                                                            j2 = j2 - 1
                                                        if 'up' in shapedir:
                                                            i2 = i2-1
                                                            j2 = j2
                                                            if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                                #remove up from shapedir
                                                                shapedir.remove('up')
                                                            i2 = i2 + 1
                                                        if 'down' in shapedir:
                                                            i2 = i2+1
                                                            j2 = j2
                                                            if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                                #remove down from shapedir
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
                                        directions.remove('right')
                                    if outofrange == False and i+1 == i1 and j == j1 and change == True:
                                        directions.remove('down')
                                    if outofrange == False and i-1 == i1 and j == j1 and change == True:
                                        directions.remove('up')
                                    if outofrange == False and i == i1 and j-1 == j1 and change == True:
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
                                                    #remove left from shapedir
                                                    shapedir.remove('left')
                                                j2 = j2 + 1
                                            if 'right' in shapedir:
                                                i2 = i2
                                                j2 = j2+1
                                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                    #remove right from shapedir
                                                    shapedir.remove('right')
                                                j2 = j2 - 1
                                            if 'up' in shapedir:
                                                i2 = i2-1
                                                j2 = j2
                                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                    #remove up from shapedir
                                                    shapedir.remove('up')
                                                i2 = i2 + 1
                                            if 'down' in shapedir:
                                                i2 = i2+1
                                                j2 = j2
                                                if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                    #remove down from shapedir
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
                                                                #remove left from shapedir
                                                                shapedir.remove('left')
                                                            j2 = j2 + 1
                                                        if 'right' in shapedir:
                                                            i2 = i2
                                                            j2 = j2+1
                                                            if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                                #remove right from shapedir
                                                                shapedir.remove('right')
                                                            j2 = j2 - 1
                                                        if 'up' in shapedir:
                                                            i2 = i2-1
                                                            j2 = j2
                                                            if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                                #remove up from shapedir
                                                                shapedir.remove('up')
                                                            i2 = i2 + 1
                                                        if 'down' in shapedir:
                                                            i2 = i2+1
                                                            j2 = j2
                                                            if (i2 == prevsquare[0]) and (j2 == prevsquare[1]):
                                                                #remove down from shapedir
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
                                        directions.remove('right')
                                    if outofrange == False and i+1 == i1 and j == j1 and change == True:
                                        directions.remove('down')
                                    if outofrange == False and i-1 == i1 and j == j1 and change == True:
                                        directions.remove('up')
                                    if outofrange == False and i == i1 and j-1 == j1 and change == True:
                                        directions.remove('left')



                            if len(directions) == 2:
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
            
            ## CHECK IF ALL NODES ARE EITHER SHAPES OR Xs
            allnodes = True
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] == 'N' or board[i][j] == '.':
                        allnodes = False
            if allnodes == True:
                # if number of nodes which are shapes is equal to sum of every number in column_totals, then print("Solved correctly")
                # else print("Solved incorrectly")
                count = 0
                for i in range(len(board)):
                    for j in range(len(board)):
                        if board[i][j] in shapes.values():
                            count += 1
                total = 0
                for i in range(len(column_totals)):
                    total += column_totals[i]
                if count == total:
                    print("Solved correctly")
                else:
                    print("Solved incorrectly")
                break


            edgerulesneeded = False

            if any_changes == False:
                edgerulesneeded = True

            if edgerulesneeded == True:
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
                                        board[i][j] = "X"
                                        any_changes = True
                                    
                            if len(dots) == 1:
                                board[dots[0][0]][dots[0][1]] = "."
                                any_changes = True
                                for i in range(len(board)):
                                    if board[i][j] == "N":
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
                                        board[i][j] = "X"
                                        any_changes = True
                                    
                            if len(dots) == 1:
                                board[dots[0][0]][dots[0][1]] = "."
                                any_changes = True
                                for j in range(len(board)):
                                    if board[i][j] == "N":
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
                                        board[k][j] = "."
                                        k += 1
                                        counter += 1
                                    any_changes = True
                                if possiblementup == True:
                                    counter = 1
                                    k = place
                                    while counter < column_totals[j]:
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
                                        board[i][k] = "."
                                        k += 1
                                        counter += 1
                                    any_changes = True
                                if possiblementleft == True:
                                    counter = 1
                                    k = place
                                    while counter < row_totals[i]:
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
                                        board[k][j] = "."
                                        k += 1
                                        counter += 1
                                    any_changes = True
                                if possiblementup == True:
                                    counter = 1
                                    k = place
                                    while counter < column_totals[j]:
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
                                        board[i][k] = "."
                                        k += 1
                                        counter += 1
                                    any_changes = True
                                if possiblementleft == True:
                                    counter = 1
                                    k = place
                                    while counter < row_totals[i]:
                                        board[i][k] = "."
                                        k -= 1
                                        counter += 1
                                    any_changes = True
                
                
                print("Unique rule used")
                print()


board, start, end = Solver.generate_board()
Solver.Solve(board, start, end)
