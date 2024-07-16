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
            board.append([0] * size)

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
        # First stage: change all 0s which connect to a start or end node to '.'
        # Print the board and solve first stage
        print("Initial board:")
        Solver.print_board(board)
        print("\nFirst stage:")

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] in Solver.characters.values():
                    if board[i][j] == Solver.RD:
                        if i + 1 < len(board):
                            board[i + 1][j] = '.'
                        if j + 1 < len(board):
                            board[i][j + 1] = '.'
                    elif board[i][j] == Solver.LD:
                        if i + 1 < len(board):
                            board[i + 1][j] = '.'
                        if j - 1 >= 0:
                            board[i][j - 1] = '.'
                    elif board[i][j] == Solver.RU:
                        if i - 1 >= 0:
                            board[i - 1][j] = '.'
                        if j + 1 < len(board):
                            board[i][j + 1] = '.'
                    elif board[i][j] == Solver.LU:
                        if i - 1 >= 0:
                            board[i - 1][j] = '.'
                        if j - 1 >= 0:
                            board[i][j - 1] = '.'
                    elif board[i][j] == Solver.H:
                        if j + 1 < len(board):
                            board[i][j + 1] = '.'
                        if j - 1 >= 0:
                            board[i][j - 1] = '.'
                    elif board[i][j] == Solver.V:
                        if i + 1 < len(board):
                            board[i + 1][j] = '.'
                        if i - 1 >= 0:
                            board[i - 1][j] = '.'

        Solver.print_board(board)

# Generate the board, print it, and solve the first stage
board, start, end = Solver.generate_board()
Solver.Solve(board, start, end)
