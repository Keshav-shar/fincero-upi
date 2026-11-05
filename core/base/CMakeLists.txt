fincero_add_library(fincero_base
    SOURCES src/module.cpp)

fincero_add_test(fincero_base_tests
    SOURCES tests/smoke_test.cpp
    DEPS fincero_base rapidcheck)
