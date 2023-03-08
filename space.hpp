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
    /// @brief a stackheight of 0 means no containers, 1 means 1 container and so on;
    /// thus do not confuse stack height with the row coordinate in cells
    int* stackHeights = nullptr;
    public:
    Space(const int width, const int height);
    Cell getCell(const int col, const int row) const;
    void setAsHull(const int col, const int row);
    void addContainer(const int col, const int row, Container* container);
    void removeContainer(const int col, const int row);
    void setCell(const int col, const int row, const Cell& cell);
    int getStackHeight(const int col) const;
    int getWidth() const;
    int getHeight() const;
    // rule of Three
    ~Space();
    Space(const Space& rhs);
    Space& operator=(const Space& rhs);
};
#endif