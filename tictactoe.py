import sys
import pygame
import random
import copy
import numpy as np

from constants import *
 
# player 1 human 
# player 2 engine

# PYGAME SETUP

pygame.init() # initalize pygame module

screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE ENGINE')
screen.fill(BG_COLOR)

class AI:

    def __init__(self, level=0, player=2):  # default level=0, player=2
        # level 0 is random move level 1 is AI move
        self.level = level
        self.player = player

    def rnd(self, board): # random move genrator
        empty_sqrs = board.get_empty_squares() # store list of epmty squares
        idx = random.randrange(0, len(empty_sqrs))  # get a random empty square position

        return empty_sqrs[idx]  # return the position

    def minimax(self, board, maximizing):
        # terminal case
        case = board.final_state()

        # player 1 ie: human wins
        if case == 1:
            return 1, None
        
        # player 2 ie: engine wins
        elif case == 2:
            return -1, None
        
        # if draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)    # human player
                eval = self.minimax(temp_board, False)[0]
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        else:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move


    def eval(self, main_board):
        if self.level == 0:    # random move generator
            move = self.rnd(main_board)
            return move
            
        else:    # engine move generator
            eval, move = self.minimax(main_board, False)

        print(f'Engine has chosen to mark {move} with an eval of: {eval}')
        return (move[0], move[1])

class Board(): 

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs_list = []  # list for empty sqrs
        self.marked_sqrs_count = 0  # count of marked sqrs
        print(self.squares)

    def mark_square(self, row, col, player):    
        self.squares[row][col] = player
        self.marked_sqrs_count += 1     # incerement num of marked squares

    def empty_square(self, row, col):   # checks if empty square
        return self.squares[row][col] == 0

    def get_empty_squares(self):# check if board full
        self.empty_sqrs_list = np.argwhere(self.squares == 0)  # this function returns the indices of squares which = 0
        return self.empty_sqrs_list
    
    def isfull(self):# check if board full
        return self.marked_sqrs_count == 9
    
    def isempty(self):# check if board empty
        return self.marked_sqrs_count == 0

    def final_state(self):
        '''
            returns 0 if no win yet
            returns 1 if player 1 wins
            returns 2 if player 2 wins
        '''

        # vertical wins
        for col in range(COLS):
                if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                    return self.squares[0][col]

        # howrizontal wins
        for row in range(ROWS):
                if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                    return self.squares[row][0]
        
        # primary diagonal win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[0][0]
        
        # secondary diagonal win
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            return self.squares[2][0]

        # no winner yet    
        return 0
    



class Game():

    def __init__(self):
        self.board = Board()    # create a Board object
        self.ai = AI(1, 2)          # create an AI object with default constructor
        self.player = 1         # 1-cross 2-circle; player 1 starts game always
        self.game_mode = 'ai'  # PVP or AI modes
        self.running = True     # checks if board full or player wins and game over
        self.show_lines()       # draw the lines on board
        

    def show_lines(self):
        # vertical lines
        pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (2*CELL_SIZE, 0), (2*CELL_SIZE, HEIGHT), LINE_WIDTH)
       
        # horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, 2*CELL_SIZE), (WIDTH, 2*CELL_SIZE), LINE_WIDTH)

    def change_turn(self):
        self.player = 2 if self.player == 1 else 1

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            x = int(col*CELL_SIZE + CELL_SIZE/4)
            x_= int((col+1)*CELL_SIZE - CELL_SIZE/4)

            y = int(row*CELL_SIZE + CELL_SIZE/4)
            y_= int((row+1)*CELL_SIZE - CELL_SIZE/4)

            pygame.draw.line(screen, CROSS_COLOR, (x,y), (x_,y_), CROSS_WIDTH)
            pygame.draw.line(screen, CROSS_COLOR, (x_,y), (x,y_), CROSS_WIDTH)
        
        elif self.player == 2:
            # draw cicrle
            center = (col * CELL_SIZE + CELL_SIZE//2, row * CELL_SIZE + CELL_SIZE//2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)  # STORE IN CONCSTANT




# main function
def main():
    
    # create game object
    game = Game()
    ai = game.ai
    board = game.board  # to allow easy access instead of writing game.board everytime

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:                
                mouse_x = event.pos[0]  # get pointer position x
                mouse_y = event.pos[1] # get pointer position x
                
                row = int(mouse_y // CELL_SIZE)  # get the row
                col = int(mouse_x // CELL_SIZE)  # get the col
                 
                if board.empty_square(row, col):
                    board.mark_square(row, col, game.player)    # mark the position in array 
                    game.draw_fig(row, col)     # draw the fig on board gui         
                    game.change_turn()


        if game.game_mode == 'ai' and game.player == ai.player:
            # update screen
            pygame.display.update()

            row, col = ai.eval(board) # return random position
            board.mark_square(row, col, 2)   # computer fills the position with 2 in array
            game.draw_fig(row,col)         # draw on the screen
            game.change_turn()


        pygame.display.update()

            



# call main function
main()
