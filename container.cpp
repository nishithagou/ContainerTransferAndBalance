#include "container.hpp"

const std::string Container::getDescription() const
{
    return description;
}

const std::string Container::toString() const
{
    std::string acc = description;
    acc += " (";
    acc += weight;
    acc += " kg)";
    return acc;
}

const int Container::getWeight() const
{
    return weight;
}

const bool Container::isToBeOffloaded() const
{
    return toOffload;
}
