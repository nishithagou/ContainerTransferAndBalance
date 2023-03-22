#ifndef CONTAINER_HPP
#define CONTAINER_HPP
#include <string>

class Container
{
    int weight;
    std::string description;
    // only useful for transfer
    bool toOffload;
    public:
    Container(std::string description, int weight) : description(description), weight(weight), 
        toOffload(false) {}
    Container(std::string description, int weight, bool toOffload): description(description), weight(weight), 
        toOffload(toOffload) {}
    const std::string getDescription() const;
    const std::string toString() const;
    const int getWeight() const;
    const bool isToBeOffloaded() const;
};

#endif