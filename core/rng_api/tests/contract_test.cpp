#include "fincero/rng/source.hpp"

#include <gtest/gtest.h>

#include <array>
#include <cstdint>

namespace {

using fincero::rng::Cursor;
using fincero::rng::Draw;
using fincero::rng::next_draw;
using fincero::rng::SourceData;

const std::array<std::uint8_t, 4> kPrimary{1, 2, 3, 4};
const std::array<std::uint8_t, 4> kSecondary{5, 6, 7, 8};

SourceData data() {
    return SourceData{kPrimary, kSecondary};
}

TEST(RngContract, SameCursorGivesSameDraw) {
    const Cursor cursor{.position = 3, .epoch = 0};
    const Draw first = next_draw(cursor, data());
    const Draw second = next_draw(cursor, data());
    EXPECT_EQ(first.digit, second.digit);
    EXPECT_EQ(first.next.position, second.next.position);
    EXPECT_EQ(first.next.epoch, second.next.epoch);
}

TEST(RngContract, DigitsStayInRangeAndCursorMoves) {
    Cursor cursor{};
    for (int step = 0; step < 1000; ++step) {
        const Draw draw = next_draw(cursor, data());
        EXPECT_LE(draw.digit, 9);
        const bool moved = draw.next.position != cursor.position || draw.next.epoch != cursor.epoch;
        EXPECT_TRUE(moved);
        cursor = draw.next;
    }
}

} // namespace
