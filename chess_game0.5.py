import pygame
from random import randrange
#menu = pygameMenu.TextMenu(screen, 200, 200,pygame.font.Font('arial',34), "Fucker")
def draw_field():
    global grid
    for x in range(8):
        for y in range(8):
            grid +=1
            pygame.draw.rect(screen,grid_colors[grid%2],(FIELD_START_POS[0] + CELL_SIZE*x, FIELD_START_POS[1] + CELL_SIZE*y, CELL_SIZE, CELL_SIZE),0)
        grid +=1
    pygame.draw.rect(screen,(0,0,0), (FIELD_START_POS[0],FIELD_START_POS[1],FIELD_LENGTH,FIELD_LENGTH), 1)


def check_cell(cell, opponent_figures):
    if (0 <= cell[0] <= 7) and (0 <= cell[1] <= 7):
        if field[cell[1]][cell[0]] == ' ':
            return 1
        elif cell in opponent_figures:
            return 2
        else:
            return 0
    else:
        return 0
    

def check_pawn(cell, opponent_figures):
    admissible = []
    if opponent_figures == black_figures:
        direction, start = 1, 1
    else:
        direction, start = -1, 6
    if cell[1] == start:
        for x,y in ([cell[0], cell[1] + 1*direction], [cell[0], cell[1] + 2*direction]):
            if check_cell([x, y], opponent_figures) == 1:
                admissible.append([x, y])
            else:
                break
    else:
        if check_cell((cell[0], cell[1] + 1*direction), opponent_figures) == 1:
            admissible.append([cell[0], cell[1] + 1*direction])
    if check_cell([cell[0] + 1, cell[1] + 1*direction], opponent_figures) == 2:
        admissible.append([cell[0] + 1, cell[1] + 1*direction])
    if check_cell([cell[0] - 1, cell[1] + 1*direction], opponent_figures) == 2:
        admissible.append([cell[0] - 1, cell[1] + 1*direction])
    return admissible


def check_king(cell, opponent_figures):
    admissible = []
    for x, y in ([-1,-1], [0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0]):
        if check_cell([cell[0] + x, cell[1] + y], opponent_figures): admissible.append([cell[0] + x, cell[1] + y])
    return admissible


def check_bishop(cell, opponent_figures):
    admissible = []
    for x,y in zip(range(cell[0]+1, 8), range(cell[1]-1, -1, -1)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]+1, 8), range(cell[1]+1, 8)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]-1, -1, -1), range(cell[1]+1,8)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]-1, -1, -1), range(cell[1]-1, -1, -1)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    return admissible


def check_knight(cell, opponent_figures):
    admissible = []
    for x,y in ([1,-2], [2,-1], [2,1], [1,2], [-1,2], [-2,1], [-2,-1], [-1,-2]):
        if check_cell([cell[0] + x, cell[1] + y], opponent_figures):
            admissible.append([cell[0] + x, cell[1] + y])
    return admissible


def check_rook(cell, opponent_figures):
    admissible = []
    for x in range(cell[0]+1, 8):
        code = check_cell([x, cell[1]], opponent_figures)
        if code == 1:
            admissible.append([x, cell[1]])
        elif code == 2:
            admissible.append([x, cell[1]])
            break
        else:
            break
    for x in range(cell[0]-1, -1, -1):
        code = check_cell([x, cell[1]], opponent_figures)
        if code == 1:
            admissible.append([x, cell[1]])
        elif code == 2:
            admissible.append([x, cell[1]])
            break
        else:
            break
    for y in range(cell[1]+1, 8):
        code = check_cell([cell[0], y], opponent_figures)
        if code == 1:
            admissible.append([cell[0], y])
        elif code == 2:
            admissible.append([cell[0], y])
            break
        else:
            break
    for y in range(cell[1]-1, -1, -1):
        code = check_cell([cell[0], y], opponent_figures)
        if code == 1:
            admissible.append([cell[0], y])
        elif code == 2:
            admissible.append([cell[0], y])
            break
        else:
            break    
    return admissible


