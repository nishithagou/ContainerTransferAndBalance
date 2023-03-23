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
    Cell(): state(EMPTY) {}
    Cell(const char state): state(state) {}
    Cell(Container* container): state{OCCUPIED}, container(container) {}
    void setContainer( Container* newContainer) {container = newContainer;}
    void clearContainer() {container = nullptr;}
    Container* getContainer() const { return container; }
    char getState() const { return state; }
    void setState(const char newState) {state = newState;}
};
#endif