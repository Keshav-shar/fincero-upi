# Applies FINCERO_SANITIZE to every target in the project.
if(FINCERO_SANITIZE)
    add_compile_options(-fsanitize=${FINCERO_SANITIZE} -fno-omit-frame-pointer
                        -fno-sanitize-recover=all)
    add_link_options(-fsanitize=${FINCERO_SANITIZE})
endif()

if(FINCERO_ENABLE_FUZZ)
    if(NOT CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        message(FATAL_ERROR "FINCERO_ENABLE_FUZZ needs Clang")
    endif()
    add_compile_options(-fsanitize=fuzzer-no-link)
endif()
