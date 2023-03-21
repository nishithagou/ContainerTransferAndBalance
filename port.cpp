#include "port.hpp"

/// @brief It wants a constructer for an abstract class sure why not
/// @param shipSize
Port::Port(const Coordinate &shipSize, const Coordinate &bufferSize) : // field initialization
                                                                       ship(Space(shipSize.x, shipSize.y)),
                                                                       buffer(Space(bufferSize.x, bufferSize.y)),
                                                                       cranePosition{Coordinate(0, 0)}, craneState{SHIP}, costToGetHere{0}
{
}

/// @brief Default Constructer not really useful I think
Port::Port() : ship(Space(0, 0)), buffer(Space(0, 0)),
               cranePosition{Coordinate(0, 0)}, craneState{SHIP}, costToGetHere{0} {}

/// @brief Will be useful for sorting. Sorts by the Port's internal cost
/// @param rhs
/// @return whether this Port's cost is less than rhs's cost
const bool Port::operator<(const Port &rhs) const
{
    return aStarCost < rhs.aStarCost;
}

/// @brief Calculates A*
/// @return The asymptotically lower bound on the number of minutes to reach the solution
void Port::calculateAStar()
{
    aStarCost = costToGetHere + calculateHeuristic();
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
    const Coordinate &shipSize,
    const Coordinate &bufferSize,
    const std::vector<std::pair<Cell, Coordinate>> &shipLoad,
    std::vector<Container *> &toLoad) : // Field Initialization
                                        Port(shipSize, bufferSize)
{
    for (size_t i = 0; i < shipLoad.size(); i++)
    {
        const Coordinate CO = shipLoad[i].second;
        ship.setCell(CO.x, CO.y, shipLoad[i].first);
        // handles where we have containers that need to be offloaded
        if (shipLoad[i].first.getState() == OCCUPIED && shipLoad[i].first.getContainer()->isToBeOffloaded())
        {
            std::pair<ContainerCoordinate, Container *> containerToOffload(ContainerCoordinate(CO.x, CO.y), shipLoad[i].first.getContainer());
            toOffload.push_back(containerToOffload);
        }
        // handles where we have containers that just need to stay in the ship after the operation
        if (shipLoad[i].first.getState() == OCCUPIED && !shipLoad[i].first.getContainer()->isToBeOffloaded())
        {
            std::pair<ContainerCoordinate, Container *> containerToStay(ContainerCoordinate(CO.x, CO.y), shipLoad[i].first.getContainer());
            toOffload.push_back(containerToStay);
        }
    }
    // preallocate memory minor optimization
    this->toLoad.reserve(toLoad.size());
    // negative values are sentinel values that indicate the containers are not in the buffer
    // nor the ship but rather on the trucks
    const ContainerCoordinate notOnShip(-1, -1);
    for (Container *c : toLoad)
    {
        std::pair<ContainerCoordinate, Container *> containerToLoad(notOnShip, c);
        this->toLoad.push_back(containerToLoad);
    }
}

/// @brief TODO
/// I think this implementation is incorrect
/// @return
int Transfer::toHashIndex() const
{
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
    for (const std::pair<ContainerCoordinate, Container *> &p : toOffload)
    {
        const ContainerCoordinate coord = p.first;
        minutesToOffload += 2 + coord.x + coord.y;
    }

    // for the edge case of having a container in the buffer that needs to be put
    // back onto the ship. If the container that needs to stay on the ship is already
    // on the ship, the heuristic for that will be 0
    int minutesToMoveFromBufferToShip = 0;
    for (const std::pair<ContainerCoordinate, Container *> &p : toStay)
    {
        const ContainerCoordinate coord = p.first;
        const Container *container = p.second;
        if (coord.isInBuffer)
            minutesToMoveFromBufferToShip += 4 + coord.x + coord.y;
    }
    // okay heuristic to be finetuned. Can certainly be better
    // TODO: finetune
    return minutesToLoad + minutesToOffload + minutesToMoveFromBufferToShip;
}

