# Target helpers, so every library, program and test gets the same rules.

# Strict warnings, on our own targets only. Third-party headers come in as SYSTEM.
function(fincero_apply_warnings target)
    target_compile_options(${target} PRIVATE
        -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Wshadow
        -Wnon-virtual-dtor -Wold-style-cast -Wcast-align -Woverloaded-virtual
        -Wnull-dereference -Wimplicit-fallthrough)
    if(FINCERO_WERROR)
        target_compile_options(${target} PRIVATE -Werror)
    endif()
endfunction()

# Static library following the include/ + src/ convention of the calling directory.
function(fincero_add_library name)
    cmake_parse_arguments(PARSE_ARGV 1 ARG "" "" "SOURCES;PUBLIC_DEPS;PRIVATE_DEPS")
    add_library(${name} STATIC ${ARG_SOURCES})
    target_include_directories(${name} PUBLIC include)
    target_link_libraries(${name} PUBLIC ${ARG_PUBLIC_DEPS} PRIVATE ${ARG_PRIVATE_DEPS})
    fincero_apply_warnings(${name})
endfunction()

function(fincero_add_executable name)
    cmake_parse_arguments(PARSE_ARGV 1 ARG "" "" "SOURCES;DEPS")
    add_executable(${name} ${ARG_SOURCES})
    target_link_libraries(${name} PRIVATE ${ARG_DEPS})
    fincero_apply_warnings(${name})
endfunction()

# GoogleTest binary. clang-tidy stays off here because test macros trip rules
# that are aimed at production code.
function(fincero_add_test name)
    cmake_parse_arguments(PARSE_ARGV 1 ARG "" "" "SOURCES;DEPS")
    add_executable(${name} ${ARG_SOURCES})
    target_link_libraries(${name} PRIVATE ${ARG_DEPS} GTest::gtest_main)
    set_target_properties(${name} PROPERTIES CXX_CLANG_TIDY "")
    fincero_apply_warnings(${name})
    gtest_discover_tests(${name} DISCOVERY_MODE PRE_TEST)
endfunction()
