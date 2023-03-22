#include "container.hpp"

std::string Container::getDescription() const
{
    return description;
}

std::string Container::toString() const
{
    std::string acc = description;
    acc += " (";
    acc += weight;
    acc += " kg)";
    return acc;
}

int Container::getWeight() const
{
    return weight;
}

bool Container::isToBeOffloaded() const
{
    return toOffload;
}
