#include <iostream>
#include <unordered_set>
#include <algorithm>
#include "port.hpp"

using namespace std;

int main(int argc, char** argv){
    // some hardcoded values to be added
    vector<pair<Cell, Coordinate>> shipLoad; 
    vector<Container *> allContainers;
    const Cell hull(HULL);
    for (int i = 0; i < 4; i++){
        pair<Cell, Coordinate> hullSpot(hull, Coordinate(0, 8-i));
        shipLoad.push_back(hullSpot);
        pair<Cell, Coordinate> hullSpot2(hull, Coordinate(11, 8-i));
        shipLoad.push_back(hullSpot2);
        allContainers.push_back(new Container("Container Ld " + i, 100+i));
        pair<Cell, Coordinate> containerSpot(Cell(allContainers.back()), Coordinate(1, 8-i));
        shipLoad.push_back(containerSpot);
    }
    allContainers.push_back(new Container("Container to Offload", 420, true));
    pair<Cell, Coordinate> toAdd(Cell(allContainers.back()), Coordinate(2, 8));
    shipLoad.push_back(toAdd);
    vector<Container *> toLoad;
    toLoad.push_back(new Container("From truck 1", 100));
    toLoad.push_back(new Container("From truck 2", 200));
    
    // cannot use the stack data structure because I need to sort
    // but stack functions pretty much like an actual stack as I in add to the top and pop
    // from the top 
    vector<Port*> stack;
    Transfer* base = new Transfer(Coordinate(12,9), Coordinate(24, 5), shipLoad, toLoad);
    // those who do not learn from history are doomed to repeat it literally
    unordered_set<string> history;
    history.insert(base->toStringBasic());
    stack.push_back(base);
    Port* solution = nullptr;
    while(stack.size() > 0){    
        if (stack.back()->isSolved()){
            solution = stack.back();
            break;
        }

        // expand cheapest node
        list<Port*> derivs = stack.back()->tryAllOperators();

        
        stack.pop_back();
        

        // look through derivs
        for (list<Port*>::iterator it = derivs.begin(); it != derivs.end(); ){
            if (history.contains((*it)->toStringBasic())){
                if (it == derivs.begin()){
                    derivs.pop_front();
                    it = derivs.begin();
                    continue;
                }
                else if ((*it)==derivs.back()){
                    derivs.pop_back();
                    break;
                }
                list<Port*>::iterator next = it++;
                it--;
                // I don't feel so confident about not causing any memory leaks
                derivs.erase(it);
                it = next;
            }
            else{
                stack.push_back((*it));
                it++;
            }
        }

        // sort
        sort(stack.begin(), stack.end(), Port::greaterThan);
    }
    cout << solution->getMoveDescription() << endl;
    return 0;
}