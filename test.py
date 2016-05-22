from blocks import Block
from tetris import *

board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]]

# assert detect_collisions(board, None, [(1, 14), (2, 15), (1, 15), (2, 16)]) == True
# assert detect_collisions(board, None, [(1, 13), (2, 14), (1, 14), (2, 15)]) == True

# print(valid_placement_helper(board, Block("t", 0, 0, 0)))
# print(valid_placement_helper(board, Block("t", 1, 0, 0)))
# print(valid_placement_helper(board, Block("t", 2, 0, 0)))
# print(valid_placement_helper(board, Block("t", 3, 0, 0)))

for b in valid_placement(board, Block("t", 0, 0, 0), [0, 16]):
    print(b.get_coords())