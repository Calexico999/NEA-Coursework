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


class Generate_Random_Path:

    def is_edge(node, size):
        x, y = node
        return x == 0 or x == size - 1 or y == 0 or y == size - 1

    def accept_board(board):
        size = len(board)
        for i in range(size):
            if all(cell == 0 for cell in board[i]):
                return False
            if all(board[j][i] == 0 for j in range(size)):
                return False
        return True

    def generate_path(board, start):
        size = len(board)
        max_length = random.randint(30, 40)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while True:
            virtual_board = [row[:] for row in board]
            stack = [start]
            path_length = 0
            last_node = start
            bignums = 0
            
            while stack and path_length < max_length: #bignums
                current = stack.pop()
                x, y = current
                if virtual_board[x][y] == 0 or (x, y) == start:
                    if (x, y) != start:
                        virtual_board[x][y] = 1
                    path_length += 1
                    last_node = (x, y)
                    random.shuffle(directions)

                    for direction in directions:
                        new_x, new_y = x + direction[0], y + direction[1]
                        if 0 <= new_x < size and 0 <= new_y < size and virtual_board[new_x][new_y] == 0:
                            stack.append((new_x, new_y))

            if Generate_Random_Path.is_edge(last_node, size) and Generate_Random_Path.accept_board(virtual_board):
                virtual_board[last_node[0]][last_node[1]] = 'E'
                # Ensure the start node remains 'S'
                virtual_board[start[0]][start[1]] = 'S'
                Generate_Board.print_board(virtual_board)
                return virtual_board


board, start = Generate_Board.generate_board()
path_board = Generate_Random_Path.generate_path(board, start)