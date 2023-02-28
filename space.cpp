#include "space.hpp"

Space::Space(int width, int height)
{
    cells = new Cell*[width];
    for (int i = 0; i < width; i++){
        cells[width] = new Cell[height];
        cells[width][0] = Cell(UNOCCUPIABLE);
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
