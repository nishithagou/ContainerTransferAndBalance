#include "space.hpp"

Space::Space(int width, int height)
{
    cells = new Cell*[width];
    for (int i = 0; i < width; i++)
        cells[width] = new Cell[height];
}

/// @brief If you were to try to bring
/// @param column
/// @return
std::vector<Coordinate> Space::tryAllColumns(int column) const
{
    return std::vector<Coordinate>();
}