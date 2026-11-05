#include "fincero/base/module.hpp"

#include <gtest/gtest.h>
#include <rapidcheck.h>

#include <string_view>

// Proves the core test stack works. Replaced by real tests from M1.
TEST(Smoke, CoreTargetLinks) {
    EXPECT_EQ(std::string_view{fincero::base::module_name()}, "base");
}

TEST(Smoke, PropertyFrameworkRuns) {
    EXPECT_TRUE(rc::check("xor with zero is identity", [](int value) {
        RC_ASSERT((value ^ 0) == value);
    }));
}
