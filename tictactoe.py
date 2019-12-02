#!/usr/bin/python

# Tic-Tac-Toe
# pyGame Demo
# Nathan R. Yergler
# 13 May 2002

# import necessary modules
import checkbox
import pygame
from pygame.locals import *

# declare our global variables for the game
XO   = "X"   # track whose turn it is; X goes first
grid = [ [ None, None, None ], \
         [ None, None, None ], \
         [ None, None, None ] ]
running = True
winner = None

def button(board, msg, x, y, w, h, action=None):
    def text_objects(text, font):
        black = (0,0,0)
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        # pygame.draw.rect(board, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    #     pygame.draw.rect(board, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    board.blit(textSurf, textRect)

# declare our support functions
def text_to_screen(screen, text, x, y, size = 50,
            color = (200, 000, 000), font_type = 'data/fonts/orecrusherexpand.ttf'):
    try:

        text = str(text)
        font = pygame.font.Font(None, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception as e:
        print('Font Error, saw it coming')
        raise e

def gdprConcents(ttt):
    
    p1_cb = checkbox.Checkbox(ttt, 80, 150, caption='Player 1 consent', text_offset=(75,1))
    p2_cb = checkbox.Checkbox(ttt, 80, 170, caption='Player 2 consent', text_offset=(75,1))

    board  = pygame.Surface (ttt.get_size())
    board  = board.convert()
    board.fill ((250, 250, 250))

    global running
    running = True
    def pclick():
        global running
        running = False
    a, b = 0, 0
    while running:
        # print(running)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            # print(event.__dict__)
            # if (event.)
            p1_cb.update_checkbox(event)
            p2_cb.update_checkbox(event)
        board.fill ((250, 250, 250))
        
        text_to_screen(board, 'GDPR compliance', 55, 10, size=32)

        button(board, 'Continue',130,290,30,30,pclick)
        
        ttt.blit (board, (0, 0))
        p1_cb.render_checkbox()
        p2_cb.render_checkbox()
        pygame.display.flip()

    print(p1_cb.is_checked(), p2_cb.is_checked())

def initBoard(ttt):
    # initialize the board and return it as a variable
    # ---------------------------------------------------------------
    # ttt : a properly initialized pyGame display variable

    # set up the background surface
    background = pygame.Surface (ttt.get_size())
    background = background.convert()
    background.fill ((250, 250, 250))

    # draw the grid lines
    # vertical lines...
    pygame.draw.line (background, (0,0,0), (100, 0), (100, 300), 2)
    pygame.draw.line (background, (0,0,0), (200, 0), (200, 300), 2)

    # horizontal lines...
    pygame.draw.line (background, (0,0,0), (0, 100), (300, 100), 2)
    pygame.draw.line (background, (0,0,0), (0, 200), (300, 200), 2)

    # return the board
    return background

def drawStatus (board):
    # draw the status (i.e., player turn, etc) at the bottom of the board
    # ---------------------------------------------------------------
    # board : the initialized game board surface where the status will
    #         be drawn

    # gain access to global variables
    global XO, winner

    # determine the status message
    if (winner is None):
        message = XO + "'s turn"
    else:
        message = winner + " won!"
        
    # render the status message
    font = pygame.font.Font(None, 24)
    text = font.render(message, 1, (10, 10, 10))

    # copy the rendered message onto the board
    board.fill ((250, 250, 250), (0, 300, 300, 25))
    board.blit(text, (10, 300))

def showBoard (ttt, board):
    # redraw the game board on the display
    # ---------------------------------------------------------------
    # ttt   : the initialized pyGame display
    # board : the game board surface

    drawStatus (board)
    ttt.blit (board, (0, 0))
    pygame.display.flip()
    
def boardPos (mouseX, mouseY):
    # given a set of coordinates from the mouse, determine which board space
    # (row, column) the user clicked in.
    # ---------------------------------------------------------------
    # mouseX : the X coordinate the user clicked
    # mouseY : the Y coordinate the user clicked

    # determine the row the user clicked
    if (mouseY < 100):
        row = 0
    elif (mouseY < 200):
        row = 1
    else:
        row = 2

    # determine the column the user clicked
    if (mouseX < 100):
        col = 0
    elif (mouseX < 200):
        col = 1
    else:
        col = 2

    # return the tuple containg the row & column
    return (row, col)

def drawMove (board, boardRow, boardCol, Piece):
    # draw an X or O (Piece) on the board in boardRow, boardCol
    # ---------------------------------------------------------------
    # board     : the game board surface
    # boardRow,
    # boardCol  : the Row & Col in which to draw the piece (0 based)
    # Piece     : X or O
    
    # determine the center of the square
    centerX = ((boardCol) * 100) + 50
    centerY = ((boardRow) * 100) + 50

    # draw the appropriate piece
    if (Piece == 'O'):
        pygame.draw.circle (board, (0,0,0), (centerX, centerY), 44, 2)
    else:
        pygame.draw.line (board, (0,0,0), (centerX - 22, centerY - 22), \
                         (centerX + 22, centerY + 22), 2)
        pygame.draw.line (board, (0,0,0), (centerX + 22, centerY - 22), \
                         (centerX - 22, centerY + 22), 2)

    # mark the space as used
    grid [boardRow][boardCol] = Piece
    
def clickBoard(board):
    # determine where the user clicked and if the space is not already
    # occupied, draw the appropriate piece there (X or O)
    # ---------------------------------------------------------------
    # board : the game board surface
    
    global grid, XO
    
    (mouseX, mouseY) = pygame.mouse.get_pos()
    (row, col) = boardPos (mouseX, mouseY)

    # make sure no one's used this space
    if ((grid[row][col] == "X") or (grid[row][col] == "O")):
        # this space is in use
        return

    # draw an X or O
    drawMove (board, row, col, XO)

    # toggle XO to the other player's move
    if (XO == "X"):
        XO = "O"
    else:
        XO = "X"
    
def gameWon(board):
    # determine if anyone has won the game
    # ---------------------------------------------------------------
    # board : the game board surface
    
    global grid, winner

    # check for winning rows
    for row in range (0, 3):
        if ((grid [row][0] == grid[row][1] == grid[row][2]) and \
           (grid [row][0] is not None)):
            # this row won
            winner = grid[row][0]
            pygame.draw.line (board, (250,0,0), (0, (row + 1)*100 - 50), \
                              (300, (row + 1)*100 - 50), 2)
            break

    # check for winning columns
    for col in range (0, 3):
        if (grid[0][col] == grid[1][col] == grid[2][col]) and \
           (grid[0][col] is not None):
            # this column won
            winner = grid[0][col]
            pygame.draw.line (board, (250,0,0), ((col + 1)* 100 - 50, 0), \
                              ((col + 1)* 100 - 50, 300), 2)
            break

    # check for diagonal winners
    if (grid[0][0] == grid[1][1] == grid[2][2]) and \
       (grid[0][0] is not None):
        # game won diagonally left to right
        winner = grid[0][0]
        pygame.draw.line (board, (250,0,0), (50, 50), (250, 250), 2)

    if (grid[0][2] == grid[1][1] == grid[2][0]) and \
       (grid[0][2] is not None):
        # game won diagonally right to left
        winner = grid[0][2]
        pygame.draw.line (board, (250,0,0), (250, 50), (50, 250), 2)

# --------------------------------------------------------------------
# initialize pygame and our window
pygame.init()
ttt = pygame.display.set_mode ((300, 325))
pygame.display.set_caption ('Tic-Tac-Toe')

gdprConcents(ttt)
# create the game board
board = initBoard (ttt)


# main event loop
running = 1

while (running == 1):
    for event in pygame.event.get():
        if event.type is QUIT:
            running = 0
        elif event.type is MOUSEBUTTONDOWN:
            # the user clicked; place an X or O
            clickBoard(board)

        # check for a winner
        gameWon (board)

        # update the display
        showBoard (ttt, board)