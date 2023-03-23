#ifndef CONTAINER_HPP
#define CONTAINER_HPP
#include <string>

class Container
{
    std::string description;
    int weight;
    // only useful for transfer
    bool toOffload;
    public:
    Container(const std::string description, const int weight) : description(description), 
        weight(weight), toOffload(false) {}
    Container(const std::string description, const int weight, const bool toOffload): 
        description(description), weight(weight), toOffload(toOffload) {}
    std::string getDescription() const;
    std::string toString() const;
    int getWeight() const;
    bool isToBeOffloaded() const;
};

#endif