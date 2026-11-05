add_subdirectory(fuzz)

# The gates must be able to fail, so they are tested like any other code.
add_test(NAME gates_selftest
    COMMAND ${Python3_EXECUTABLE} ${PROJECT_SOURCE_DIR}/cmake/tests/test_gates.py)
