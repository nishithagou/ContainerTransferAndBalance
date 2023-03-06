#include "port.hpp"

/// @brief It wants a constructer for an abstract class not sure why
/// @param shipSize 
Port::Port(Coordinate shipSize): ship(Space(shipSize.x, shipSize.y))
{}

Port::Port(): ship(Space(0, 0))
{
}

int Port::getTotalCost() const
{
    return costToGetHere + calculateHeuristic();
}

/// @brief Lots of arguments, but it's for a good reason
/// @param shipSize 
/// @param bufferSize 
/// @param shipLoad 
/// @param toLoad 
Transfer::Transfer(Coordinate shipSize, Coordinate bufferSize, 
    std::vector<std::pair<Cell, Coordinate>>& shipLoad, 
    std::vector<Container*>& toLoad):
buffer(Space(bufferSize.x, bufferSize.y))
{
    ship = Space(shipSize.x, shipSize.y);
    for (size_t i = 0; i < shipLoad.size(); i++){
        const Coordinate CO = shipLoad[i].second;
        ship.setCell(CO.x, CO.y, shipLoad[i].first);
        if (shipLoad[i].first.getState() == OCCUPIED){
            toOffload.push_back(shipLoad[i].first.getContainer());
        }
    }
    this->toLoad = toLoad;
}

/// @brief TODO
/// @return 
int Transfer::toHashIndex() const {
    return 0;
}

/// @brief TODO
/// @return 
int Transfer::calculateHeuristic() const
{
    // Recall that our heuristic is admissible so long it never overestimates
    // however that also means
    int minutesToLoad = toLoad.size() * 2;
}

bool Transfer::operator==(const Transfer& rhs) const{
    // find the first thing that is unequal
    // go through the ship's space
    for (int row = 0; row < ship.getHeight(); row++){
        for (int col = 0; col < ship.getWidth(); col++){
            if (rhs.ship.getCell(col, row).getState() != ship.getCell(col, row).getState())
                return false;
        }
    }
    // then the buffer's space room for optimization
    for (int row = 0; row < buffer.getHeight(); row++){
        for (int col = 0; col < buffer.getWidth(); col++){
            if (rhs.buffer.getCell(col, row).getState() != buffer.getCell(col, row).getState())
                return false;
        }
    }
    return true;
}