def check_queen(cell, opponent_figures):
    admissible = []
    for x,y in zip(range(cell[0]+1, 8), range(cell[1]-1, -1, -1)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]+1, 8), range(cell[1]+1, 8)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]-1, -1, -1), range(cell[1]+1,8)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]-1, -1, -1), range(cell[1]-1, -1, -1)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x in range(cell[0]+1, 8):
        code = check_cell([x, cell[1]], opponent_figures)
        if code == 1:
            admissible.append([x, cell[1]])
        elif code == 2:
            admissible.append([x, cell[1]])
            break
        else:
            break
    for x in range(cell[0]-1, -1, -1):
        code = check_cell([x, cell[1]], opponent_figures)
        if code == 1:
            admissible.append([x, cell[1]])
        elif code == 2:
            admissible.append([x, cell[1]])
            break
        else:
            break
    for y in range(cell[1]+1, 8):
        code = check_cell([cell[0], y], opponent_figures)
        if code == 1:
            admissible.append([cell[0], y])
        elif code == 2:
            admissible.append([cell[0], y])
            break
        else:
            break
    for y in range(cell[1]-1, -1, -1):
        code = check_cell([cell[0], y], opponent_figures)
        if code == 1:
            admissible.append([cell[0], y])
        elif code == 2:
            admissible.append([cell[0], y])
            break
        else:
            break
    return admissible


def check_positions(cell, player_figures, opponent_figures):
    # cell = field[y][x] -> 'f','p'...
    admissible = []
    figure = field[cell[1]][cell[0]]
    if figure == 'p':
        admissible = check_pawn(cell, opponent_figures)
    elif figure == 'r':
        admissible = check_rook(cell, opponent_figures)
    elif figure == 'h':
        admissible = check_knight(cell, opponent_figures)
    elif figure == 'b':
        admissible = check_bishop(cell, opponent_figures)
    elif figure == 'q':
        admissible = check_queen(cell, opponent_figures)
    elif figure == 'k':
        admissible = check_king(cell, opponent_figures)
    return admissible
    

def draw_figures2():
    for figure in black_figures:
        x = figure[0] * CELL_SIZE + FIGURE_START_POS[0]
        y = figure[1] * CELL_SIZE + FIGURE_START_POS[1]
        pygame.draw.rect(screen,(0,0,0),(x, y, FIGURE_SIZE, FIGURE_SIZE), 0)
        figure_letter = text_font.render(field[figure[1]][figure[0]],0, COLOR_BACKGROUND)
        screen.blit(figure_letter, (x+MARGIN, y+MARGIN))        
    for figure in white_figures:
        x = figure[0] * CELL_SIZE + FIGURE_START_POS[0]
        y = figure[1]*CELL_SIZE + FIGURE_START_POS[1]
        pygame.draw.rect(screen,(255,255,255),(x, y, FIGURE_SIZE, FIGURE_SIZE), 0)
        pygame.draw.rect(screen,(0,0,0),(x, y, FIGURE_SIZE, FIGURE_SIZE), 1)
        figure_letter = text_font.render(field[figure[1]][figure[0]],0, COLOR_TEXT)
        screen.blit(figure_letter, (x+MARGIN, y+MARGIN))

        
def draw_figures():
    for figure in black_figures:
        x = figure[0] * CELL_SIZE + FIGURE_START_POS[0]
        y = figure[1] * CELL_SIZE + FIGURE_START_POS[1]
        if black_pictures[field[figure[1]][figure[0]]]:
            screen.blit(black_pictures[field[figure[1]][figure[0]]], (x,y))       
    for figure in white_figures:
        x = figure[0] * CELL_SIZE + FIGURE_START_POS[0]
        y = figure[1] * CELL_SIZE + FIGURE_START_POS[1]
        if black_pictures[field[figure[1]][figure[0]]]:
            screen.blit(white_pictures[field[figure[1]][figure[0]]], (x,y))


def take_figure(player_figures, opponent_figures):
    global selected, selected_figure, selected_cell, white_step, black_step
    opponent_figures.remove(selected_cell) # Удаляем фигуру у противника
    field[selected_cell[1]][selected_cell[0]] = field[selected_figure[1]][selected_figure[0]] # Перемещаем свою фигуру на место удаленной
    field[selected_figure[1]][selected_figure[0]] = ' ' # Очищаем клетку перемещенной фигуры
    player_figures[player_figures.index(selected_figure)] = selected_cell[:] # Меняем координаты выбранной фигуры на координаты выбранной ячейки
    white_step, black_step = black_step, white_step
    selected,selected_figure,selected_cell = False, None, None


def move_figure(player_figures):
    global selected, selected_figure, selected_cell, white_step, black_step
    field[selected_cell[1]][selected_cell[0]] = field[selected_figure[1]][selected_figure[0]] # Перемещаем фигуру на новое место
    field[selected_figure[1]][selected_figure[0]] = ' ' # Очищаем клетку перемещенной фигуры
    player_figures[player_figures.index(selected_figure)] = selected_cell[:]
    white_step, black_step = black_step, white_step
    selected,selected_figure,selected_cell = False, None, None


