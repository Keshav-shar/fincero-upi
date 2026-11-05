if(NOT FINCERO_ENABLE_FUZZ)
    return()
endif()

# Each parser gets a target here from M1.
add_executable(fuzz_placeholder placeholder_fuzz.cpp)
target_link_options(fuzz_placeholder PRIVATE -fsanitize=fuzzer)
set_target_properties(fuzz_placeholder PROPERTIES CXX_CLANG_TIDY "")
fincero_apply_warnings(fuzz_placeholder)
