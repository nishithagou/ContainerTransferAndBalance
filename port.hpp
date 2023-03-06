#ifndef PORT_HPP
#define PORT_HPP
#include "space.hpp"
#include "coordinate.hpp"
#include <vector>
#include <utility>

/// @brief Abstract class of Port which shares similar properties for both transfer
/// and balance
/// @return 
class Port{
    // cost defined as minutes i.e. Manhattan Distance
    int costToGetHere;
    Space ship;
    public:
    virtual int toHashIndex() const = 0;
    virtual bool operator==(const Port& rhs) const = 0;
    virtual std::vector<Port*> tryAllOperators() const = 0;
    int getTotalCost() const;
    private:
    virtual int calculateHeuristic() const = 0;
};

class Transfer: public Port{
    Space buffer;
    public:
    Transfer(Coordinate shipSize, Coordinate bufferSize, std::vector<std::pair<Container, Coordinate>> shipLoad);
    int toHashIndex() const;
    bool operator==(const Port& rhs) const;
    std::vector<Port*> tryAllOperators() const;
};
#endif