#ifndef CONTAINER_HPP
#define CONTAINER_HPP
#include <string>

class Container
{
    std::string description;
    int weight;
    public:
    Container(std::string description, int weight) : description(description), weight(weight) {}
    const std::string getDescription() const;
    const int getWeight() const;
};

#endif