#include "space.hpp"

Space::Space(const int width, const int height)
{
    cells = new Cell*[width];
    stackHeights = new int[width];
    for (int i = 0; i < width; i++){
        // kind of weird but it will make sense later on
        stackHeights[i] = 0; 
        cells[i] = new Cell[height];
        cells[i][0] = Cell(UNOCCUPIABLE);
    }   
}

/// @brief Gets a cell. No bounds checking
/// @param col 
/// @param row 
/// @return The cell at the col and row
Cell Space::getCell(const int col, const int row) const
{
    return cells[col][row];
}

/// @brief Sets a cell like with a ship as a hull thus limiting stack height
/// @param col 
/// @param row 
void Space::setAsHull(const int col, const int row)
{
    cells[col][row] = Cell(HULL);
    if (stackHeights[col] <= row) {
        stackHeights[col] = row + 1;
    }
}

void Space::addContainer(const int col, const int row, Container* container)
{
    // TODO: Error Handling
    if (cells[col][row].getState() != EMPTY)
        throw 10;
    cells[col][row].setState(OCCUPIED);
    cells[col][row].setContainer(container);
}

void Space::removeContainer(const int col, const int row)
{
    if (cells[col][row].getState() != OCCUPIED)
        throw 9;
    cells[col][row] = Cell(EMPTY);
}

void Space::setCell(const int col, const int row, const Cell &cell)
{
    cells[col][row] = cell;
}

int Space::getWidth() const
{
    return width;
}

int Space::getHeight() const
{
    return height;
}

Space::~Space()
{
    delete[] stackHeights;
    // this is how you deallocate a 2D array
    for (int i = 0; i < width; i++){
        delete[] cells[i];
    }
    delete[] cells;
}

/// @brief TODO Copy constructer
/// @param rhs 
Space::Space(const Space &rhs)
{
    
}

/// @brief Assignment constructer
/// @param rhs 
/// @return 
Space &Space::operator=(const Space &rhs)
{
    // TODO: insert return statement here
}
