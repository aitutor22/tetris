import random
from collections import OrderedDict

class Block(object):
    shapes_length = {
        "i": [4, 1],
        "o": [2, 2],
        "t": [3, 2],
        "s": [3, 2],
        "z": [3, 2],
        "j": [3, 2],
        "l": [3, 2],
    }

    shapes_buffer = {
        "i": [(0, 0), (-2, 1), (0, 0), (-1, 2)],
        "o": [(0, 0), (0, 0), (0, 0), (0, 0)],
        "t": [(0, 0), (-1, 0), (0, 0), (0, 1)],
        "s": [(0, 0), (-1, 0), (0, 0), (0, 1)],
        "z": [(0, 0), (-1, 0), (0, 0), (0, 1)],
        "j": [(0, 0), (-1, 0), (0, 0), (0, 1)],
        "l": [(0, 0), (-1, 0), (0, 0), (0, 1)],
    }

    shapes = OrderedDict()
    shapes["i"] = [[
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [1, 1, 1, 1],          
                [0, 0, 0, 0]
            ],
            [
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]
            ]]

    shapes["o"] = [[
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1],
                [1, 1]
            ]]

    shapes["t"] = [[
                [0, 1, 0],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 1, 0],
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 1, 0],          
            ],
            [
                [0, 1, 0],
                [1, 1, 0],
                [0, 1, 0],
            ]]

    shapes["s"] = [[
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 0, 1]
            ],
            [
                [0, 0, 0],
                [0, 1, 1],
                [1, 1, 0]         
            ],
            [
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]]

    shapes["z"] = [[
                [1, 1, 0],
                [0, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 0, 1],
                [0, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 0],
                [0, 1, 1]      
            ],
            [
                [0, 1, 0],
                [1, 1, 0],
                [1, 0, 0]
            ]]

    shapes["j"] = [[
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 1],
                [0, 1, 0],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 0, 1]
            ],
            [
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 0]
            ]]

    shapes["l"] = [[
                [0, 0, 1],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 1]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [1, 0, 0]
            ],
            [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 0]
            ]]

    #queue to determine what shapes to get
    shapes_queue = shapes.keys()
    random.shuffle(shapes_queue)


    def __init__(self, block_type, index=0, start_x=0, start_y=0):
        self.block_type = block_type
        self.index = index

        self.x = start_x
        self.y = start_y

        #buffer is used to check
        self.buffer = Block.shapes_buffer[self.block_type][self.index]
        #index 0 and 2 have the same length, while 1 and 3 have the same length
        self.length = Block.shapes_length[self.block_type][self.index % 2]        

        self.value = self.get_value()

    @classmethod
    def copy_block(cls, block):
        return cls(block.block_type, block.index, block.x, block.y)

    @classmethod
    def new_block(cls, start_x=0, start_y=0):

        #obtains block type from a random queue
        #this is to ensure a more even distribution of blocks
        try:
            block_type = cls.shapes_queue.pop()
        except IndexError:
            cls.shapes_queue = cls.shapes.keys()
            random.shuffle(cls.shapes_queue)
            block_type = cls.shapes_queue.pop()

        return cls(block_type, 0, start_x, start_y)

    def get_value(self):
        return Block.shapes[self.block_type][self.index]

    #returns list of coordinates for block
    def get_coords(self):
        return [(cx + self.x, cy + self.y) for cy, row in enumerate(self.value)
            for cx, val in enumerate(row) if val]

    def rotate(self, amt):
        self.index = (self.index + amt) % 4

        #buffer is used to check     
        self.buffer = Block.shapes_buffer[self.block_type][self.index]
        #index 0 and 2 have the same length, while 1 and 3 have the same length
        self.length = Block.shapes_length[self.block_type][self.index % 2]        
        self.value = self.get_value()

    def rotate_left(self):
        self.rotate(-1)

    def rotate_right(self):
        self.rotate(1)
