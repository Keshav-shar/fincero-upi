# C++ side of the @fincero/core TurboModule. Links the client slice of core only.
fincero_add_library(fincero_client_binding
    SOURCES src/module.cpp
    PUBLIC_DEPS fincero_core_client)