def init_pictures():
    for black in ('p','r','h','b','q','k'):
        if black == 'p':
            black_pictures[black] = pygame.transform.scale(pygame.image.load('pawn_black.png').convert(),(FIGURE_SIZE, FIGURE_SIZE))
            black_pictures[black].set_colorkey((0,255,0))
        elif black == 'r':
            black_pictures[black] = pygame.transform.scale(pygame.image.load('rook_black.png').convert(),(FIGURE_SIZE, FIGURE_SIZE))
            black_pictures[black].set_colorkey((0,255,0))
        elif black == 'h':
            black_pictures[black] = pygame.transform.scale(pygame.image.load('knight_black.png').convert(),(FIGURE_SIZE, FIGURE_SIZE))
            black_pictures[black].set_colorkey((0,255,0))
        elif black == 'b':
            black_pictures[black] = pygame.transform.scale(pygame.image.load('bishop_black.png').convert(),(FIGURE_SIZE, FIGURE_SIZE))
            black_pictures[black].set_colorkey((0,255,0))
        elif black == 'q':
            black_pictures[black] = pygame.transform.scale(pygame.image.load('queen_black.png').convert(),(FIGURE_SIZE, FIGURE_SIZE))
            black_pictures[black].set_colorkey((0,255,0))
        elif black == 'k':
            black_pictures[black] = pygame.transform.scale(pygame.image.load('king_black.png').convert(),(FIGURE_SIZE, FIGURE_SIZE))
            black_pictures[black].set_colorkey((0,255,0))
            
    for white in ('p','r','h','b','q','k'):
        if white == 'p':
            white_pictures[white] = pygame.transform.scale(pygame.image.load('pawn_white.png').convert(),(FIGURE_SIZE, FIGURE_SIZE))
            white_pictures[white].set_colorkey((0,255,0))
        elif white == 'r':
            white_pictures[white] = pygame.transform.scale(pygame.image.load('rook_white.png').convert(),(FIGURE_SIZE, FIGURE_SIZE))
            white_pictures[white].set_colorkey((0,255,0))
        elif white == 'h':
            white_pictures[white] = pygame.transform.scale(pygame.image.load('knight_white.png').convert(),(FIGURE_SIZE, FIGURE_SIZE))
            white_pictures[white].set_colorkey((0,255,0))
        elif white == 'b':
            white_pictures[white] = pygame.transform.scale(pygame.image.load('bishop_white.png').convert(),(FIGURE_SIZE, FIGURE_SIZE))
            white_pictures[white].set_colorkey((0,255,0))
        elif white == 'q':
            white_pictures[white] = pygame.transform.scale(pygame.image.load('queen_white.png').convert(),(FIGURE_SIZE, FIGURE_SIZE))
            white_pictures[white].set_colorkey((0,255,0))
        elif white == 'k':
            white_pictures[white] = pygame.transform.scale(pygame.image.load('king_white.png').convert(),(FIGURE_SIZE, FIGURE_SIZE))
            white_pictures[white].set_colorkey((0,255,0))
        

SIZE_X, SIZE_Y = 640, 480
DELAY = 30
COLOR_BACKGROUND = [255, 255, 255]
COLOR_TEXT = [0, 0, 0]
COLOR_YELLOW = (220, 220, 0)
COLOR_RED = (220, 0, 0)
COLOR_GREEN = (0, 220, 0)
CELL_SIZE = 40
FIGURE_SIZE = 30
FIELD_START_POS = [5, 5]
FIELD_LENGTH = 400
CELL_SIZE = int(FIELD_LENGTH/8)
MARGIN = 5 # Расстояние откраев ячейки до фигуры
FIGURE_SIZE = CELL_SIZE - MARGIN*2
FIGURE_START_POS = [FIELD_START_POS[0] + MARGIN, FIELD_START_POS[1] + MARGIN]

field = [
    ['r','h','b','q','k','b','h','r'],
    ['p','p','p','p','p','p','p','p'],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    ['p','p','p','p','p','p','p','p'],
    ['r','h','b','q','k','b','h','r'],
    ]

