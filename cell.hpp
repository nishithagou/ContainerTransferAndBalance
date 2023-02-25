#ifndef CELL_H
#define CELL_H
#include "container.hpp"
enum Condition  {HULL, OCCUPIED, EMPTY, UNOCCUPIABLE};

class Cell{
    private:
    char state;
    /// Cell does not do any deallocation of container pointer 
    Container* container = nullptr;
    public:
    Cell(char state): state(state) {}
    void setContainer(Container* newContainer) {container = newContainer;}
    void clearContainer() {container = nullptr;}
};
#endif