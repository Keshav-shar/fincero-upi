cmake_minimum_required(VERSION 3.28)

# Must come before project(): vcpkg reads it when the toolchain loads.
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/tools/gen_digits/CMakeLists.txt")
    list(APPEND VCPKG_MANIFEST_FEATURES "offline-tools")
endif()

project(fincero VERSION 0.0.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(FINCERO_WERROR "Treat compiler warnings as errors" ON)
option(FINCERO_ENABLE_TIDY "Run clang-tidy while compiling" OFF)
option(FINCERO_ENABLE_FUZZ "Build libFuzzer targets (Clang only)" OFF)
option(FINCERO_REQUIRE_REAL_RNG "Fail instead of using the public RNG stand-in" OFF)
set(FINCERO_SANITIZE "" CACHE STRING "Comma-separated -fsanitize list, e.g. address,undefined")

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(FinceroSanitizers)
include(FinceroTargets)

enable_testing()
include(GoogleTest)
find_package(GTest CONFIG REQUIRED)
find_package(rapidcheck CONFIG REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

if(FINCERO_ENABLE_TIDY)
    find_program(FINCERO_CLANG_TIDY NAMES clang-tidy REQUIRED)
    set(CMAKE_CXX_CLANG_TIDY "${FINCERO_CLANG_TIDY}")
endif()

# Dependency direction: client and server depend on core; core depends on nothing
# but the standard library. cmake/check_boundaries.py enforces this on the real graph.
add_subdirectory(core)
add_subdirectory(server)
add_subdirectory(sandbox_psp)
add_subdirectory(client/native/fincero-core)
add_subdirectory(tools)
add_subdirectory(tests)
