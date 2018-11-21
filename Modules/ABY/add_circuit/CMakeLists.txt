cmake_minimum_required(VERSION 3.10)

find_package(ABY QUIET)
if(ABY_FOUND)
	message(STATUS "Found ABY")
elseif (NOT ABY_FOUND AND NOT TARGET ABY::aby)
	message("ABY was not found: add ABY subdirectory")
	add_subdirectory(extern/ABY)
endif()


add_executable(add_test add_test.cpp common/add.cpp)
target_link_libraries(add_test ABY::aby ENCRYPTO_utils::encrypto_utils)


