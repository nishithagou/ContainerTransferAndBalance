#include <iostream>
#include <unordered_map>
#include "port.hpp"

using namespace std;

int main(int argc, char** argv){
    // some hardcoded values to be added
    vector<pair<Cell, Coordinate>> shipLoad; 
    vector<Container *> allContainers;
    const Cell hull(HULL);
    for (int i = 0; i < 4; i++){
        pair<Cell, Coordinate> hullSpot(hull, Coordinate(0, i));
        shipLoad.push_back(hullSpot);
        pair<Cell, Coordinate> hullSpot2(hull, Coordinate(11, i));
        shipLoad.push_back(hullSpot2);
        allContainers.push_back(new Container("Container Ld " + i, 100+i));
        pair<Cell, Coordinate> containerSpot(Cell(allContainers.back()), Coordinate(1, i));
        shipLoad.push_back(containerSpot);
    }
    allContainers.push_back(new Container("Container to Offload", 420, true));
    pair<Cell, Coordinate> toAdd(Cell(allContainers.back()), Coordinate(2, 0));
    shipLoad.push_back(toAdd);
    vector<Container *> toLoad;
    toLoad.push_back(new Container("From truck 1", 100));
    toLoad.push_back(new Container("From truck 2", 200));
    
    Transfer base(Coordinate(12,9), Coordinate(24, 5), shipLoad, toLoad);
    string tostring = base.toStringBasic();
    cout << tostring << endl;
    return 0;
}