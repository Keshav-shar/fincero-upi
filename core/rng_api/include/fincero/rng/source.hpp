#pragma once

#include <cstdint>
#include <span>

namespace fincero::rng {

// Position in the source. Persisted by the market and never exposed (Rule 7).
struct Cursor {
    std::uint64_t position = 0;
    std::uint32_t epoch = 0;
};

struct Draw {
    std::uint8_t digit = 0; // 0 to 9
    Cursor next;
};

// Read-only data the source may need. The caller loads it, so core does no I/O.
struct SourceData {
    std::span<const std::uint8_t> primary;
    std::span<const std::uint8_t> secondary;
};

// Pure: the same cursor and data always give the same draw.
[[nodiscard]] Draw next_draw(Cursor cursor, const SourceData& data) noexcept;

// False for the public stand-in, so the server can refuse to run on it.
[[nodiscard]] bool is_production_source() noexcept;

} // namespace fincero::rng
