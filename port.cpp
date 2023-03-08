#include "port.hpp"

/// @brief It wants a constructer for an abstract class sure why not
/// @param shipSize 
Port::Port(Coordinate shipSize): ship(Space(shipSize.x, shipSize.y)) {}

/// @brief Default Constructer not really useful I think
Port::Port(): ship(Space(0, 0)) {}

/// @brief Calculates A*
/// @return The asymptotically lower bound on the number of minutes to reach the solution
int Port::getTotalCost() const
{
    return costToGetHere + calculateHeuristic();
}

/// @brief Lots of arguments, but it's for a good reason
/// @param shipSize 
/// @param bufferSize 
/// @param shipLoad 
/// @param toLoad 
Transfer::Transfer(const Coordinate shipSize, const Coordinate bufferSize, 
    const std::vector<std::pair<Cell, Coordinate>>& shipLoad, 
    std::vector<Container*>& toLoad):
        Port(shipSize),
        buffer(Space(bufferSize.x, bufferSize.y))  
{
    for (size_t i = 0; i < shipLoad.size(); i++){
        const Coordinate CO = shipLoad[i].second;
        ship.setCell(CO.x, CO.y, shipLoad[i].first);
        if (shipLoad[i].first.getState() == OCCUPIED){
            std::pair<ContainerCoordinate, Container*> containerToOffload 
                (ContainerCoordinate(CO.x, CO.y), shipLoad[i].first.getContainer());
            toOffload.push_back(containerToOffload);
        }
    }
    // preallocate memory minor optimization
    this->toLoad.reserve(toLoad.size());
    // negative values are sentinel values that indicate the containers are not in the buffer
    // nor the ship but rather on the trucks
    const ContainerCoordinate notOnShip(-1, -1);
    for (Container* c:toLoad){
        std::pair<ContainerCoordinate, Container*> containerToLoad(notOnShip, c);
        this->toLoad.push_back(containerToLoad);
    }
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
    int minutesToOffload = 0;
    
    // incredibly mediocre heuristic to be finetuned

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