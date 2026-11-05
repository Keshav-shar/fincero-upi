# Pure C++20. No I/O, clocks or global RNG; cmake/check_core_purity.py enforces this.
add_subdirectory(base)
add_subdirectory(money)
add_subdirectory(upi_text)
add_subdirectory(ledger)
add_subdirectory(txn)
add_subdirectory(rng)
add_subdirectory(market)
add_subdirectory(economy)
add_subdirectory(prediction)

# Everything, for tools that need the whole engine.
add_library(fincero_core INTERFACE)
target_link_libraries(fincero_core INTERFACE
    fincero_base fincero_money fincero_upi_text fincero_ledger_rules fincero_txn
    fincero_rng fincero_market_model fincero_economy_rules fincero_prediction)

# The only slice that ships to clients. It must never include the RNG (Rule 7).
add_library(fincero_core_client INTERFACE)
target_link_libraries(fincero_core_client INTERFACE
    fincero_base fincero_money fincero_upi_text)
