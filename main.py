"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""

import pygame
from Engine.GameState import GameState
from Engine.Move import Move

WIDTH = 576
HEIGHT = 704
C_DIMENSION = 9
R_DIMENSION = 11
SQ_SIZE = HEIGHT // R_DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ["b0", "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9",
              "r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("image/" + piece + ".png"),
                                               (SQ_SIZE - 10, SQ_SIZE - 10))


def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    gs = GameState()
    valid_moves = gs.getAllPossibleMoves()
    move_made = False  # flag variable for when a move is made
    loadImages()
    running = True
    sq_selected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    player_clicks = []  # keep track of the player clicks
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()  # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):  # the user clicked the same square twice
                    sq_selected = ()  # deselect
                    player_clicks = []  # clear player clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)  # append for both 1st and 2nd clicks
                if len(player_clicks) == 2:  # after 2 click
                    move = Move(player_clicks[0], player_clicks[1], gs.board)
                    if move in valid_moves:
                        gs.makeMove(move)
                        move_made = True
                        sq_selected = ()  # reset user clicks
                        player_clicks = []
                    else:
                        player_clicks = [sq_selected]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:  # undo when 'z' is pressed
                    gs.undoMove()
                    move_made = True
        if move_made:
            valid_moves = gs.getAllPossibleMoves()
            move_made = False
        drawGameState(screen, gs, valid_moves, sq_selected)
        clock.tick(MAX_FPS)
        pygame.display.flip()


'''
Highlight square selected and moves for piece selected
'''


def highlightSquares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ('r' if gs.red_to_move else 'b'):  # sq_selected is a piece that can be moved
            # highlight selected square
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value -> 0 transparent; 255 opaque
            s.fill(pygame.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(pygame.Color('yellow'))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))


def drawGameState(screen, gs, valid_moves, sq_selected):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)
    highlightSquares(screen, gs, valid_moves, sq_selected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    colors = [pygame.Color("white"), pygame.Color("bisque3")]
    for r in range(R_DIMENSION):
        for c in range(C_DIMENSION):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for r in range(R_DIMENSION):
        for c in range(C_DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c * SQ_SIZE + 5, r * SQ_SIZE + 5, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
