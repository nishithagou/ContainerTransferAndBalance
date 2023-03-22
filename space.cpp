#include "space.hpp"

Space::Space(const int width, const int height): width(width), height(height)
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

char Space::getCellState(const int col, const int row) const
{
    return cells[col][row].getState();
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
    if (cells[col][row].getState() != EMPTY)
        throw 10;
    cells[col][row].setState(OCCUPIED);
    cells[col][row].setContainer(container);
    stackHeights[col] = height - row;
}

void Space::removeContainer(const int col, const int row)
{
    if (cells[col][row].getState() != OCCUPIED)
        throw 9;
    cells[col][row] = Cell(EMPTY);
    stackHeights[col]--;
}



void Space::setCell(const int col, const int row, const Cell &cell)
{
    if (cell.getState() == OCCUPIED){
        if (row < height - stackHeights[col]){
            stackHeights[col] = height - row;
        }
    }
    cells[col][row] = cell;
}

/// @brief Gets the height of the stack at a certain column. No bounds checking
/// @param col 
/// @return the stack height at the indicated column
int Space::getStackHeight(const int col) const
{
    return stackHeights[col];
}

/// @brief sorely needed
/// @param col 
/// @return 
Cell Space::getTopPhysicalCell(const int col) const
{
    if (stackHeights[col] == 0){
        return Cell(EMPTY); // no physical cell
    }
    else{
        // TODO Make sure this logic is correct
        return cells[col][height - stackHeights[col]];
    }
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

/// @brief Copy constructer
/// @param rhs 
Space::Space(const Space &rhs)
{
    height = rhs.height;
    width = rhs.width;
    stackHeights = new int[width];
    cells = new Cell*[width];
    for (int i = 0; i < width; i++){
        cells[i] = new Cell[height];
        stackHeights[i] = rhs.stackHeights[i];
        for (int j = 0; j < height; j++){
            cells[i][j] = rhs.cells[i][j];
        }
    }
}

/// @brief Assignment constructer
/// @param rhs 
/// @return 
Space &Space::operator=(const Space &rhs)
{
    if (this == &rhs)
        return *this;

    // deallocate old dynamically allocated data
    delete[] stackHeights;
    for (int i = 0; i < width; i++){
        delete[] cells[i];
    }
    delete[] rhs.cells;

    // allocate and take in new data
    height = rhs.height;
    width = rhs.width;
    stackHeights = new int[width];
    cells = new Cell*[width];
    for (int i = 0; i < width; i++){
        cells[i] = new Cell[height];
        stackHeights[i] = rhs.stackHeights[i];
        for (int j = 0; j < height; j++){
            cells[i][j] = rhs.cells[i][j];
        }
    }

    return *this;

}

/// @brief Move constructor
/// @param other 
Space::Space(Space &&other)
{
    this->width = other.width;
    this->height = other.height;
    this->cells = other.cells;
    this->stackHeights = other.stackHeights;
    other.cells = nullptr;
    other.stackHeights = nullptr;
}

/// @brief Move assignment
/// @param rhs 
/// @return a new Space object?
Space &Space::operator=(Space &&rhs)
{
    if (this != &rhs){
        this->width = rhs.width;
        this->height = rhs.height;

        // deallocate old data
        delete[] stackHeights;
        // this is how you deallocate a 2D array
        for (int i = 0; i < width; i++){
            delete[] cells[i];
        }
        delete[] cells;
        
        this->cells = rhs.cells;
        rhs.cells = nullptr;
        this->stackHeights = rhs.stackHeights;
        rhs.stackHeights = nullptr;
    }
    return *this;
    // I would like to thank and credit Sandesh from
    // https://www.codementor.io/@sandesh87/the-rule-of-five-in-c-1pdgpzb04f
    // for actually explaining the rule of five 
}
