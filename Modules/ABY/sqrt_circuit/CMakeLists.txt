cmake_minimum_required(VERSION 3.10)
find_package(Boost REQUIRED COMPONENTS thread system)
find_package(ABY QUIET)
if(ABY_FOUND)
	message(STATUS "Found ABY")
elseif (NOT ABY_FOUND AND NOT TARGET ABY::aby)
	message("ABY was not found: add ABY subdirectory")
	add_subdirectory(extern/ABY)
endif()


add_executable(sqrt_test sqrt_test.cpp common/sqrt.cpp)
target_link_libraries(sqrt_test ABY::aby ENCRYPTO_utils::encrypto_utils)


