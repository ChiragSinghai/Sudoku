import pygame
from solver import isvalid,solve
pygame.font.init()

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
        self.nrows = 9
        self.ncols = 9
        self.width = width
        self.height = height
        self.cubes = [[Cube(self.board[i][j],i,j,self.width,self.height) for j in range(self.ncols)]
                      for i in range(self.nrows)]
        self.selected = None

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
                self.cubes[i][j].set_value(4)
                self.cubes[i][j].draw(win)




class Cube:
    def __init__(self,value,x,y,width,height):
        self.width = width
        self.height = height
        self.row = x*self.width//9
        self.col = y*self.width//9
        self.value = value
        self.temp = value
        self.set = True if self.value else False
        self.selected = False


    def draw(self,win):
        fnt = pygame.font.SysFont("arial",30)
        gap = self.width//9
        if self.set:
            txt = fnt.render(str(self.value),1,(0,0,0))
            win.blit(txt, (self.row + (gap//2 - txt.get_width() // 2), self.col + (gap//2 - txt.get_height() // 2)))
        elif not self.set and self.value != 0:
            txt = fnt.render(str(self.value),1,(0,255,0))
            win.blit(txt,(self.row+(gap//2-txt.get_width()//2),self.col+(gap//2-txt.get_height()//2)))
        elif self.temp != 0:
            txt = fnt.render(str(self.temp),1,(128,128,128))
            win.blit(txt,(self.row+5,self.col+5))
        if self.selected and self.set:
            pygame.draw.rect(pygame.draw.rect(win, (255,0,0), (self.row,self.col, gap ,gap), 3))

    def set_value(self,val):
        self.value = val

    def set_temp(self,val):
        self.temp = val



def main():
    run = True
    Screen = pygame.display.set_mode((540,600))
    board = Board(540,540)

    pygame.display.set_caption('Soduko')
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        Screen.fill((255,255,255))
        board.draw(Screen)
        pygame.display.update()


main()