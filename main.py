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

        return board, start, end


    def print_board(board):
        for row in board:
            print(' '.join(map(str, row)))


    def Solve(board, start, end):
        any_changes = True
        while any_changes:
            any_changes = False
            RD = "┌"
            LD = "┐"
            RU = "└"
            LU = "┘"
            H = "─"
            V = "│"
            DOT = "."
            NULL = "N"
            
            definites = {
                'RD': RD,
                'LD': LD,
                'RU': RU,
                'LU': LU,
                'H': H,
                'V': V,
                '.': DOT
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
            column_totals = [3,5,5,2,3,2]
            row_totals = [2,2,3,6,6,1]

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
                        elif count == 3:
                            if 'left' in directions and 'down' in directions and 'up' in directions:
                                if i - 1 >= 0 and j-1 >= 0 and board[i-1][j-1] == RD:
                                    directions.remove('left')
                            if 'right' in directions and 'down' in directions and 'up' in directions:
                                if i - 1 >= 0 and j+1 < len(board) and board[i-1][j+1] == LD:
                                    directions.remove('right')
                            if 'up' in directions and 'left' in directions and 'right' in directions:
                                if i - 1 >= 0 and j-1 >= 0 and board[i-1][j-1] == RD:
                                    if board[i-1][j] == LD:
                                        directions.remove('left')
                                    if board[i][j-1] == RU:
                                        directions.remove('up')
                                if i - 1 >= 0 and j+1 < len(board) and board[i-1][j+1] == LD:
                                    if board[i-1][j] == RD:
                                        directions.remove('right')
                                    if board[i][j+1] == LU:
                                        directions.remove('up')
                            if 'down' in directions and 'left' in directions and 'right' in directions:
                                if i + 1 < len(board) and j-1 >= 0 and board[i+1][j-1] == RU:
                                    if board[i+1][j] == LU:
                                        directions.remove('left')
                                    if board[i][j-1] == RD:
                                        directions.remove('down')
                                if i + 1 < len(board) and j+1 < len(board) and board[i+1][j+1] == LU:
                                    if board[i+1][j] == RU:
                                        directions.remove('right')
                                    if board[i][j+1] == LD:
                                        directions.remove('down')
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







board, start, end = Solver.generate_board()
Solver.Solve(board, start, end)
