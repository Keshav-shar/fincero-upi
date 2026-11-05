# Public stand-in for builds without the private source. Never for production:
# the `release` preset refuses it.
fincero_add_library(fincero_rng
    SOURCES src/stub_source.cpp
    PUBLIC_DEPS fincero_rng_api fincero_base)
