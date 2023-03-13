#ifndef COORDINATE_HPP
#define COORDINATE_HPP

/// @brief Just a convient way to hold two numbers that's it
struct Coordinate{
    int x;
    int y;
    Coordinate(const int x, const int y): x(x), y(y) {}
};

/// @brief Ok it might be helpful for transfer if I knew which containers are in the buffer
/// however no other "Coordinate" needs a to hold a boolean value
struct ContainerCoordinate:public Coordinate{
    bool isInBuffer;
    ContainerCoordinate (const int x, const int y): Coordinate(x, y), isInBuffer{false} {}
};
#endif