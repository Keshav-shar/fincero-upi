#include "fincero/rng/source.hpp"

namespace fincero::rng {

// A plain repeating sequence, so public builds compile and run.
Draw next_draw(Cursor cursor, const SourceData& /*data*/) noexcept {
    const auto digit = static_cast<std::uint8_t>((cursor.position * 7U + 3U) % 10U);
    return Draw{.digit = digit,
                .next = Cursor{.position = cursor.position + 1U, .epoch = cursor.epoch}};
}

bool is_production_source() noexcept {
    return false;
}

} // namespace fincero::rng
