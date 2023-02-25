#ifndef SPACE_H
#define SPACE_H
#include "cell.hpp"
/// @brief Space defines either the ship or the buffer. Now to make the math easier
/// the top row is the 0th row. It is unoccupiable or else the crane would be blocked if
/// it could be occupied by a container
class Space {
    private:
    Cell** cells;
    public:
    Space(int width, int height);
    const int manhattanDistance(int firstX, int firstY, int secondX, int secondY);
    
};
#endif