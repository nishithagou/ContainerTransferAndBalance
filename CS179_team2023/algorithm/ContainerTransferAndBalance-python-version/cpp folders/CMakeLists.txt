CMAKE_MINIMUM_REQUIRED(VERSION 3.5)

project(PROTOTYPE_TRANSFER_AND_BALANCE)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_compile_options(-Wall -Wextra -Wpedantic -O0 -g)

ADD_EXECUTABLE(a.out
    container.cpp
    port.cpp
    space.cpp
	main.cpp
)