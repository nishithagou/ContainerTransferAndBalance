#include "port.hpp"

/// @brief It wants a constructer for an abstract class sure why not
/// @param shipSize 
Port::Port(const Coordinate& shipSize, const Coordinate& bufferSize): 
ship(Space(shipSize.x, shipSize.y)), 
buffer(Space(bufferSize.x, bufferSize.y)),
cranePosition{Coordinate(0,0)}, craneState{SHIP} 
{}

/// @brief Default Constructer not really useful I think
Port::Port(): ship(Space(0, 0)), buffer(Space(0, 0)), cranePosition{Coordinate(0,0)}, craneState{SHIP} {}

/// @brief Will be useful for sorting. Sorts by the Port's internal cost
/// @param rhs 
/// @return whether this Port's cost is less than rhs's cost
const bool Port::operator<(const Port &rhs) const
{
    return costToGetHere < rhs.costToGetHere;
}

/// @brief Calculates A*
/// @return The asymptotically lower bound on the number of minutes to reach the solution
int Port::getTotalCost() const
{
    return costToGetHere + calculateHeuristic();
}

/// @brief Returns the move description
/// @return const string type
const std::string &Port::getMoveDescription() const
{
    return moveDescription;
}

/// @brief Lots of arguments, but it's for a good reason
/// @param shipSize 
/// @param bufferSize 
/// @param shipLoad 
/// @param toLoad 
Transfer::Transfer(
    // parameters
    const Coordinate& shipSize, 
    const Coordinate& bufferSize, 
    const std::vector<std::pair<Cell, Coordinate>>& shipLoad, 
    std::vector<Container*>& toLoad):
    // Field Initialization
    Port(shipSize, bufferSize) 
{
    for (size_t i = 0; i < shipLoad.size(); i++){
        const Coordinate CO = shipLoad[i].second;
        ship.setCell(CO.x, CO.y, shipLoad[i].first);
        // handles where we have containers that need to be offloaded
        if (shipLoad[i].first.getState() == OCCUPIED && shipLoad[i].first.getContainer()->isToBeOffloaded()){
            std::pair<ContainerCoordinate, Container*> containerToOffload 
                (ContainerCoordinate(CO.x, CO.y), shipLoad[i].first.getContainer());
            toOffload.push_back(containerToOffload);
        }
        // handles where we have containers that just need to stay in the ship after the operation
        if (shipLoad[i].first.getState() == OCCUPIED && !shipLoad[i].first.getContainer()->isToBeOffloaded()){
            std::pair<ContainerCoordinate, Container*> containerToStay
                (ContainerCoordinate(CO.x, CO.y), shipLoad[i].first.getContainer());
            toOffload.push_back(containerToStay);
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

/// @brief  Recall that our heuristic is admissible so long it never overestimates;
/// however, that also means the heuristic is best when it is as close to the actual
/// time but never overshooting it
/// @return how close are we to the goal state in terms of minutes 
int Transfer::calculateHeuristic() const
{

    // this is just the remaining number of containers that need to load. Will just
    // assume all containers can just phase through one another
    int minutesToLoad = toLoad.size() * 2;

    // this is the remaining number of containers that need to offload 
    // thanks to how we defined the coordinate system the manhattan distance is
    // calculated the same for both the ship and buffer
    int minutesToOffload = 0;
    for (const std::pair<ContainerCoordinate, Container*>& p: toOffload) {
        const ContainerCoordinate coord = p.first;
        minutesToOffload += 2 + coord.x + coord.y;
    }
    
    // for the edge case of having a container in the buffer that needs to be put
    // back onto the ship. If the container that needs to stay on the ship is already
    // on the ship, the heuristic for that will be 0
    int minutesToMoveFromBufferToShip = 0;
    for (const std::pair<ContainerCoordinate, Container*>& p: toStay) {
        const ContainerCoordinate coord = p.first;
        const Container* container = p.second;
        if (coord.isInBuffer)
            minutesToMoveFromBufferToShip += 4 + coord.x + coord.y;
    }
    // okay heuristic to be finetuned. Can certainly be better
    // TODO: finetune
    return minutesToLoad + minutesToOffload + minutesToMoveFromBufferToShip;
}

/// @brief Calculates the Manhattan Distance between two points in the Port. Assumes
/// parameters fed are actually real as this function does not check. Does not actually 
/// move anything. Also factors in the move distance for crane when moving between spaces
/// i.e. going from (0,0) on the ship takes 2 minutes to go to truck bay
/// @param start 
/// @param end 
/// @param startSpace 
/// @param endSpace 
/// @return the Manhattan Distance between two points.
int Transfer::calculateManhattanDistance(const ContainerCoordinate &start, 
    const ContainerCoordinate &end, 
    const char startSpace, 
    const char endSpace) const
{
    // this is an "intraspace" transfer so to speak
    if (startSpace == endSpace){
        // are we in the buffer or ship
        const Space* currSpace;
        if (start.isInBuffer){
            currSpace = &buffer;
        }
        else{
            currSpace = &ship;
        }
        // actually the most complicated 
        const int toMoveX = start.x - end.x;
        const int SPACE_HEIGHT = currSpace->getHeight();
        if (toMoveX > 0){
            // need to decrement x
            int minDepth = start.y;
            for (int x = start.x; x >= end.x; x--){
                const int minClearance = SPACE_HEIGHT - currSpace->getStackHeight(x);
                if (minDepth <= minClearance)
                    minDepth = minClearance;
            }
            return ( start.y - minDepth) + toMoveX + (end.y - minDepth);           
        }
        if (toMoveX < 0){
            // I have failed for I am writing boilerplate please forgive me as 
            // ctrl-C and ctrl-V and minorly tweak the code
            // need to increment x
            int minDepth = start.y;
            for (int x = start.x; x <= end.x; x++){
                const int minClearance = SPACE_HEIGHT - currSpace->getStackHeight(x);
                if (minDepth <= minClearance)
                    minDepth = minClearance;
            }
            return ( start.y - minDepth) + (-toMoveX) + (end.y - minDepth); 
        }
        else{
            // why are you trying to move within the same column?
            throw 6;
        }
    }
    // this is an "interspace" transfer so like moving between the buffer/ship/truckbay
    // actually made easier since the crane always has to go up to 0,0 coordinate
    else {
        if (startSpace == TRUCKBAY && endSpace == TRUCKBAY){
            // illogical move throw error
            throw 8;
        }
        // quite trivial
        if (startSpace == TRUCKBAY ){
            return end.x + end.y + 2;
        }
        if (endSpace == TRUCKBAY) {
            return start.x + start.y + 2;
        }
        // only dealing with distance between ship and buffer also pretty trivial
        return start.x + start.y + end.x + end.y + 4;
    }
}

/// @brief Compares whether the transfer ports are logically identical. Not by
/// comparing strings of containers but the states of the cells
/// @param rhs 
/// @return a boolean indicating logical equivalence
bool Transfer::operator==(const Transfer& rhs) const{
    if (craneState != rhs.craneState){
        return false;
    }
    if (cranePosition != rhs.cranePosition){
        return false;
    }
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

/// @brief 
/// @return 
std::list<Port*> Transfer::tryAllOperators() const {
    std::list<Port*> acc;
    return acc;
}