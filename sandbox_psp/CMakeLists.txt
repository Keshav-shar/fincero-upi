# Simulator only. It implies no NPCI behaviour or approval.
fincero_add_executable(fincero_sandbox_psp
    SOURCES src/main.cpp
    DEPS fincero_platform fincero_upi_text)
