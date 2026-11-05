# Private, so absent from public clones.
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/gen_digits/CMakeLists.txt")
    add_subdirectory(gen_digits)
endif()
add_subdirectory(econ_sim)
add_subdirectory(market_replay)
