# Links the production rules so that results cannot drift from them.
fincero_add_executable(fincero_econ_sim
    SOURCES main.cpp
    DEPS fincero_economy_rules fincero_market_model fincero_rng)