black_figures = [[j,i] for j in range(8) for i in range(6,8)]
white_figures = [[j,i] for j in range(8) for i in range(2)]
admissible_positions = []
selected_cell = None
selected_figure = None
game = True
selected = False
black_step = False
white_step = True
white_check = False
black_check = False
pygame.init()
pygame.display.set_caption('CHESS')
screen = pygame.display.set_mode((SIZE_X, SIZE_Y))
black_pictures = {}
white_pictures = {}
init_pictures()
text_font = pygame.font.SysFont('arial', 24)
grid = 0
grid_colors = {0:(200,200,200),1:(50,50,50)}
while game:
    pygame.time.delay(DELAY)
    screen.fill(COLOR_BACKGROUND)
    draw_field()
    if selected:
        for cell in admissible_positions:
            if selected_figure in white_figures and cell in black_figures:
                pygame.draw.rect(screen, COLOR_RED, (cell[0]*CELL_SIZE + FIELD_START_POS[0], cell[1]*CELL_SIZE + FIELD_START_POS[1], CELL_SIZE, CELL_SIZE), 4)
            elif selected_figure in black_figures and cell in white_figures:
                pygame.draw.rect(screen, COLOR_RED, (cell[0]*CELL_SIZE + FIELD_START_POS[0], cell[1]*CELL_SIZE + FIELD_START_POS[1], CELL_SIZE, CELL_SIZE), 4)
            else:
                pygame.draw.rect(screen, COLOR_YELLOW, (cell[0]*CELL_SIZE + FIELD_START_POS[0], cell[1]*CELL_SIZE + FIELD_START_POS[1], CELL_SIZE, CELL_SIZE), 4)
        pygame.draw.rect(screen, COLOR_GREEN, (selected_cell[0]*CELL_SIZE + FIELD_START_POS[0],selected_cell[1]*CELL_SIZE + FIELD_START_POS[1],CELL_SIZE,CELL_SIZE), 4)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x = ((pygame.mouse.get_pos()[0] - FIELD_START_POS[0]) // CELL_SIZE)
                y = ((pygame.mouse.get_pos()[1] - FIELD_START_POS[1]) // CELL_SIZE)
                selected_cell = [x, y]
                if selected_cell in white_figures and white_step:
                    selected_figure = selected_cell[:]
                    admissible_positions = check_positions(selected_figure[:], white_figures, black_figures)
                    selected = True
                elif selected_cell in black_figures and black_step:
                    selected_figure = selected_cell
                    admissible_positions = check_positions(selected_figure[:], black_figures, white_figures)
                    selected = True
                else:
                    if selected_figure != None and white_step: # Если выбрана фигура и ячейка
                        if selected_cell in black_figures and selected_cell in admissible_positions:
                            take_figure(white_figures, black_figures)
                        elif selected_cell in admissible_positions:
                            move_figure(white_figures)
                        else:
                            selected = False
                            selected_figure = None
                            selected_cell = None
                    elif selected_figure != None and black_step:
                        if selected_cell in white_figures and selected_cell in admissible_positions:
                            take_figure(black_figures, white_figures)
                        elif selected_cell in admissible_positions:
                            move_figure(black_figures)
                        else:
                            selected = False
                            selected_figure = None
                            selected_cell = None
            elif event.button == 3:
                x = (pygame.mouse.get_pos()[0] // CELL_SIZE) * CELL_SIZE + 5
                y = (pygame.mouse.get_pos()[1] // CELL_SIZE) * CELL_SIZE + 5
                if [x,y] in white_figures and white_step:
                    selected = False
                    selected_figure = None
                    selected_cell = None
                elif [x,y] in black_figures and black_step:
                    selected = False
                    selected_figure = None
                    selected_cell = None

                    
    step_white = text_font.render('white step: ' + str(white_step), 0, COLOR_TEXT)
    step_black = text_font.render('black step: ' + str(black_step), 0, COLOR_TEXT)
    check_white = text_font.render('white check: ' + str(white_check), 0, COLOR_TEXT)
    check_black = text_font.render('black check: ' + str(black_check), 0, COLOR_TEXT)
    screen.blit(step_white,(410, 20))
    screen.blit(step_black,(410, 50))
    screen.blit(check_white,(410, 100))
    screen.blit(check_black, (410, 130))
    draw_figures()    
    pygame.display.flip()
pygame.quit()
                
#  print(pygame.mouse.get_pos()) позиция мыши
#  rint(event.buttons[0]) нажата ли левая кнопка мыши

# pygame.MOUSEMOTION - event.buttons = (0,0,0)
# pygame.MOUSEBUTTONDWON - event.button = 1,2...5

# text_font = pygame.font.Font(FONT_FILE, 24)
# score_text = text_font.render('score:{: >3}'.format(int(score)),0,TEXT_COLOR)
# screen.blit(score_text, (tetris_len_x+10,240))