/// @brief Just moves the crane and container if applicable. Does nothing else. Help cut down on the boilerplate
/// @param container a container; nullptr if just moving the crane
/// @param start 
/// @param end 
/// @param startSpace 
/// @param endSpace 
void Transfer::moveContainerAndCrane(Container *container, const Coordinate &start, const Coordinate &end, 
    const char startSpace, const char endSpace)
{
    // just moving the crane
    if (container == nullptr){
        cranePosition = end;
        craneState = endSpace;
    }
    // moving the crane and the container c
    else{
        cranePosition = end;
        craneState = endSpace;
        // add container at end
        if (endSpace == BUFFER){
            buffer.addContainer(end.x, end.y, container);
        }
        else if (endSpace == SHIP){
            ship.addContainer(end.x, end.y, container);
        }
        // remove container at beginning
        if (startSpace == BUFFER){
            buffer.removeContainer(end.x, end.y);
        }
        else if (startSpace == SHIP){
            ship.removeContainer(end.x, end.y);
        }
    }
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
int Port::calculateManhattanDistance(const Coordinate &start,
                                     const Coordinate &end,
                                     const char startSpace,
                                     const char endSpace) const
{
    // this is an "intraspace" transfer so to speak
    if (startSpace == endSpace)
    {
        // are we in the buffer or ship
        const Space *currSpace;
        if (startSpace == BUFFER)
        {
            currSpace = &buffer;
        }
        else
        {
            currSpace = &ship;
        }

        // actually the most complicated to calculate

        const int toMoveX = start.x - end.x;
        const int SPACE_HEIGHT = currSpace->getHeight();
        if (toMoveX > 0)
        {
            // need to decrement x
            int minDepth = start.y;
            for (int x = start.x; x >= end.x; x--)
            {
                const int minClearance = SPACE_HEIGHT - currSpace->getStackHeight(x);
                if (minDepth <= minClearance)
                    minDepth = minClearance;
            }
            return (start.y - minDepth) + toMoveX + (end.y - minDepth);
        }
        if (toMoveX < 0)
        {
            // I have failed for I am writing boilerplate please forgive me as
            // ctrl-C and ctrl-V and minorly tweak the code
            // need to increment x
            int minDepth = start.y;
            for (int x = start.x; x <= end.x; x++)
            {
                const int minClearance = SPACE_HEIGHT - currSpace->getStackHeight(x);
                if (minDepth <= minClearance)
                    minDepth = minClearance;
            }
            return (start.y - minDepth) + (-toMoveX) + (end.y - minDepth);
        }
        else
        {
            // why are you trying to move within the same column?
            throw 6;
        }
    }
    // this is an "interspace" transfer so like moving between the buffer/ship/truckbay
    // actually made easier since the crane always has to go up to 0,0 coordinate
    else
    {
        if (startSpace == TRUCKBAY && endSpace == TRUCKBAY)
        {
            // illogical move throw error
            throw 8;
        }
        // quite trivial
        if (startSpace == TRUCKBAY)
        {
            return end.x + end.y + 2;
        }
        if (endSpace == TRUCKBAY)
        {
            return start.x + start.y + 2;
        }
        // only dealing with distance between ship and buffer also pretty trivial
        return start.x + start.y + end.x + end.y + 4;
    }
}

/// @brief Compares whether the ports are logically identical. Not by
/// comparing strings of containers but the states of the cells
/// @param rhs
/// @return a boolean indicating logical equivalence
bool Port::operator==(const Port &rhs) const
{
    if (craneState != rhs.craneState)
    {
        return false;
    }
    if (cranePosition != rhs.cranePosition)
    {
        return false;
    }
    // find the first thing that is unequal
    // go through the ship's space
    for (int row = 0; row < ship.getHeight(); row++)
    {
        for (int col = 0; col < ship.getWidth(); col++)
        {
            if (rhs.ship.getCell(col, row).getState() != ship.getCell(col, row).getState())
                return false;
        }
    }
    // then the buffer's space room for optimization
    for (int row = 0; row < buffer.getHeight(); row++)
    {
        for (int col = 0; col < buffer.getWidth(); col++)
        {
            if (rhs.buffer.getCell(col, row).getState() != buffer.getCell(col, row).getState())
                return false;
        }
    }
    return true;
}

/// @brief TODO this requires thought
/// This function needs to
/// 1. generate all valid Transfer translations including some just moving the crane w/o
/// container
/// 2. Call to calculate the cost with A*
/// @return
std::list<Port *> &Transfer::tryAllOperators() const
{
    std::list<Port *> acc;
    // yo know I'm legit when I use a switch statement
    switch (craneState)
    {
    case SHIP:
    {
        break;
    }
    case BUFFER:
    {
        const Coordinate START_BUFFER_COORDINATE(cranePosition);

        // sanity check
        if (buffer.getCell(START_BUFFER_COORDINATE.x, START_BUFFER_COORDINATE.y).getState()
            != OCCUPIED){
            // why is the crane in the position with no container?
            // makes no sense
            // should not be possible so throw exeption
            throw 5;
        }

        // get container
        Container* toMove = buffer.getCell(START_BUFFER_COORDINATE.x, START_BUFFER_COORDINATE.y).getContainer();

        // move container within buffer or move to ship or if appicable, the truck bay
        // or just move crane 

        for (int i = 0; i < buffer.getWidth(); i++){
            if (i != START_BUFFER_COORDINATE.x && buffer.getStackHeight(i) < buffer.getHeight() - 1){
                Transfer *deriv = new Transfer(*this);
                
                const ContainerCoordinate NEW_COORD =
                    ContainerCoordinate(i, buffer.getHeight() - buffer.getStackHeight(i));
                
                int translationMove = calculateManhattanDistance(START_BUFFER_COORDINATE, NEW_COORD, BUFFER, BUFFER);
                // do not need to change the crane state
                // deriv->craneState = BUFFER;
                deriv->cranePosition = NEW_COORD;
                deriv->costToGetHere += translationMove;
                // make another derivative where it's just moving the crane not the container
                Transfer* noMoveContainer = new Transfer(*deriv);
                // remove the container at its original position 
                deriv->buffer.removeContainer(START_BUFFER_COORDINATE.x, START_BUFFER_COORDINATE.y);
                // update 
                deriv->calculateAStar();
                // I am not sure if the inheritance with pointers work gettin' some CS12 flashbacks
                acc.push_back(deriv);
            }
        }
        
        break;
    }
    case TRUCKBAY:
    {
        // Truck coordinate can actually be whatever because manhattan distance transitions ignores it because
        // it is in a TRUCKBAY state
        const Coordinate TRUCK(0, 0);
        // if the crane is at the truck bay, if there are no containers to load
        // just move the
        // crane to all valid spaces which are positions which have a container
        // but do it for both if there are no containers and if there are 
        // see if stackHeights are greater than 0 which indicates a container
        // for buffer
        for (int i = 0; i < buffer.getWidth(); i++)
        {
            if (buffer.getStackHeight(i) > 0)
            {
                // let's hope the copy constructor works
                Transfer *deriv = new Transfer(*this);
                const ContainerCoordinate NEW_COORD = ContainerCoordinate(i, buffer.getHeight() - buffer.getStackHeight(i));
                int translationMove = calculateManhattanDistance(TRUCK, NEW_COORD, TRUCKBAY, BUFFER);
                deriv->moveContainerAndCrane(nullptr, TRUCK, NEW_COORD, TRUCKBAY, BUFFER);
                deriv->costToGetHere += translationMove;
                deriv->calculateAStar();
                // I am not sure if the inheritance with pointers work gettin' some CS12 flashbacks
                acc.push_back(deriv);
            }
        }
        // for ship
        // do not move crane to a HULL or empty position as that is pointless
        for (int i = 0; i < ship.getWidth(); i++)
        {
            if (ship.getStackHeight(i) > 0 && 
                ship.getTopPhysicalCell(i).getState() != HULL)
            {
                // let's hope the copy constructor works
                Transfer *deriv = new Transfer(*this);
                const ContainerCoordinate NEW_COORD =
                    ContainerCoordinate(i, buffer.getHeight() - buffer.getStackHeight(i));
                int translationMove = calculateManhattanDistance(TRUCK, NEW_COORD, TRUCKBAY, SHIP);
                deriv->moveContainerAndCrane(nullptr, TRUCK, NEW_COORD, TRUCKBAY, SHIP);
                deriv->costToGetHere += translationMove;
                deriv->calculateAStar();
                // I am not sure if the inheritance with pointers work gettin' some CS12 flashbacks
                acc.push_back(deriv);
            }
        }
        // if there are still containers to load we must add moving the crane empty
        // like with the previous lift statement
        // and moving the crane with a container to all empty, availble spots in the ship
        // and bufer
        if (toLoad.size() != 0){
            // simulating taking one of the toLoad containers to all possible positions 
            // in ship and buffer
            Container* toMove = toLoad.back().second;
            std::vector<std::pair<ContainerCoordinate, Container*>> newToLoad;
            for (std::pair<ContainerCoordinate, Container*> p:toLoad){
                newToLoad.push_back(p);
            }
            // remove toMove Container 
            newToLoad.pop_back();
            for (int i = 0; i < buffer.getWidth(); i++){
                if (buffer.getStackHeight(i) < buffer.getHeight() - 1){

                    Transfer *deriv = new Transfer(*this);

                    // to create a new ContainerCoordinate in the buffer
                    const ContainerCoordinate NEW_COORD =
                        ContainerCoordinate(i, buffer.getHeight() - buffer.getStackHeight(i));
                    
                    // calculate such move to the new coordinate
                    int translationMove = 
                        calculateManhattanDistance(TRUCK, NEW_COORD, TRUCKBAY, BUFFER);
                    
                    deriv->moveContainerAndCrane(toMove, TRUCK, NEW_COORD, TRUCKBAY, BUFFER);


                    // calculate g(n)
                    deriv->costToGetHere += translationMove;
                    
                    // calculate A*
                    deriv->calculateAStar();

                    acc.push_back(deriv);
                }

            }
            
            // apologies more boilerplate for transfering a container to the ship
            for (int i = 0; i < ship.getWidth(); i++){
                if (ship.getStackHeight(i) < ship.getHeight() - 1){

                    Transfer *deriv = new Transfer(*this);

                    // to create a new ContainerCoordinate in the ship
                    const ContainerCoordinate NEW_COORD =
                        ContainerCoordinate(i, ship.getHeight() - ship.getStackHeight(i));
                    
                    // calculate such move to the new coordinate
                    int translationMove = 
                        calculateManhattanDistance(TRUCK, NEW_COORD, TRUCKBAY, SHIP);

                    // move crane to ship 
                    deriv->craneState = SHIP;
                    deriv->cranePosition = NEW_COORD;

                    // calculate g(n)
                    deriv->costToGetHere += translationMove;
                    
                    // Create new cell with a container
                    Cell containerCell(OCCUPIED);
                    containerCell.setContainer(toMove);

                    // Set the cell in the buffer to the new ContainerCell
                    deriv->buffer.setCell(NEW_COORD.x, NEW_COORD.y, containerCell);

                    // calculate A*
                    deriv->calculateAStar();

                    acc.push_back(deriv);
                }

            }
        }
        break;
    }
    }
    return acc;
}
