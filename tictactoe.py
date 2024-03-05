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
        # fill bg_color
        screen.fill(BG_COLOR)

        # vertical lines
        pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (2*CELL_SIZE, 0), (2*CELL_SIZE, HEIGHT), LINE_WIDTH)
       
        # horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, 2*CELL_SIZE), (WIDTH, 2*CELL_SIZE), LINE_WIDTH)

    def change_turn(self):
        self.player = 2 if self.player == 1 else 1

    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)    # mark the position in array using board object
        self.draw_fig(row, col)     # draw the fig on board gui         
        self.change_turn()

    def change_game_mode(self):
        self.game_mode = 'ai' if self.game_mode == 'pvp' else 'pvp'


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

    def reset(self):
        self.__init__() #just call initialiser function to reset all values
        

    def game_over(self):
        return self.board.final_state() != 0 or self.board.isfull()     # if either 1 or 2 has won or board is full game over

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
                 
                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)

                    if game.game_over():
                        game.running = False
            
            if event.type == pygame.KEYDOWN:
                # g key changes game mode
                if event.key == pygame.K_g:
                    game.change_game_mode()
                
                # 0 key changes to random move mode
                if event.key == pygame.K_0:
                    game.ai.level = 0
                
                # 1 key changes to engine move mode
                if event.key == pygame.K_1:
                    game.ai.level = 1

                # r key resets game
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board



        if game.game_mode == 'ai' and game.player == ai.player and game.running:
            # update screen
            pygame.display.update()

            row, col = ai.eval(board) # return random position
            game.make_move(row, col)
            
            if game.game_over():
                game.running = False

        pygame.display.update()

            



# call main function
main()
