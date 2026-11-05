# Neutral interface to the market's randomness. The implementation is fincero_rng.
add_library(fincero_rng_api INTERFACE)
target_include_directories(fincero_rng_api INTERFACE include)

# Holds for the real source and the public stand-in alike.
fincero_add_test(fincero_rng_api_tests
    SOURCES tests/contract_test.cpp
    DEPS fincero_rng)
