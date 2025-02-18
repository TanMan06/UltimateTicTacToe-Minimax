import sys
import numpy as np
import pygame

pygame.init()

# Colors
WHITE = (255,255,255)
GRAY = (180,180,180)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

# Sizes
B_WIDTH = 600
B_HEIGHT = 600
B_SQUARE_SIZE = B_WIDTH//3
B_CIRCLE_RADIUS = B_SQUARE_SIZE//3
B_CIRCLE_WIDTH = 45
B_CROSS_WIDTH = 75
B_LINE_WIDTH = 15



WIDTH = 200
HEIGHT = 200
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
BOARD_SIZE = 9
SQUARE_SIZE = WIDTH//BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE//3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25


# ROW = square//3
# COL = square %3

screen = pygame.display.set_mode((B_WIDTH, B_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe AI")
screen.fill(BLACK)
clock = pygame.time.Clock()
clock.tick(30) 

board = np.zeros((BOARD_SIZE, BOARD_SIZE))
B_board = np.zeros(BOARD_SIZE)
def draw_big_board(color = WHITE):
    for i in range (1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, B_SQUARE_SIZE*i), (B_WIDTH, B_SQUARE_SIZE * i), B_LINE_WIDTH)
        pygame.draw.line(screen, color, (B_SQUARE_SIZE*i, 0), (B_SQUARE_SIZE * i, B_HEIGHT), B_LINE_WIDTH)
    
def draw_lines(color = WHITE):
    for i in range(BOARD_SIZE):
        x_offset = B_SQUARE_SIZE * (i%3)
        y_offset = B_SQUARE_SIZE * (i//3)
        for j in range(1,BOARD_ROWS):
            pygame.draw.line(screen, color, (x_offset, y_offset + SQUARE_SIZE*j), (x_offset + WIDTH, y_offset + SQUARE_SIZE * j), LINE_WIDTH)
            pygame.draw.line(screen, color, (x_offset + SQUARE_SIZE*j, y_offset), (x_offset + SQUARE_SIZE * j, y_offset + HEIGHT), LINE_WIDTH)
        
def draw_figures(color = WHITE):
    for big_square in range(BOARD_SIZE):
        x_offset = B_SQUARE_SIZE * (big_square%3)
        y_offset = B_SQUARE_SIZE * (big_square//3)
        for small_square in range(BOARD_SIZE):
            row = small_square//3
            col = small_square%3
            if board[big_square][small_square] == 1:
                pygame.draw.circle(screen, color, ((int(col * SQUARE_SIZE + SQUARE_SIZE//2 + x_offset)), int(row * SQUARE_SIZE + SQUARE_SIZE//2 + y_offset)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[big_square][small_square] == 2:
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE//4 + x_offset, row * SQUARE_SIZE + SQUARE_SIZE//4 + y_offset), 
                                (col * SQUARE_SIZE + 3*SQUARE_SIZE//4 + x_offset, row * SQUARE_SIZE + 3*SQUARE_SIZE//4 + y_offset), CROSS_WIDTH)
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE//4 + x_offset, row * SQUARE_SIZE + 3 * SQUARE_SIZE//4 + y_offset), 
                                (col * SQUARE_SIZE + 3*SQUARE_SIZE//4 + x_offset, row * SQUARE_SIZE + SQUARE_SIZE//4 + y_offset), CROSS_WIDTH)

def b_draw_figures(color = WHITE):
    for B_square in range(BOARD_SIZE):
        row = B_square//3
        col = B_square%3
        if B_board[B_square] == 1:
            pygame.draw.circle(screen, color, ((int(B_square//3 * B_SQUARE_SIZE + B_SQUARE_SIZE//2)), int(B_square%3 * B_SQUARE_SIZE + B_SQUARE_SIZE//2)), B_CIRCLE_RADIUS, B_CIRCLE_WIDTH)
        elif B_board[B_square] == 2:
            pygame.draw.line(screen, color, (row * B_SQUARE_SIZE + B_SQUARE_SIZE//4, col * B_SQUARE_SIZE + B_SQUARE_SIZE//4), 
                                (row * B_SQUARE_SIZE + 3*B_SQUARE_SIZE//4, col * B_SQUARE_SIZE + 3*B_SQUARE_SIZE//4), B_CROSS_WIDTH)
            pygame.draw.line(screen, color, (row * B_SQUARE_SIZE + B_SQUARE_SIZE//4, col * B_SQUARE_SIZE + 3 * B_SQUARE_SIZE//4), 
                                (row * B_SQUARE_SIZE + 3*B_SQUARE_SIZE//4, col * B_SQUARE_SIZE + B_SQUARE_SIZE//4), B_CROSS_WIDTH)
                
                
                
                
def mark_square(B_square, s_square, player):
    board[B_square][s_square] = player
    
def mark_b_square(B_square, player):
    B_board[B_square] = player

def avaliable_square(B_sqaure, s_square):
    return board[B_sqaure][s_square] == 0

def B_avaliable_square(B_square):
    return B_board[B_square] == 0

def is_board_full(check_board = board):
    for square in range(9):
        if check_board[square] == 0:
            return False
    return True

def check_win(player, check_board = board):
    for col in range(BOARD_COLS):
        if check_board[col%3] == player and check_board[col%3+1] == player and check_board[col%3+2] == player:
            return True
    for row in range(BOARD_ROWS):
        if check_board[row*3] == player and check_board[row*3+1] == player and check_board[row*3+2] == player:
            return True
    if check_board[0] == player and check_board[4] == player and check_board[8] == player:
        return True
    if check_board[2] == player and check_board[4] == player and check_board[6] == player:
        return True
    return False

def minimax(minimax_board, B_square, depth, alpha, beta, isHuman):
    if check_win(2, B_board):
        return float('inf')
    if check_win(1, B_board):
        return float('-inf')
    if is_board_full(minimax_board[B_square]):
        return 0
    if depth == 0:
        return evaluation(minimax_board)
    
    best_score = float('inf') if isHuman else float('-inf')
    player = 1 if isHuman else 2
    update_func = min if isHuman else max
    for s_square in range(BOARD_SIZE):
        if minimax_board[B_square][s_square] == 0:
            minimax_board[B_square][s_square] = player
            score = minimax(minimax_board, s_square, depth - 1, alpha, beta, not isHuman)
            minimax_board[B_square][s_square] = 0
            best_score = update_func(score, best_score)
            if isHuman:
                beta = min(beta, best_score)
            else:
                alpha = max(alpha, best_score)
            if beta <= alpha:
                break
    return best_score

def evaluation(minimax_board):
    cnt = 0
    good_dict = []
    bad_dict = []
    for square in range(BOARD_SIZE):
        cnt += eval_board(minimax_board[square], False)
    cnt += 10 * eval_board(B_board, True)
    return cnt


def eval_board(check_board, is_big_board):
    cnt = 0
    if not is_big_board and check_win(2, check_board):
        cnt+=50
    if not is_big_board and check_win(1, check_board):
        cnt-=50
    if check_board[4] == 1:
        cnt-=5
    if check_board[4] == 2:
        cnt+=5
    if check_board[0] == 1:
        cnt -= 3
    if check_board[2] == 1:
        cnt -= 3
    if check_board[6] == 1:
        cnt -= 3
    if check_board[8] == 1:
        cnt -= 3
    if check_board[0] == 2:
        cnt += 3
    if check_board[2] == 2:
        cnt += 3
    if check_board[6] == 2:
        cnt += 3
    if check_board[8] == 2:
        cnt += 3
    if check_board[1] == 1:
        cnt -= 2
    if check_board[3] == 1:
        cnt -= 2
    if check_board[5] == 1:
        cnt -= 2
    if check_board[7] == 1:
        cnt -= 2
    if check_board[1] == 2:
        cnt += 2
    if check_board[3] == 2:
        cnt += 2
    if check_board[5] == 2:
        cnt += 2
    if check_board[7] == 2:
        cnt += 2
    return cnt
            
def best_move(B_square):
    move = -1
    if is_board_full(board[B_square]) or B_board[B_square] != 0:
        best_move_square_full()
    else: 
        best_score = float("-inf")
        for s_square in range(BOARD_SIZE):
            if board[B_square][s_square] == 0:
                board[B_square][s_square] = 2
                score = minimax(board, B_square, 4, float('-inf'), float('inf'), False)
                board[B_square][s_square] = 0
                if score > best_score:
                    best_score = score
                    move = s_square
        if move != -1:
            mark_square(B_square, move, 2)
    return B_square, move

def best_move_square_full():
    best_score = float('-inf')
    best_move = None
    best_B_square = -1
    for B_square in range(BOARD_SIZE):
        for s_square in range(BOARD_SIZE):
            if board[B_square][s_square] == 0 and not is_board_full(board[B_square]):
                board[B_square][s_square] = 2
                score = minimax(board, B_square, 3, float('-inf'), float('inf'), False)
                board[B_square][s_square] = 0
                if score > best_score:
                    best_score = score
                    best_move = s_square
                    best_B_square = B_square
    if best_move:
        s_square = best_move
        mark_square(best_B_square, s_square, 2)
        return best_B_square, s_square
    return None
    

def restart_game():
    screen.fill(BLACK)
    draw_big_board()
    draw_lines()
    for square in range(BOARD_SIZE):
        board[square] = 0

def update_display():
    if not game_over:
        draw_figures()
        b_draw_figures()
    else:
        color = GREEN if check_win(1) else RED if check_win(2) else GRAY
        draw_figures(color)
        draw_lines(color)
    pygame.display.update()


draw_big_board()    
draw_lines()
player = 1
game_over = False
cur_square = 4
update_display()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            B_square = (event.pos[1] // B_SQUARE_SIZE) * 3 + (event.pos[0] // B_SQUARE_SIZE)
            s_square = (event.pos[1]%B_SQUARE_SIZE // SQUARE_SIZE) *3 + (event.pos[0]%B_SQUARE_SIZE // SQUARE_SIZE)
            
            valid_big_square = B_avaliable_square(B_square)
            valid_small_square = avaliable_square(B_square, s_square)
            following_rules = (cur_square == B_square) or B_board[cur_square] != 0

            if valid_big_square and valid_small_square and following_rules:

                mark_square(B_square, s_square, player)
                if check_win(player, board[B_square]):
                    B_board[B_square] = player
                if check_win(player, B_board) or check_win(player, B_board) or is_board_full(B_board):
                    game_over = True
                    
                player = player % 2 + 1
                
                if not game_over:
                    B_square, cur_square = best_move(s_square)
                    if cur_square != -1 and not is_board_full(B_board):
                        if check_win(player, board[B_square]):
                            B_board[B_square] = player
                        if check_win(player, B_board):
                            game_over = True
                        else:
                            player = player % 2 + 1
                    if is_board_full(B_board):
                        game_over = True  
                update_display()
            else:
                continue

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1
    