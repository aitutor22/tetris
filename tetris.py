from __future__ import division
import pygame, sys, copy, time, random, itertools
from blocks import Block
import classifier

#inspired by 2010 "Kevin Chabowski"<kevin@kch42.de>'s implementation of Tetris
#rules taken from http://tetris.wikia.com/wiki/Tetris_Guideline
cols = 8
rows = 16
cell_size = 36
base_score = [0, 40, 100, 300, 1200]
num_lines_to_advance = 6
colors = [(0, 0, 0), (255, 85, 85), (35, 35, 35), (155, 200, 70)]
pause_before_closing = 0
interval_between_drop = 0.01
fast_mode = True

turn_in_milliseconds = 1

#event to tell pygame to move current block down by 1
DROP_EVENT = pygame.USEREVENT + 1
AI_MOVE_EVENT = pygame.USEREVENT + 2

#converts board to a dictionary using tuple as key
def convert_board_to_dict(board):
    d = {}

    for cy, row in enumerate(board):
        for cx, val in enumerate(row):
            d[(cx, cy)] = val

    return d

#returns True is there is a collision
def detect_collisions(board, block, coords=None):
    if coords == None:
        coords = block.get_coords()

    try:
        for x, y in coords:
            #check if there is a collision or if block goes off screen
            if x < 0 or x >= cols or board[y][x]:
                return True
    except IndexError:
        return True

    return False

def potential_moves(board, block):
    moves_dict = {}     
    filled_surfaced = get_filled_surface(board)
    potential_boards = []

    flattened_potential_boards = []

    for fs in filled_surfaced:
        for b in valid_placement(board, block, fs):

            temp_board = add_block_to_board(board, b)

            #we use the flattened temp board (1D list) to test if the board is already stored
            flattened_temp_board = list(itertools.chain(*temp_board))
        
            if flattened_temp_board not in flattened_potential_boards:
                potential_boards.append((temp_board, b))
                flattened_potential_boards.append(flattened_temp_board)

    # print_boards([b for b, _ in potential_boards])
    return potential_boards

def print_boards(boards):
    print("Total number of boards: {}".format(len(boards)))
    for b in boards:
        print_matrix(b, True)


def valid_placement(board, block, surface_coords):
    width, height = len(block.value[0]), len(block.value)
    results = []

    #need to consider multiple positions to left
    for rotation_index in range(4):
        for offset_x in range(width)[::-1]:
            test_block = Block.copy_block(block)
            test_block.rotate_to(rotation_index)            
            test_block.x = surface_coords[0] - offset_x
            test_block.y = surface_coords[1] - height

            coords = valid_placement_helper(board, test_block)

            if coords:
                results.append(test_block)

    return results

#returns True if any space above it is occupied
def space_above_occupied(board, x, y):
    for row in range(y):
        if board[row][x]:
            return True

    return False

#modifies block in place
#returns coords of final position
def valid_placement_helper(board, block):

    #if there is an initial collision before we start dropping, means invalid 
    if detect_collisions(board, block):
        return None

    #invalid if any space above it is blocked
    #while this is a valid case, ignore it to make algorithm easier
    coords = block.get_coords()
    if any([space_above_occupied(board, x, y) for x, y in coords]):
        return None

    #meant to consider blocks that have empty parts
    while drop_helper(board, block):
        block.y += 1

    return block.get_coords()    

#returns True if a block can be dropped
#does not affect the block
def drop_helper(board, block):
    if block == None:
        return False
    #we first test to see if there will be a collision if block moves down
    test_block = Block.copy_block(block)
    test_block.y += 1

    return not detect_collisions(board, test_block)

#returns a new board with block added
#returns None if there is an overlap
def add_block_to_board(board, block):
    board = copy.deepcopy(board)

    coords = block.get_coords()    
    for x, y in coords:
        board[y][x] += 1
        if board[y][x] > 1:
            return None

    return board

#helper function for debugging
def print_matrix(matrix, exclude_bottom=False):
    if exclude_bottom:
        matrix = matrix[:-1]
    for row in matrix:
        print(row)  

    print("\n")

