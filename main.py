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

    def dfs(start, board_size, min_length=30):
        visited = set()
        stack = [(start, [start])]

        while stack:
            v, path = stack.pop()

            if len(path) >= min_length:
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

if __name__ == "__main__":
    board_size = int(input("Enter the size of the board: "))
    path = None
    while path is None:
        start = GenerateRandomPath.start_node(board_size)
        path = GenerateRandomPath.dfs(start, board_size)
    print(path)
