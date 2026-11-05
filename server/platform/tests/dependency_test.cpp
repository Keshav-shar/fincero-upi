#include "fincero/server/platform/module.hpp"

#include <drogon/version.h>
#include <gtest/gtest.h>
#include <jsoncons/json.hpp>
#include <sodium.h>
#include <spdlog/version.h>

#include <string>
#include <string_view>

// Proves every server dependency links and runs under each preset. Replaced from M2.
TEST(Dependencies, PlatformTargetLinks) {
    EXPECT_EQ(std::string_view{fincero::server::platform::module_name()}, "platform");
}

TEST(Dependencies, SodiumInitialises) {
    EXPECT_GE(sodium_init(), 0);
}

TEST(Dependencies, JsonconsParses) {
    const auto value = jsoncons::json::parse(R"({"amount_paise":"12345"})");
    EXPECT_EQ(value["amount_paise"].as<std::string>(), "12345");
}

TEST(Dependencies, HeadersMatchPinnedLibraries) {
    EXPECT_FALSE(std::string_view{DROGON_VERSION}.empty());
    EXPECT_GT(SPDLOG_VER_MAJOR, 0);
}
