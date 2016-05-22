from __future__ import division
import pygame, sys, copy, time
from blocks import Block

#inspired by 2010 "Kevin Chabowski"<kevin@kch42.de>'s implementation of Tetris
#rules taken from http://tetris.wikia.com/wiki/Tetris_Guideline
cols = 10
rows = 22
cell_size = 36
base_score = [0, 40, 100, 300, 1200]
num_lines_to_advance = 6
colors = [(0, 0, 0), (255, 85, 85), (35, 35, 35)]

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
def detect_collisions(board, block):
    coords = block.get_coords()
    try:
        for x, y in coords:
            #check if there is a collision or if block goes off screen
            if x < 0 or x >= cols or board[y][x]:
                return True
    except IndexError:
        return True

    return False

#modifies board inplace
def add_block_to_board(board, block):
    coords = block.get_coords()    
    for x, y in coords:
        board[y][x] += 1    

#helper function for debugging
def print_matrix(matrix):
    for row in matrix:
        print(row)    

class TetrisApp(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250, 10)
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

        while True:
            #resets the screen every tick
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                self.event_helper(event) 

    def update_screen(self):
        self.draw_matrix(self.bground_grid, (0,0))
        self.draw_matrix(self.board, (0, 0))
        self.draw_matrix(self.block.value, (self.block.x, self.block.y))

        #render score and level
        score = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score, (self.width - score.get_width() - 20, score.get_height()))

        level = self.font.render("Level: " + str(self.level), True, (255, 255, 255))
        #allign with score
        self.screen.blit(level, (self.width - score.get_width() - 20, score.get_height() + 40))

        pygame.display.update()

    def event_helper(self, event):
        if self.board:
            self.update_screen()

        if event.type == pygame.QUIT:
            self.quit()
        elif event.type == DROP_EVENT:
            self.drop()

        #for AI 
        elif event.type == AI_MOVE_EVENT:
            self.ai_move([(8, 20), (9, 20), (8, 21), (9, 21)])   

        elif event.type == pygame.KEYDOWN:

            # print(event)
            #escape key
            if event.key == 27:
                self.quit()
            
            #space key
            elif event.key == 32:
                self.start_game()      
            
            #up key
            elif event.key == 273:
                self.rotate() 
            
            #down key
            elif event.key == 274:
                self.drop() 

            #left key
            elif event.key == 276:
                self.move(-1)  
            
            #right key
            elif event.key == 275:
                self.move(1)    

            #a key trigger ai movement
            elif event.key == 97:
                pygame.time.set_timer(AI_MOVE_EVENT, 50)

            elif event.key == 98:
                self.potential_moves()

            #z key trigger instant drop
            elif event.key == 122:
                while True:
                    if not self.drop():
                        break

    def drop(self):
        #we create a test block to check if there is a collision before manipulating the 
        #actual block (that is shown on screen)
        if self.game_running:

            #we first test to see if there will be a collision if block moves down
            test_block = Block.copy_block(self.block)
            test_block.y += 1

            #if there is a collision for the test_block, we do not modify
            #the position of the actual block and just add it to board
            if detect_collisions(self.board, test_block):

                add_block_to_board(self.board, self.block)

                #game over
                test_block.y -= 1
                if test_block.y == 0:
                    self.game_running = False
                    print("Game Over")

                #if not game over, then create new block
                self.clear_rows()
                self.check_level()

                target_coords = self.generate_best_move()
                print(target_coords[0][0])
                self.block = Block.new_block(target_coords[0][0], 0)

                return False
            
            #if there is no collision (i.e. valid move), then update actual block
            else:
                self.block.y += 1

            return True
                

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

    def rotate(self):
        if self.game_running:

            test_block = Block.copy_block(self.block)

            #try to rotate right
            test_block.rotate_right()

            #if there is no collision detected, rotate actual block
            if not detect_collisions(self.board, test_block):
                self.block.rotate_right()

    def start_game(self):
        if not self.game_running:
            self.init_game()
            self.game_running = True

    def init_game(self):
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.board = self.new_board()
        self.block = Block.new_block()

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

    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for cy, row in enumerate(matrix):
            for cx, val in enumerate(row):
                #ensures that only valid blocks are drawn
                if val:
                    pygame.draw.rect(self.screen, colors[val],
                        pygame.Rect(
                            (off_x + cx) * cell_size,
                            (off_y + cy) * cell_size, 
                            cell_size - 1, cell_size - 1), 0)



    def ai_move(self, target_coords):
        coords = self.block.get_coords()
        if coords[0][0] < target_coords[0][0]: 
            self.move(1)

        if coords[0][0] > target_coords[0][0]: 
            self.move(-1)

        elif coords[0][1] < target_coords[0][1]:
            self.drop()





    def potential_moves(self):
        # moves = []
        
        filled_surfaced = self.get_filled_surface()
        print(filled_surfaced)




    #returns list of coords with outermost filled blocks
    def get_filled_surface(self):
        filled_surfaced = []
        board_dict = convert_board_to_dict(self.board)
        for cx in range(cols):
            for cy in range(len(self.board) - 1):
                if not board_dict[(cx, cy)] and board_dict[(cx, cy + 1)]:
                    filled_surfaced.append((cx, cy + 1))
                    break

        return filled_surfaced        






        # print_matrix(self.board)
        # print(self.block.value)
        # for cy, row in enumerate(self.board):
        #     for cx, val in enumerate(row):
        #         if val == 1 and self.board[row - 1][cx]
        #         moves.append((cx, cy))


    def generate_best_move(self):
        return [(8, 20), (9, 20), (8, 21), (9, 21)]



    def quit(self):
        print("quitting")
        sys.exit()        

if __name__ == "__main__":
    app = TetrisApp()
    app.run()