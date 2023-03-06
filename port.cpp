#include "port.hpp"

int Port::getTotalCost() const
{
    return costToGetHere + calculateHeuristic();
}