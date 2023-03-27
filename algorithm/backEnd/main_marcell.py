from space import Space

test = Space(12, 9)
cells = test.cells
for i in range(cells.__len__()):
    for j in range(cells[0].__len__()):
        print(str(cells[i][j]))
