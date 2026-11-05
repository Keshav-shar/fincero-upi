fincero_add_library(fincero_platform
    SOURCES src/module.cpp
    PUBLIC_DEPS fincero_base Drogon::Drogon jsoncons spdlog::spdlog unofficial-sodium::sodium)

fincero_add_test(fincero_platform_tests
    SOURCES tests/dependency_test.cpp
    DEPS fincero_platform)
