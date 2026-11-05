fincero_add_executable(fincero_server
    SOURCES main.cpp
    DEPS fincero_identity fincero_upi_gateway fincero_ledger_inr fincero_ledger_cero
         fincero_economy fincero_market fincero_assistant fincero_notifications)
