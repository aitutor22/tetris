from blocks import Block
from tetris import *

board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]]

# assert detect_collisions(board, None, [(1, 14), (2, 15), (1, 15), (2, 16)]) == True
# assert detect_collisions(board, None, [(1, 13), (2, 14), (1, 14), (2, 15)]) == True

# print(valid_placement_helper(board, Block("t", 0, 0, 0)))
# print(valid_placement_helper(board, Block("t", 1, 0, 0)))
# print(valid_placement_helper(board, Block("t", 2, 0, 0)))
# print(valid_placement_helper(board, Block("t", 3, 0, 0)))

# for b in valid_placement(board, Block("t", 0, 0, 0), [0, 16]):
#     print(b.get_coords())

assert space_above_occupied(board, 2, 4) == False


# board = [[0, 0, 0, 0, 0, 1, 1, 0], [0, 0, 1, 1, 1, 1, 1, 0], [0, 1, 1, 0, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 0], [0, 1, 0, 1, 1, 1, 1, 0], [0, 1, 0, 1, 1, 1, 1, 1], [0, 1, 0, 1, 1, 1, 1, 1], [0, 1, 0, 0, 1, 1, 1, 1], [0, 1, 0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1, 1], [0, 1, 1, 0, 1, 1, 1, 1], [0, 1, 1, 0, 1, 0, 1, 1], [0, 1, 1, 0, 1, 1, 1, 1], [1, 1, 0, 1, 1, 0, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
# block = Block("o")

# print_matrix(board)
# for b, bl in potential_moves(board, block):
#     print(bl.x, bl.y)

# board = [[0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 0, 0], [0, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 1], [1, 0, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1]]
# # block = Block("o")

# # print_matrix(board)
# # for b, bl in potential_moves(board, block):
# #     print(bl.x, bl.y)


app = TetrisApp([-1.73952898, -1.35679522, -3.89298252, -1.2184164], True, board)
app.run()
print(app.score)


# board = [[0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 0, 0], [0, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 1], [1, 0, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1]]
# block = Block("l", 3, 6, 1)

# print(block.value)

# print_matrix(board)
# print("******")
# print(detect_collisions(board, block))
# temp_board = add_block_to_board(board, block)
# print_matrix(temp_board)
# print(potential_moves(board, block))
# print(valid_placement_helper(board, block))

# print(detect_collisions(board, Block("l", 3, 6, 0)))

# (6, 2)
# print(len(potential_moves(board, block)))
# for b, bl in potential_moves(board, block):
#     print(bl.x, bl.y)
