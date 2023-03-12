#ifndef PORT_HPP
#define PORT_HPP
#include "space.hpp"
#include "coordinate.hpp"
#include <vector>
#include <utility>
#include <list>

enum CraneState {SHIP, BUFFER, TRUCKBAY};

/// @brief Abstract class of Port which shares similar properties for both transfer
/// and balance
/// @return 
class Port{
    // cost defined as minutes i.e. Manhattan Distance
    protected:
    Coordinate cranePosition;
    char craneState;
    int costToGetHere;
    Space ship;
    Space buffer;
    public:
    Port();
    Port(const Coordinate& shipSize, const Coordinate& bufferSize);
    virtual int toHashIndex() const = 0;
    virtual bool operator==(const Port& rhs) const = 0;
    virtual std::list<Port*> tryAllOperators() const = 0;
    int getTotalCost() const;
    protected:
    virtual int calculateHeuristic() const = 0;
};

class Transfer: public Port{
    private:
    std::vector<std::pair<ContainerCoordinate, Container*>> toOffload;
    std::vector<std::pair<ContainerCoordinate, Container*>> toLoad;
    std::vector<std::pair<ContainerCoordinate, Container*>> toStay;
    public:
    Transfer(const Coordinate& shipSize, 
        const Coordinate& bufferSize, 
        const std::vector<std::pair<Cell, Coordinate>>& shipLoad, 
        std::vector<Container*>& toLoad);
    int toHashIndex() const;
    bool operator==(const Transfer& rhs) const;
    std::list<Port*> tryAllOperators() const;
    private:
    int calculateHeuristic() const;
    int calculateManhattanDistance(const Coordinate& start, const Coordinate& end, 
        const char startSpace, const char endSpace) const;
};
#endif