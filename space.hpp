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
    Cell** cells;
    public:
    Space(int width, int height);
    const int manhattanDistance(Coordinate start, Coordinate end);
    std::vector<Coordinate> tryAllColumns(int column) const;
    
};
#endif