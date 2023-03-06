#ifndef SPACE_H
#define SPACE_H
#include <vector>
#include "cell.hpp"
#include "coordinate.hpp"
/// @brief Space defines either the ship or the buffer. Now to make the math easier
/// the top row is the index 0 row. That row is unoccupiable or else the crane would 
/// be blocked if it could be occupied by a container
class Space {
    private:
    int width, height;
    Cell** cells;
    int* stackHeights;
    public:
    Space(int width, int height);
    Cell getCell(int col, int row) const;
    void setAsHull(int col, int row);
};
#endif