#returns list of coords with outermost filled blocks
def get_filled_surface(board):
    filled_surfaced = []
    board_dict = convert_board_to_dict(board)

    for cx in range(cols):
        for cy in range(len(board) - 1):
            if not board_dict[(cx, cy)] and board_dict[(cx, cy + 1)]:
                filled_surfaced.append((cx, cy + 1))
                break

    return filled_surfaced   

class TetrisApp(object):
    def __init__(self, weights):
        pygame.init()
        pygame.key.set_repeat(250, 10)

        self.weights = weights
        self.width = cell_size * cols
        self.height = cell_size * rows

        self.bground_grid = [[2 if x % 2 == y % 2 else 0 for x in xrange(cols)] for y in xrange(rows)]
        self.board = None
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        # initialize font
        self.font = pygame.font.SysFont("comicsansms", 24)

    def run(self):   
        self.game_running = False
        self.start_game()
        pygame.time.set_timer(AI_MOVE_EVENT, 50)   

        while True and not self.paused:
            for event in pygame.event.get():
                self.event_helper(event)

    def event_helper(self, event):
        if event.type == pygame.QUIT:
            self.quit()
        elif event.type == DROP_EVENT:
            self.drop()

        #for AI 
        elif event.type == AI_MOVE_EVENT:
            try:
                self.get_best_move()
            except:
                pass

        elif event.type == pygame.KEYDOWN:
            #escape key
            if event.key == 27:
                self.quit()    
            
            #up key
            elif event.key == 273:
                self.rotate() 
            
            #down key
            elif event.key == 274:
                self.drop()
                self.update_screen()

            #left key
            elif event.key == 276:
                self.move(-1)  
            
            #right key
            elif event.key == 275:
                self.move(1)    

            #a key trigger ai movement
            elif event.key == 97:
                self.get_best_move()
                # pygame.time.set_timer(AI_MOVE_EVENT, turn_in_milliseconds)

            #b key 
            elif event.key == 98:
                # self.generate_new_block()
                # self.update_screen()
                # print(self.board)
                potential_moves(self.board, self.block)
                pass
                # potential_moves(self.board, self.block)


    def update_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_matrix(self.bground_grid, (0,0))

        if self.block:
            self.draw_matrix(self.block.value, (self.block.x, self.block.y))

        self.draw_matrix(self.board, (0, 0), True)

        #render score and level
        score = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score, (self.width - score.get_width() - 20, score.get_height()))
        level = self.font.render("Level: " + str(self.level), True, (255, 255, 255))
        #allign with score
        self.screen.blit(level, (self.width - score.get_width() - 20, score.get_height() + 40))

        pygame.display.update()


    def drop(self):
        if self.game_running:
            if drop_helper(self.board, self.block):
                self.block.y += 1
                return True

            #if collide, then add block to board and check if game over
            else:
                test_board = add_block_to_board(self.board, self.block)
                # print_matrix(test_board)

                #test_board will be None if there is an overlap (aka game over)
                if test_board == None:
                    self.game_over()

                else:
                    self.board = test_board
                    #if not game over, then create new block

                    self.clear_rows()
                    self.check_level()

                    self.generate_new_block()

                return False

    def generate_new_block(self, x=0, y=0):
        #first test if a new block is valid
        test_block = Block.new_block(x, y, False)
        if detect_collisions(self.board, test_block):
            self.game_over()

        else:
            self.last_block = self.block
            self.block = Block.new_block(x, y)        

    def clear_rows(self):
        #get a list of rows that we want to remove
        to_remove = []
        #exclude the last row which is supposed to be hidden
        for cy, row in enumerate(self.board[:-1]):
            #assumption that values in board are binary
            #thus a row is full if its sum is equals to number of columns
            if sum(row) == cols:
                to_remove.append(cy)

        #since we are deleting, delete from the end to prevent bugs
        to_remove.reverse()
        for cy in to_remove:
            del self.board[cy]

        #after we finish deleting, add new blank rows at the top
        for cy in to_remove:
            self.board.insert(0, [0] * cols)

        self.score += self.calculate_score(len(to_remove))
        self.lines_cleared += len(to_remove)

    def calculate_score(self, num_lines):
        return base_score[num_lines] * self.level

    #check to see if we should increment level
    def check_level(self):
        if self.lines_cleared >= self.level * num_lines_to_advance:
            self.level += 1
            #increase speed as we increase level
            delay = max(1000 - 50 * (self.level - 1), 100)
            pygame.time.set_timer(DROP_EVENT, delay)        

    def move(self, amt):
        if self.game_running:
            #we first test to see if there will be a collision if block moves down
            #by using a test_block
            test_block = Block.copy_block(self.block)
            test_block.x += amt

            #checks that ensure block does not go out of screen
            if test_block.x < test_block.buffer[0]:
                self.block.x = self.block.buffer[0]

            elif test_block.x > cols - test_block.length + test_block.buffer[1]:
                self.block.x = cols - self.block.length + self.block.buffer[1]

            #if there is a collision, then apply the movement to actual block
            if not detect_collisions(self.board, test_block):
                self.block.x += amt

            self.update_screen()

    def rotate(self):
        if self.game_running:

            test_block = Block.copy_block(self.block)

            #try to rotate right
            test_block.rotate_right()

            #if there is no collision detected, rotate actual block
            if not detect_collisions(self.board, test_block):
                self.block.rotate_right()
                self.update_screen()

    def start_game(self):
        if not self.game_running:
            self.game_running = True
            self.paused = False
            self.init_game()

    def init_game(self):
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.board = self.new_board()
        self.block = None
        self.last_block = None
        self.update_screen()


        #remove for AI
        self.block = Block.new_block(0, 0)

        #tells system to fire off a drop event once every 1000ms
        # pygame.time.set_timer(DROP_EVENT, 1000)

    #creates and returns a bit matrix that represents gameboard
    #1 represents a filled block while 0 represents an empty block
    def new_board(self):
        #empty block
        board = [[0 for x in xrange(cols)]
                for y in xrange(rows) ]

        #bottom-most layer is filled
        board += [[1 for x in xrange(cols)]]
        return board

    def draw_matrix(self, matrix, offset, special_color=False):
        off_x, off_y  = offset

        if special_color and self.last_block:
            coords = self.last_block.get_coords()

        for cy, row in enumerate(matrix):
            for cx, val in enumerate(row):
                #ensures that only valid blocks are drawn
                if val:
                    color_index = val

                    if special_color and self.last_block and (off_x + cx, off_y + cy) in coords:
                        color_index = 3

                    # pygame.draw.rect(self.screen, colors[val],
                    pygame.draw.rect(self.screen, colors[color_index],
                        pygame.Rect(
                            (off_x + cx) * cell_size,
                            (off_y + cy) * cell_size, 
                            cell_size - 1, cell_size - 1), 0)

    def quit(self):
        print("quitting")
        sys.exit()        

    def game_over(self):
        self.last_block = self.block
        self.block = None
        self.update_screen()
        self.game_running = False
        print("Game Over")

        #2 sec pause before closing
        time.sleep(pause_before_closing)
        # print("redrawing")
        # self.update_screen()
        self.paused = True
        return self.score


    def get_best_move(self):
        if self.game_running:

            #we test if this block is valid before using it
            test_block = Block.new_block(0, 0, False)
            moves = potential_moves(self.board, test_block)

            potential_boards = [potential_board for potential_board, _ in moves]
            potential_blocks = [potential_block for _, potential_block in moves]

            # print(potential_boards)
            index = classifier.return_best_board(potential_boards, self.weights, rows + 1, cols)
            best_block = potential_blocks[index]

            best_block.y = 0
            self.block = best_block
            self.update_screen()

            if not fast_mode:
                while True:
                    if self.drop():
                        time.sleep(interval_between_drop)
                        self.update_screen()

                    else:
                        break
            else:
                while True:
                    if not self.drop():
                        self.update_screen()
                        break

if __name__ == "__main__":
    #clear, height, hole, blockage
    app = TetrisApp([-3.11447111, -4.39566282, -4.47513427, 1.30973485])
    app.run()


