#ifndef CONTAINER_HPP
#define CONTAINER_HPP
#include <string>

class Container
{
    std::string description;
    bool toOffload;
    int weight;
    public:
    Container(std::string description, int weight) : description(description), weight(weight), toOffload(false) {}
    Container(std::string description, int weight, bool toOffload): description(description), 
        weight(weight), toOffload(toOffload) {}
    const std::string getDescription() const;
    const int getWeight() const;
};

#endif