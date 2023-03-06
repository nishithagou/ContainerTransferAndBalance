#include "space.hpp"

Space::Space(int width, int height)
{
    cells = new Cell*[width];
    stackHeights = new int[width];
    for (int i = 0; i < width; i++){
        // kind of weird but it will make sense later on
        stackHeights[i] = height; 
        cells[i] = new Cell[height];
        cells[i][0] = Cell(UNOCCUPIABLE);
    }   
}

/// @brief Gets a cell. No bounds checking
/// @param col 
/// @param row 
/// @return The cell at the col and row
Cell Space::getCell(int col, int row) const
{
    return cells[col][row];
}

/// @brief Sets a cell like with a ship as a hull thus limiting stack height
/// @param col 
/// @param row 
void Space::setAsHull(int col, int row)
{
    cells[col][row] = Cell(HULL);
    if (stackHeights[col] < row + 1 ){
        stackHeights[col] = row + 1;
    }
}

void Space::addContainer(int col, int row, Container* container)
{
    // TODO: Error Handling
    if (cells[col][row].getState() != EMPTY)
        throw 10;
    cells[col][row].setState(OCCUPIED);
    cells[col][row].setContainer(container);
}

void Space::removeContainer(int col, int row)
{
    if (cells[col][row].getState() != OCCUPIED)
        throw 9;
    cells[col][row] = Cell(EMPTY);
}
