import sys
import time
import pygame
from solver import isvalid,find,solve

pygame.font.init()
start = None

class Board:
    board = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
             [5, 2, 0, 0, 0, 0, 0, 0, 0],
             [0, 8, 7, 0, 0, 0, 0, 3, 1],
             [0, 0, 3, 0, 1, 0, 0, 8, 0],
             [9, 0, 0, 8, 6, 3, 0, 0, 5],
             [0, 5, 0, 0, 9, 0, 6, 0, 0],
             [1, 3, 0, 0, 0, 0, 2, 5, 0],
             [0, 0, 0, 0, 0, 0, 0, 7, 4],
             [0, 0, 5, 2, 0, 6, 3, 0, 0]]

    def __init__(self,width,height):
        self.stack = []
        self.nrows = 9
        self.ncols = 9
        self.width = width
        self.height = height
        self.cubes = [[Cube(self.board[i][j],i,j,self.width,self.height) for j in range(self.ncols)]
                      for i in range(self.nrows)]
        self.selected = None
        self.updated_board = self.board

    def update_board(self):
        self.updated_board = [[self.cubes[i][j].value for j in range(self.ncols)]for i in range(self.nrows)]

    def place(self,val):
        i,j = self.selected
        self.cubes[i][j].set_value(val)
        self.update_board()
        if isvalid(self.updated_board,val,(i,j)):
            return True
        else:
            self.cubes[i][j].set_value(0)
            self.cubes[i][j].set_temp(0)
            return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def click(self, pos):

        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width // self.nrows
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None

    def draw(self,win):
        gap = self.width//self.nrows
        for i in range(self.nrows+1):
            if i % 3 == 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(win,(0,0,0), (0, i*gap), (self.width, i*gap),thickness)
            pygame.draw.line(win,(0,0,0),(i*gap,0),(i*gap,self.height),thickness)
        for i in range(self.nrows):
            for j in range(self.ncols):
                self.cubes[i][j].draw(win)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)
        elif not self.cubes[row][col].set:
            self.cubes[row][col].set_value(0)
            self.cubes[row][col].set_temp(0)

    def deselect(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                self.cubes[i][j].selected = False

    def select(self,row,col):
        # Reset all other
        self.deselect()
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def is_finished(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.cubes[i][j].value == 0:
                    return False
        return True



    def complete(self):
        self.updated_board = [[self.cubes[i][j].value if self.cubes[i][j].set else 0 for j in range(self.ncols)]
                              for i in range(self.nrows)]
        solve(self.updated_board)
        for i in range(self.nrows):
            for j in range(self.ncols):
                if not self.cubes[i][j].set:
                    self.cubes[i][j].set_value(self.updated_board[i][j])


    def callSolve(self,win):
        self.deselect()
        self.updated_board = [[self.cubes[i][j].value if self.cubes[i][j].set else 0 for j in range(self.ncols)]
                              for i in range(self.nrows)]

        self.solve_with_display(win)


    def solve_with_display(self,win):
        global start
        pos = find(self.updated_board)
        if not pos:
            return True
        else:
            row, col = pos

        for i in range(1, 10):
            if isvalid(self.updated_board, i, pos):
                self.cubes[row][col].selected = True
                #win.fill((255,255,255))
                self.updated_board[row][col] = i
                self.cubes[row][col].set_value(i)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                draw_window(win, self, round(time.time() - start))
                self.cubes[row][col].selected = False
                if self.solve_with_display(win):
                    return True

                self.updated_board[row][col] = 0
                self.cubes[row][col].set_value(0)
        return False

class Cube:
    def __init__(self,value,x,y,width,height):
        self.width = width
        self.height = height
        self.row = y*self.width//9
        self.col = x*self.width//9
        self.value = value
        self.temp = value
        self.set = True if self.value else False
        self.selected = False


    def draw(self,win):
        fnt = pygame.font.SysFont("arial",30)
        gap = self.width//9
        if self.set:
            txt = fnt.render(str(self.value),True,(0,0,0))
            win.blit(txt, (self.row + (gap//2 - txt.get_width() // 2), self.col + (gap//2 - txt.get_height() // 2)))
        elif not self.set and self.value != 0:
            txt = fnt.render(str(self.value),True,(0,255,0))
            win.blit(txt,(self.row+(gap//2-txt.get_width()//2),self.col+(gap//2-txt.get_height()//2)))
        elif self.temp != 0:
            txt = fnt.render(str(self.temp),True,(128,128,128))
            win.blit(txt,(self.row+5,self.col+5))
        if self.selected and not self.set:
            #print(self.row,self.col)
            pygame.draw.rect(win, (255,0,0), (self.row,self.col, gap,gap), 3)

    def set_value(self,val):
        self.value = val

    def set_temp(self,val):
        self.temp = val


def draw_time(win,sec):
    secs = sec % 60
    minutes = sec//60
    mat = " " + str(minutes) + ":" + str(secs)
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + mat, True, (0, 0, 0))
    win.blit(text, (540 - 160, 560))

def draw_window(win,board,play_time):
    win.fill((255, 255, 255))
    board.draw(win)
    draw_time(win, play_time)
    pygame.display.update()

def main():
    global start
    run = True
    Screen = pygame.display.set_mode((540,600))
    board = Board(540,540)
    key = None
    completed = False
    start = time.time()
    pygame.display.set_caption('Sudoku')
    while run:
        if not completed:
            play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_SPACE:
                    board.callSolve(Screen)
                    #board.complete()
                    play_time = round(time.time() - start)
                    completed = True
                if event.key == pygame.K_9:
                    key = 9

                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i,j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print('Success')
                        else:
                            print('Failure')
                        key = None
                    if board.is_finished():
                        print("Game over")
                        completed = True
                        run = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key:
            board.sketch(key)
        draw_window(Screen,board,play_time)


main()
pygame.quit()
