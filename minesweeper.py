import random
from tkinter import *

class Board:
    def __init__(self,dim_size,num_bombs):
        self.window = Tk()
        self.window.title('Minesweeper')
        img = PhotoImage(file='_internal/minesweeper.png')
        self.window.iconphoto(False,img)
        self.label = Label(self.window,text="MINESWEEPER",font=('Fixedsys', 40, 'bold'),fg='black')
        self.label.pack()
        self.playagainbutton = Button(self.window,text=" ^__^ ",fg='black',bg='#BEBEBE',height=2,
                                           width=4,state=DISABLED,command=self.reset)
        self.playagainbutton.pack()
        self.dim_size = dim_size #board dimensions
        self.num_bombs = num_bombs #number of bombs to be planted
        self.board = self.makenewboard() #func to make a new board (2d array)
        self.plant_bombs(self.board) #func to plan t bombs in array
        self.dug = set() #set to store already dug blocks
        self.flagged = set() #set to store flagged blocks
        self.board3 = self.makenewboard()

    def plant_bombs(self,board):
        bombs_planted = 0

        while bombs_planted < self.num_bombs:
            location = random.randint(0, self.dim_size ** 2 - 1)
            row = location // self.dim_size
            col = location % self.dim_size
            if board[row][col] == '@@':
                continue
            else:
                board[row][col] = '@@'
                bombs_planted += 1


    def askdifficulty(self):
        pass

    def flag(self,event,r,c):
        if (r,c) not in self.dug:
            self.dug.add((r,c))
            self.flagged.add((r, c))
            self.board3[r][c]['text'] = 'F'
            self.board3[r][c]['command'] = NONE
            self.board3[r][c]['bg'] = 'pink'
        elif (r,c) in self.flagged:
            self.flagged.remove((r,c))
            self.dug.remove((r, c))
            self.board3[r][c]['text'] = ' '
            self.board3[r][c]['command'] = lambda r=r,c=c:self.dig(r,c)
            self.board3[r][c]['bg'] = '#848884'


    # displays the n x n grid feild
    def addfeild(self):
        frame = Frame(self.window)
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                self.board3[r][c] = Button(frame,text=' ',
                                           command= lambda r=r,c=c:self.dig(r,c),
                                           font=('Fixedsys',2, 'bold'),
                                           height=1,
                                           width=2, bg= '#848884')
                self.board3[r][c].bind("<Button-3>",lambda event, r=r,c=c:self.flag(event,r=r,c=c))
                self.board3[r][c].grid(row=r, column=c)
        frame.pack(padx=10,pady=15)


    def makenewboard(self):
        board = [['[]' for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        return board

    def count(self,r,c):
        counter = 0
        squares = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        for square in squares:
            sqr_row = r + square[0]
            sqr_col = c + square[1]
            if (sqr_row >= 0 and sqr_row <= self.dim_size-1) and (sqr_col >= 0 and sqr_col <= self.dim_size-1):
                if self.board[sqr_row][sqr_col] == '@@':
                    counter += 1
        if counter == 0:
            return ' '
        return counter

    def revealbombs(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '@@':
                    if (r,c) in self.flagged:
                        self.board3[r][c]['text'] = '*'
                        self.board3[r][c]['bg'] = 'pink'
                    else:
                        self.board3[r][c]['text'] = '*'
                        self.board3[r][c]['bg'] = '#181818'
                self.board3[r][c]['state'] = DISABLED
        self.playagainbutton.config(state=NORMAL)

    def colorize(self,r,c,count):
        self.board3[r][c]['bg'] = '#C0C0C0'
        if count == ' ':
            self.board3[r][c]['text'] = count
            self.board3[r][c]['command'] = NONE
        elif (count <= 8) and (count >= 0):
            self.board3[r][c]['text'] = count
            self.board3[r][c]['command'] = NONE
            for i in range(1,8):
                if count == 1:
                    self.board3[r][c]['fg'] = 'blue'
                elif count == 2:
                    self.board3[r][c]['fg'] = 'green'
                elif count == 3:
                    self.board3[r][c]['fg'] = 'red'
                elif count == 4:
                    self.board3[r][c]['fg'] = 'brown'
                else:
                    self.board3[r][c]['fg'] = 'black'


    def dig(self,row,col):
        self.dug.add((row,col))
        squares = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        count = self.count(row, col)

        if self.board[row][col] == '@@':
            self.playagainbutton.config(text= " *__* ")
            self.board3[row][col]['text'] = '*'
            self.board3[row][col]['state'] = DISABLED
            self.board3[row][col]['bg'] = '#181818'
            self.revealbombs()
            return False

        if count != ' ':
            self.colorize(row,col,count)
            return True
        elif count == ' ':
            self.colorize(row,col,count)
            for square in squares:
                sqr_row = row + square[0]
                sqr_col = col + square[1]
                if ((sqr_row >= 0 and sqr_row<= self.dim_size-1) and
                        (sqr_col >= 0 and sqr_col <= self.dim_size-1) and
                        (sqr_row,sqr_col) not in self.dug):

                    self.dig(sqr_row, sqr_col)
            return True

    def reset(self):
        self.dug.clear()
        self.board = self.makenewboard()
        self.plant_bombs(self.board)
        self.playagainbutton.config(text=" ^__^ ")
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                self.board3[r][c]['text'] = ' '
                self.board3[r][c]['state'] = NORMAL
                self.board3[r][c]['fg'] = 'black'
                self.board3[r][c]['bg'] = '#848884'
                self.board3[r][c]['command'] = lambda r=r, c=c : self.dig(r,c)



def playgame(dim_size=20, num_bombs=20*3):  #increase or decrease num_bombs to change difficulty
    board = Board(dim_size,num_bombs)
    board.addfeild()
    Label(board.window,text='left click - dig',
                  font=('Fixedsys', 8, 'bold')).pack()
    Label(board.window, text='right click - flag',
          font=('Fixedsys', 8, 'bold'),pady=8).pack()
    board.window.mainloop()

if __name__ == '__main__':
    playgame()