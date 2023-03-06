#ifndef SPACE_H
#define SPACE_H
#include <exception>
#include "cell.hpp"
#include "coordinate.hpp"
/// @brief Space defines either the ship or the buffer. Now to make the math easier
/// the top row is the index 0 row. That row is unoccupiable or else the crane would 
/// be blocked if it could be occupied by a container
class Space {
    private:
    int width, height;
    Cell** cells = nullptr;
    int* stackHeights = nullptr;
    public:
    Space(int width, int height);
    Cell getCell(int col, int row) const;
    void setAsHull(int col, int row);
    void addContainer(int col, int row, Container* container);
    void removeContainer(int col, int row);
    void setCell(int col, int row, Cell& cell);
    int getWidth() const;
    int getHeight() const;
    // rule of Three
    ~Space();
    Space(const Space& rhs);
    Space& operator=(const Space& rhs);
};
#endif