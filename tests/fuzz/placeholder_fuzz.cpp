#include <cstddef>
#include <cstdint>

// Proves the fuzz toolchain works. Replaced by parser targets from M1.
extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t* /*data*/, std::size_t /*size*/) {
    return 0;
}
