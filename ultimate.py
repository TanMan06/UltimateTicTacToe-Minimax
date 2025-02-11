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
SQUARE_SIZE = WIDTH//BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE//3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25


screen = pygame.display.set_mode((B_WIDTH, B_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe AI")
screen.fill(BLACK)

board = np.zeros((9, BOARD_ROWS, BOARD_COLS))
B_board = np.zeros((BOARD_ROWS, BOARD_COLS))

def draw_big_board(color = WHITE):
    for i in range (1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, B_SQUARE_SIZE*i), (B_WIDTH, B_SQUARE_SIZE * i), B_LINE_WIDTH)
        pygame.draw.line(screen, color, (B_SQUARE_SIZE*i, 0), (B_SQUARE_SIZE * i, B_HEIGHT), B_LINE_WIDTH)
    
def draw_lines(color = WHITE):
    for i in range(9):
        x_offset = B_SQUARE_SIZE * (i%3)
        y_offset = B_SQUARE_SIZE * (i//3)
        for j in range(1,BOARD_ROWS):
            pygame.draw.line(screen, color, (x_offset, y_offset + SQUARE_SIZE*j), (x_offset + WIDTH, y_offset + SQUARE_SIZE * j), LINE_WIDTH)
            pygame.draw.line(screen, color, (x_offset + SQUARE_SIZE*j, y_offset), (x_offset + SQUARE_SIZE * j, y_offset + HEIGHT), LINE_WIDTH)
        
def draw_figures(color = WHITE):
    for i in range(9):
        x_offset = B_SQUARE_SIZE * (i%3)
        y_offset = B_SQUARE_SIZE * (i//3)
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[i][row][col] == 1:
                    pygame.draw.circle(screen, color, ((int(col * SQUARE_SIZE + SQUARE_SIZE//2 + x_offset)), int(row * SQUARE_SIZE + SQUARE_SIZE//2 + y_offset)), CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif board[i][row][col] == 2:
                    pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE//4 + x_offset, row * SQUARE_SIZE + SQUARE_SIZE//4 + y_offset), 
                                    (col * SQUARE_SIZE + 3*SQUARE_SIZE//4 + x_offset, row * SQUARE_SIZE + 3*SQUARE_SIZE//4 + y_offset), CROSS_WIDTH)
                    pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE//4 + x_offset, row * SQUARE_SIZE + 3 * SQUARE_SIZE//4 + y_offset), 
                                    (col * SQUARE_SIZE + 3*SQUARE_SIZE//4 + x_offset, row * SQUARE_SIZE + SQUARE_SIZE//4 + y_offset), CROSS_WIDTH)

def b_draw_figures(color = WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if B_board[row][col] == 1:
                pygame.draw.circle(screen, color, ((int(row * B_SQUARE_SIZE + B_SQUARE_SIZE//2)), int(col * B_SQUARE_SIZE + B_SQUARE_SIZE//2)), B_CIRCLE_RADIUS, B_CIRCLE_WIDTH)
            elif B_board[row][col] == 2:
                pygame.draw.line(screen, color, (row * B_SQUARE_SIZE + B_SQUARE_SIZE//4, col * B_SQUARE_SIZE + B_SQUARE_SIZE//4), 
                                 (row * B_SQUARE_SIZE + 3*B_SQUARE_SIZE//4, col * B_SQUARE_SIZE + 3*B_SQUARE_SIZE//4), B_CROSS_WIDTH)
                pygame.draw.line(screen, color, (row * B_SQUARE_SIZE + B_SQUARE_SIZE//4, col * B_SQUARE_SIZE + 3 * B_SQUARE_SIZE//4), 
                                 (row * B_SQUARE_SIZE + 3*B_SQUARE_SIZE//4, col * B_SQUARE_SIZE + B_SQUARE_SIZE//4), B_CROSS_WIDTH)
                
                
                
                
def mark_sqaure(B_square, row, col, player):
    board[B_square][row][col] = player

def mark_b_square(row, col, player):
    B_board[row][col] = player

def avaliable_square(B_sqaure, row, col):
    return board[B_sqaure][row][col] == 0

def B_avaliable_square(row, col):
    return B_board[row][col] == 0

def is_board_full(check_board = board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board = board):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    if check_board[2][0] == player and check_board[1][1] == player and check_board[0][2] == player:
        return True
    return False

def B_check_win(player, check_board = B_board):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    if check_board[2][0] == player and check_board[1][1] == player and check_board[0][2] == player:
        return True
    return False

def minimax(minimax_board, B_square, depth, alpha, beta, is_maximizing):
    if B_check_win(2):
        return float('inf')
    if B_check_win(1):
        return float('-inf')
    if is_board_full(minimax_board[B_square]):
        return 0
    
    if (depth == 0):
        return evaluation(minimax_board)
    
    
    if is_maximizing:
        best_score = -1000000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[B_square][row][col] == 0:
                    minimax_board[B_square][row][col] = 2
                    best_score = max(minimax(minimax_board, row*3 + col, depth-1, alpha, beta, False), best_score)
                    minimax_board[B_square][row][col] = 0
                    alpha = max(alpha, best_score)
                    if beta<=alpha:
                        break
        return best_score
    else:
        best_score = 1000000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[B_square][row][col] == 0:
                    minimax_board[B_square][row][col] = 1
                    best_score = min(minimax(minimax_board, row*3 +col, depth-1, alpha, beta, True), best_score)
                    minimax_board[B_square][row][col] = 0
                    beta = min(beta, best_score)
                    if beta<=alpha:
                        break
        return best_score

def eval_board(check_board, is_big_board):
    cnt = 0
    if not is_big_board and check_win(2, check_board):
        return float('inf')
    if not is_big_board and check_win(1, check_board):
        return float('-inf')
    if check_board[1][1] == 1:
        cnt-=5
    if check_board[1][1] == 2:
        cnt+=5
    if check_board[0][0] == 1:
        cnt -= 3
    if check_board[2][0] == 1:
        cnt -= 3
    if check_board[0][2] == 1:
        cnt -= 3
    if check_board[2][2] == 1:
        cnt -= 3
    if check_board[0][0] == 2:
        cnt += 3
    if check_board[2][0] == 2:
        cnt += 3
    if check_board[0][2] == 2:
        cnt += 3
    if check_board[2][2] == 2:
        cnt += 3
    if check_board[1][0] == 1:
        cnt -= 2
    if check_board[0][1] == 1:
        cnt -= 2
    if check_board[1][2] == 1:
        cnt -= 2
    if check_board[2][1] == 1:
        cnt -= 2
    if check_board[1][0] == 2:
        cnt += 2
    if check_board[0][1] == 2:
        cnt += 2
    if check_board[1][2] == 2:
        cnt += 2
    if check_board[2][1] == 2:
        cnt += 2
    return cnt

def evaluation(minimax_board):
    cnt = 0
    good_dict = []
    bad_dict = []
    for i in range(3):
        for j in range(3):
            cnt += eval_board(minimax_board[i*3 + j], False)
    cnt += 10 * eval_board(B_board, True)
    
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if B_board[row][col] == 2:
                good_dict.append((row, col))
            if B_board[row][col] == 1:
                bad_dict.append((row, col))
    for i in range (len(good_dict)):
        for j in range (i+1):
            if i==j:
                pass
            if (abs(good_dict[i][0] - good_dict[j][0]) <= 1):
                cnt +=20
            if (abs(good_dict[i][1] - good_dict[j][1]) <= 1):
                cnt +=20
    for i in range (len(bad_dict)):
        for j in range (i+1):
            if i==j:
                pass
            if (abs(bad_dict[i][0] - bad_dict[j][0]) <= 1):
                cnt -= 20
            if (abs(bad_dict[i][1] - bad_dict[j][1]) <= 1):
                cnt -= 20
    return cnt
            
    
def best_move(B_square):
    if B_board[B_square % 3][B_square//3] != 0:
        print("YEp")
        best_score = -1000000
        move = (-1,-1)
        for i in range(9):
            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    if board[i][row][col] == 0 and B_board[i//3][i%3] == 0:
                        board[i][row][col] = 2
                        score = minimax(board, i, 3, float('-inf'), float('inf'), False)
                        print(score)
                        board[i][row][col] = 0
                        if score > best_score:
                            best_score = score
                            move = (row, col)
                            B_square = i
        if move != (-1,-1):
            mark_sqaure(B_square, move[0],move[1], 2)
    else: 
        best_score = -1000000
        move = (-1,-1)
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[B_square][row][col] == 0:
                    board[B_square][row][col] = 2
                    score = minimax(board, B_square, 3, float('-inf'), float('inf'), False)
                    board[B_square][row][col] = 0
                    if score > best_score:
                        best_score = score
                        move = (row, col)
        if move != (-1,-1):
            mark_sqaure(B_square, move[0],move[1], 2)
    print(best_score)

    return move
    

def restart_game():
    screen.fill(BLACK)
    draw_big_board()
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0
    
draw_big_board()    
draw_lines()
player = 1
game_over = False
curX = 1
curY = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            B_mouseX = event.pos[0] // B_SQUARE_SIZE
            B_mouseY = event.pos[1] // B_SQUARE_SIZE
            B_square = B_mouseY * 3 + B_mouseX
            mouseX = event.pos[0]%B_SQUARE_SIZE // SQUARE_SIZE
            mouseY = event.pos[1]%B_SQUARE_SIZE // SQUARE_SIZE
            if B_avaliable_square(B_mouseX, B_mouseY) and avaliable_square(B_square, mouseY, mouseX) and curX == B_mouseX and curY == B_mouseY or \
            (B_board[curX][curY] != 0 and avaliable_square(B_square, mouseY, mouseX) and B_avaliable_square(B_mouseX, B_mouseY)): 
                mark_sqaure(B_square, mouseY, mouseX, player)
                if check_win(player, board[B_square]):
                    B_board[B_mouseX][B_mouseY] = player
                if check_win(player, B_board):
                    game_over = True
                player = player % 2 + 1
                if not game_over:
                    curY, curX = best_move(mouseY*3 + mouseX)
                    if ((curX, curY) != (-1,-1)):
                        if check_win(player, board[curX*3 + curY]):
                            B_board[curY][curX] = player
                        if B_check_win(2) or check_win(2, B_board):
                            game_over = True
                        player = player % 2 + 1
                    if is_board_full(B_board):
                        game_over = True
                    
                
                
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1
    if not game_over:
        draw_figures()
        b_draw_figures()
    else:
        if check_win(1):
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif check_win(2):
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_figures(GRAY)
            draw_lines(GRAY)
    pygame.display.update()
                            