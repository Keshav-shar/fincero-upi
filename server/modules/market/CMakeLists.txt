fincero_add_library(fincero_market
    SOURCES src/module.cpp
    PUBLIC_DEPS fincero_platform fincero_ledger_cero fincero_market_model fincero_rng fincero_prediction)
