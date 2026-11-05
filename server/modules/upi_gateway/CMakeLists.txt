fincero_add_library(fincero_upi_gateway
    SOURCES src/module.cpp
    PUBLIC_DEPS fincero_platform fincero_money fincero_upi_text fincero_txn)
