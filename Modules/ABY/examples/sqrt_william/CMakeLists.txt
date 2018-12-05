cmake_minimum_required(VERSION 3.10)
find_package(Boost REQUIRED COMPONENTS thread system)
find_package(ABY QUIET)
if(ABY_FOUND)
	message(STATUS "Found ABY")
elseif (NOT ABY_FOUND AND NOT TARGET ABY::aby)
	message("ABY was not found: add ABY subdirectory")
	add_subdirectory(extern/ABY)
endif()



add_executable(Evaluator Evaluator.cpp common/circuit.cpp common/utils.cpp)
add_executable(CSP CSP.cpp common/circuit.cpp common/utils.cpp)
target_link_libraries(Evaluator ABY::aby ENCRYPTO_utils::encrypto_utils)
target_link_libraries(CSP ABY::aby ENCRYPTO_utils::encrypto_utils)
