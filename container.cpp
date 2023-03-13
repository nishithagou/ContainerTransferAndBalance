#include "container.hpp"

const std::string Container::getDescription() const
{
    return description;
}

const int Container::getWeight() const
{
    return weight;
}

const bool Container::isToBeOffloaded() const
{
    return toOffload;
}
