cmake_minimum_required(VERSION 3.26)
project({{ cookiecutter.task_name }})

set(CMAKE_CXX_STANDARD 14)

#
# {{ cookiecutter.task_name }} library
#

add_library({{ cookiecutter.task_name }}lib src/{{ cookiecutter.task_name }}.cpp src/{{ cookiecutter.task_name }}.h)
set_target_properties({{ cookiecutter.task_name }}lib PROPERTIES
        CXX_STANDARD 14
        CXX_STANDARD_REQUIRED YES
        CXX_EXTENSIONS NO)

#
# Main executable
#

add_executable({{ cookiecutter.task_name }} src/main.cpp)

add_dependencies({{ cookiecutter.task_name }}
        {{ cookiecutter.task_name }}lib)

target_link_libraries({{ cookiecutter.task_name }}
        {{ cookiecutter.task_name }}lib)

#
# Unit tests
#
add_executable(unittests
        src/tests/main.cpp
        src/tests/{{ cookiecutter.task_name }}_unittest.cpp)

set_target_properties(unittests PROPERTIES
        CXX_STANDARD 14
        CXX_STANDARD_REQUIRED YES
        CXX_EXTENSIONS NO)

target_include_directories(unittests PRIVATE
        "${PROJECT_SOURCE_DIR}/src")

add_dependencies(unittests
        {{ cookiecutter.task_name }}lib)

target_link_libraries(unittests
        {{ cookiecutter.task_name }}lib)

#
# GoogleTest - find in packages or download from github and compile on-the-fly.
#

find_package(GTest)
if (GTest_FOUND)
    message(STATUS "Using installed googletest package.")

    target_include_directories(unittests PRIVATE
            ${GTEST_INCLUDE_DIRS})

    target_link_libraries(unittests
            ${GTEST_LIBRARIES})

else ()
    message(STATUS "Fallback to googletest downloading on-the-fly.")

    # download googletest
    configure_file(CMakeLists.txt.gtest.in googletest-download/CMakeLists.txt)

    execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" .
            RESULT_VARIABLE result
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download)
    if (result)
        message(FATAL_ERROR "CMake step for googletest failed: ${result}")
    endif ()

    execute_process(COMMAND ${CMAKE_COMMAND} --build .
            RESULT_VARIABLE result
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download)
    if (result)
        message(FATAL_ERROR "Build step for googletest failed: ${result}")
    endif ()

    # prevent overriding the parent project's compiler/linker on windows
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

    # add googletest to build. This defines the gtest and gtest_main targets.
    add_subdirectory(${CMAKE_CURRENT_BINARY_DIR}/googletest-src
            ${CMAKE_CURRENT_BINARY_DIR}/googletest-build
            EXCLUDE_FROM_ALL)

    target_include_directories(unittests PRIVATE
            "${CMAKE_CURRENT_BINARY_DIR}/googletest-src"
            "${CMAKE_CURRENT_BINARY_DIR}/googletest-src/include")

    target_link_libraries(unittests
            gtest_main)

endif ()
