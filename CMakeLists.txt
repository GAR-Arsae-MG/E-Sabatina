cmake_minimum_required(VERSION 3.20)

project(e-sabatina
    VERSION 0.1.0
    DESCRIPTION "Hybrid C++20 + Python project"
    LANGUAGES CXX
)

# -------------------------------
#   C++ SETTINGS
# -------------------------------
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Output directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/builds/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/builds/lib)

# -------------------------------
#   SOURCES
# -------------------------------
file(GLOB_RECURSE E_SABATINA_CPP_SOURCES
    ${CMAKE_SOURCE_DIR}/src/cpp/*.cpp
    ${CMAKE_SOURCE_DIR}/src/cpp/*.cc
)

add_executable(e-sabatina ${E_SABATINA_CPP_SOURCES})

target_include_directories(e-sabatina PRIVATE
    ${CMAKE_SOURCE_DIR}/src/cpp
)

# -------------------------------
#   OPTIONAL: PYTHON INTEGRATION
# -------------------------------
# Enable this if you want C++ <-> Python bindings later
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
target_link_libraries(e-sabatina PRIVATE Python3::Python)
