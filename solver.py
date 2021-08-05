def isvalid(bo,num,pos):
    for i in range(len(bo)):
        if bo[i][pos[1]]==num and i!=pos[0]:
            return False
    for j in range(len(bo[0])):
        if bo[pos[0]][j]==num and j!=pos[1]:
            return False

    box_row=pos[0]//3
    box_col=pos[1]//3
    for i in range(box_row*3,(box_row*3)+3):
        for j in range(box_col*3,(box_col*3)+3):
            if bo[i][j]==num and (i,j)!=pos:
                return False
    return True

def solve(bo):
    pos = find(bo)
    if not pos:
        return True
    else:
        row,col = pos
    for i in range(1,10):
        if isvalid(bo,i,pos):
            bo[row][col] = i
            if solve(bo):
                return True
            bo[row][col] = 0
    return False
        
        


def find(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i,j)
    return None

def printboard(bo):
    for i in range(len(bo)):
        if i %3==0 and i!=0:
            print('-----------------------------')
        for j in range(len(bo[0])):
            if  j %3==0 and j!=0:
                print('|',end='')
            if j!=8:
                print(bo[i][j],end=' ')
            else:
                print(bo[i][j])
if __name__ == '__main__':
    board =[[3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0],
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0]]
    print(find(board))
    printboard(board)

    solve(board)
    
    printboard(board)



    
