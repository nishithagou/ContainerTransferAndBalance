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
    /// @brief describes the move done; only to be modified in tryAllOperators
    std::string moveDescription;
    /// @brief parent describes how the Port is derived from
    Port* parent;
    Coordinate cranePosition;
    char craneState;
    /// @brief the number of minutes it took to reach this Port i.e. g(n)
    int costToGetHere;
    /// @brief The lower bound number of minutes it has taken and will take for the Port to
    /// finish
    int aStarCost;
    bool solved;
    Space ship;
    Space buffer;
    public:
    Port();
    Port(const Coordinate& shipSize, const Coordinate& bufferSize);
    virtual bool operator==(const Port& rhs) const;
    bool operator<(const Port& rhs) const;
    static bool greaterThan(const Port* lhs, const Port* rhs);
    virtual std::list<Port*> tryAllOperators() const = 0;
    void calculateAStar();
    std::string getMoveDescription() const;
    virtual std::string toStringBasic() const = 0;
    bool isSolved() const;
    protected:
    virtual int calculateHeuristic()  = 0;
    int calculateManhattanDistance(const Coordinate& start, const Coordinate& end, 
        const char startSpace, const char endSpace) const;
    static std::string toStringFromState(const char state);
};

/// @brief For transfer operations of the abstract Port class
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
    std::list<Port*> tryAllOperators() const;
    virtual std::string toStringBasic() const;
    private:
    int calculateHeuristic();
    void moveContainerAndCrane(Container* c, const Coordinate& start, const Coordinate& end,  
        const char startSpace, const char endSpace);
    Transfer* createDerivatative(Container* c, const Coordinate& end, const char endSpace) const;
    void updateContainerCoordinateVectors(Container* container, const Coordinate& newPosition, const char newSpace);
};
#endif