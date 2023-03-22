#ifndef COORDINATE_HPP
#define COORDINATE_HPP

/// @brief Just a convient way to hold two numbers that's it
struct Coordinate{
    int x;
    int y;
    Coordinate(const int x, const int y): x(x), y(y) {}
    /// @brief Trying to offload as much code from port to here
    /// @param rhs 
    /// @return a boolean whether Coordinates are equal
    virtual bool operator!=(const Coordinate& rhs) const 
        { return (rhs.x != x) || (rhs.y != y); }
    virtual bool operator==(const Coordinate& rhs) const
        { return (rhs.x == x) && (rhs.y == y); }
    std::string& toString() const {
        // complier complains I think there is a more elegant solution but I'm too tired to 
        // look it up 
        std::string acc = "(";
        acc += x;
        acc += ", ";
        acc += y;
        acc += ")";
        return acc; 

    }
};

/// @brief Ok it might be helpful for transfer if I knew which containers are in the buffer
/// however no other "Coordinate" needs a to hold a boolean value
struct ContainerCoordinate:public Coordinate{
    bool isInBuffer;
    ContainerCoordinate (const int x, const int y): Coordinate(x, y), isInBuffer{false} {}
    ContainerCoordinate (const int x, const int y, const bool isInBuffer): 
        Coordinate(x,y), isInBuffer(isInBuffer) {}
};
#endif